#!/bin/bash
# waits for the short sweeps, then runs the long rules run and the order experiment (our runs)
cd "$(dirname "$0")"
PY=../../../.pixi/envs/default/bin/python
while pgrep -f "eca_lab.py rules n=32 k=" >/dev/null; do sleep 5; done
$PY eca_lab.py rules n=32 k=16 steps=20000 > ${LOGDIR:-/tmp}/lab_long.log 2>&1 &
$PY eca_lab.py order k=8 steps=4000 > ${LOGDIR:-/tmp}/lab_order.log 2>&1 &
wait
