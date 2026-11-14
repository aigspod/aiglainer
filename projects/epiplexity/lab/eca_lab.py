"""Our own laptop-scale versions of two experiments in arXiv:2601.03220 (not the authors' code or results).

1. `rules`: predict Y = F^k(X) from a random row X for elementary cellular automaton rules (like Fig. 3, much smaller),
   plus a coin-flip control (Y independent of X). A small transformer is trained online on fresh samples, so each
   step's loss is measured on data it has not seen yet (prequential). We record the loss curve and estimate
   structure as the area above the final loss (the paper's prequential heuristic, eq. 8), in bits.
2. `order`: rule 30 as a stand-in one-way function (like Fig. 4a): model the pair (X, Y=F^k(X)) as X then Y
   ("forward") or Y then X ("reverse"), and compare total bits per pair with the true entropy (n bits).

Usage:  python eca_lab.py rules    python eca_lab.py order     (writes ../data/ours_*.json)
Runs on Apple's MPS if available. Everything is labelled 'our run' wherever it is shown.
"""
import json, math, os, sys, time
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'
LN2 = math.log(2)


def eca_step(x, rule):
    """x: (B, n) uint8 in {0,1}, periodic boundary."""
    l, r = np.roll(x, 1, 1), np.roll(x, -1, 1)
    idx = (l << 2) | (x << 1) | r
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    return table[idx]


def eca_run(x, rule, k):
    for _ in range(k):
        x = eca_step(x, rule)
    return x


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1, s.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        s.att = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(s, x, mask):
        a = s.ln1(x)
        x = x + s.att(a, a, a, attn_mask=mask, need_weights=False)[0]
        return x + s.mlp(s.ln2(x))


class GPT(nn.Module):
    def __init__(s, vocab, L, d=128, layers=4, heads=4):
        super().__init__()
        s.tok, s.pos = nn.Embedding(vocab, d), nn.Parameter(torch.zeros(1, L, d))
        nn.init.normal_(s.pos, std=0.02)
        s.blocks = nn.ModuleList([Block(d, heads) for _ in range(layers)])
        s.ln, s.head = nn.LayerNorm(d), nn.Linear(d, vocab)
        s.register_buffer('mask', torch.triu(torch.ones(L, L, dtype=torch.bool), 1))

    def forward(s, idx):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos[:, :T]
        for b in s.blocks:
            x = b(x, s.mask[:T, :T])
        return s.head(s.ln(x))


def train(make_batch, L, loss_slice, steps, bs=128, lr=1e-3, seed=0, log_every=25, **arch):
    """Online training on fresh batches. Returns per-step mean loss (bits per predicted sequence) on each batch
    *before* training on it (prequential), and the parameter count."""
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    m = GPT(3, L, **arch).to(DEV)
    nparams = sum(p.numel() for p in m.parameters())
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=0.0, betas=(0.9, 0.98))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda i: min(1.0, (i + 1) / 200))
    curve = []
    t0 = time.time()
    for i in range(steps):
        seq = torch.from_numpy(make_batch(rng, bs)).long().to(DEV)  # (B, L)
        logits = m(seq[:, :-1])[:, :, :2]          # predictions are over the bits {0, 1} only
        tgt = seq[:, 1:].clamp(max=1)              # SEP targets are never scored (outside loss_slice)
        lp = F.cross_entropy(logits.transpose(1, 2), tgt, reduction='none')  # (B, L-1) nats
        a, b = loss_slice
        loss_bits_seq = lp[:, a:b].sum(1).mean() / LN2       # bits per sequence on the scored part
        opt.zero_grad(set_to_none=True)
        (lp[:, a:b].mean()).backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step(); sched.step()
        curve.append(float(loss_bits_seq))
        if i % log_every == 0:
            print(f'  step {i:5d}  {curve[-1]:8.3f} bits/seq  {time.time() - t0:6.1f}s', flush=True)
    return np.array(curve), nparams


def prequential(curve, bs, tail=0.05):
    """Area above the final loss, in bits, summed over every training example (eq. 8, batch of bs per step)."""
    k = max(10, int(len(curve) * tail))
    final = float(np.mean(curve[-k:]))
    area = float(np.sum(np.clip(curve - final, 0, None)) * bs)
    return final, area


def run_rules(n=32, k=4, steps=3000, bs=128):
    """Conditional task Y | X: tokens X (n bits), SEP (2), Y (n bits); loss on Y only."""
    L = 2 * n + 1
    out = dict(source='our run (not the paper): ' + __doc__.split('\n')[2].strip(), n=n, k=k, steps=steps,
               batch=bs, device=DEV, units='bits per sequence of Y (n bits); area in bits', runs={})
    for name in ['15', '30', '54', '110', 'coin']:
        def make_batch(rng, B, name=name):
            x = rng.integers(0, 2, (B, n), dtype=np.uint8)
            y = rng.integers(0, 2, (B, n), dtype=np.uint8) if name == 'coin' else eca_run(x, int(name), k)
            return np.concatenate([x, np.full((B, 1), 2, np.uint8), y], 1)
        print(f'rule {name}', flush=True)
        t0 = time.time()
        curve, npar = train(make_batch, L, (n, 2 * n), steps, bs)
        final, area = prequential(curve, bs)
        out['runs'][name] = dict(curve=[round(v, 4) for v in curve[::5].tolist()], every=5, final_bits=final,
                                 area_bits=area, params=npar, seconds=round(time.time() - t0, 1))
        print(f'  -> final {final:.3f} bits/seq, area {area:.3e} bits, {npar} params', flush=True)
        json.dump(out, open(os.path.join(DATA, f'ours_rules_n{n}_k{k}_s{steps}.json'), 'w'))
    return out


def run_order(sizes=(8, 12, 16, 20, 24), k=8, steps=3000, bs=128, seed=0, n=0):
    sizes = (n,) if n else sizes
    """Joint modelling of (X, Y=rule30^k(X)) in two orders; loss on all 2n bits."""
    out = dict(source='our run (not the paper): rule 30, k steps, forward = X then Y, reverse = Y then X',
               k=k, steps=steps, batch=bs, device=DEV, units='bits per (X,Y) pair; entropy = n', runs={})
    for n in sizes:
        L = 2 * n + 1
        for direction in ['forward', 'reverse']:
            def make_batch(rng, B, n=n, direction=direction):
                x = rng.integers(0, 2, (B, n), dtype=np.uint8)
                y = eca_run(x, 30, k)
                a, b = (x, y) if direction == 'forward' else (y, x)
                return np.concatenate([np.full((B, 1), 2, np.uint8), a, b], 1)
            print(f'n={n} {direction}', flush=True)
            curve, npar = train(make_batch, L + 1, (0, 2 * n), steps, bs, seed=seed)
            final, area = prequential(curve, bs)
            out['runs'][f'{n}_{direction}'] = dict(n=n, direction=direction, final_bits=final, area_bits=area,
                                                    curve=[round(v, 4) for v in curve[::10].tolist()], every=10)
            print(f'  -> final {final:.3f} bits/pair (entropy {n}), area {area:.3e}', flush=True)
            json.dump(out, open(os.path.join(DATA, f'ours_order_k{k}_s{steps}' + (f'_n{sizes[0]}_seed{seed}' if seed else '') + '.json'), 'w'))
    return out


if __name__ == '__main__':
    os.makedirs(DATA, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else 'rules'
    kw = dict(a.split('=') for a in sys.argv[2:])
    kw = {k: int(v) for k, v in kw.items()}
    {'rules': run_rules, 'order': run_order}[what](**kw)
