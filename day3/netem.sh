#!/bin/bash
# 노트북1(보내는 쪽)의 와이파이 인터페이스에 지연·손실을 걸고 푸는 스크립트
# 사용법: ./netem.sh on | off | show
IF=wlo1

case "$1" in
  on)   sudo tc qdisc add dev $IF root netem delay 100ms 20ms loss 5% ;;
  off)  sudo tc qdisc del dev $IF root ;;
  show) tc qdisc show dev $IF ;;
  *)    echo "usage: $0 on|off|show"; exit 1 ;;
esac
