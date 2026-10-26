"""Command line: python -m aiglainer <command> [-p PROJECT] [--cut narrated|full] ...

Also installed as the `aiglainer` command. `tts`, `verify` and `voices` need the `tts` extra (included by tools/setup.sh).
"""
import argparse, os, sys

COMMANDS = {
    'new':       'scaffold projects/<name> from the template',
    'inspect':   'list a PDF page\'s vector paths and images, to find figure data to extract',
    'tex':       'typeset eqs.py into tex/*.png (skipped when unchanged)',
    'tts':       'synthesize narration lines (cached) and Whisper-check each one',
    'plan':      'print the narrated timing plan',
    'render':    'render frames to out/<cut>/video_noaudio.mp4',
    'audio':     'score + sound effects + narration -> out/<cut>/audio.wav',
    'finish':    'mux at -14 LUFS, write captions.srt and youtube_description.txt',
    'verify':    'Whisper the final mix line by line',
    'frames':    'contact sheets with one frame per narration line -> out/<cut>/qa/',
    'preview':   'contact sheet of one scene: preview SCENE t1 t2 ...',
    'thumbnail': '1280x720 YouTube thumbnail -> out/thumbnail.png',
    'voices':    'audition Kokoro voices on a line -> voice_samples/index.html',
    'fingerprint': 'hash sampled frames/cues/placements; --compare after an engine change',
}

def main(argv=None):
    ap = argparse.ArgumentParser(prog='python -m aiglainer', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='\n'.join(f'  {k:12s} {v}' for k, v in COMMANDS.items()))
    ap.add_argument('command', choices=COMMANDS, metavar='command')
    ap.add_argument('args', nargs='*')
    ap.add_argument('-p', '--project', default=os.environ.get('AIGLAINER_PROJECT'))
    ap.add_argument('--cut', default='narrated', choices=['narrated', 'full'])
    ap.add_argument('--force', action='store_true', help='tex: rebuild even if unchanged')
    ap.add_argument('--compare', action='store_true', help='fingerprint: compare against the saved one')
    a = ap.parse_args(argv)
    if a.command == 'new':
        from . import scaffold
        return scaffold.main(*a.args)
    if a.command == 'inspect':
        from . import pdf
        return pdf.inspect(*a.args)
    if a.project:
        os.environ['AIGLAINER_PROJECT'] = a.project    # inherited by render workers
    from . import project
    project.get()
    c = a.command
    if c == 'tex':
        from . import build_tex; build_tex.main(a.force)
    elif c == 'tts':
        from . import tts; tts.main()
    elif c == 'plan':
        from . import narrated; narrated.plan()
    elif c == 'render':
        from . import render; render.main(a.cut, [int(x) for x in a.args])
    elif c == 'audio':
        from . import audio; audio.main(a.cut)
    elif c == 'finish':
        from . import finish; finish.main(a.cut)
    elif c == 'verify':
        from . import verify_mix; verify_mix.main(a.cut)
    elif c == 'frames':
        from . import line_frames; line_frames.main(a.cut)
    elif c == 'preview':
        from . import preview; preview.main(a.args[0], [float(x) for x in a.args[1:]])
    elif c == 'thumbnail':
        from . import thumbnail; thumbnail.main(*a.args)
    elif c == 'voices':
        from . import voices; voices.main(*a.args)
    elif c == 'fingerprint':
        from . import fingerprint; fingerprint.main(a.compare)

if __name__ == '__main__':
    sys.exit(main())
