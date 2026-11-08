# ROS 2 미들웨어 Day 2 주말 과제 — 지연과 손실

- 이름: 예희원
- 주제: 지연과 손실 (netem으로 지연·손실을 걸고 RTT 평균, p95, 손실 측정)

## 1. 질문

손실이 있는 와이파이에서 QoS reliability를 reliable로 할 때와 best_effort로 할 때, 손실과 지연(RTT p95)은 각각 어떻게 달라지는가?

## 2. 예상

실험 전에 이렇게 예상했다.

- 지연을 걸면 두 설정 모두 메시지가 돌아오는 시간(RTT)이 늘어날 것이다.
- **reliable**: 빠진 메시지를 다시 보내 주므로 손실은 거의 없을 것이다. 대신 다시 보내는 시간 때문에 지연이 약간 더 늘어날 것이다.
- **best_effort**: 빠진 메시지를 다시 보내지 않으므로 손실이 생길 것이다. 대신 지연은 reliable보다 작을 것이다.

## 3. 방법

### 환경

| 항목 | 내용 |
|---|---|
| PC | 노트북 2대. 노트북1(보내는 쪽, ping, netem 적용), 노트북2(되돌려 주는 쪽, pong) |
| ROS | 두 노트북 모두 ROS 2 Jazzy, RMW 기본값(Fast DDS, 별도 설정 파일 없음) |
| 네트워크 | 같은 와이파이 `ROBIT_5G`, 5GHz 채널 100, 폭 80MHz |
| 발견 | 멀티캐스트 정상(`ros2 multicast send/receive` 확인), Peers 설정 없음 |
| 도메인 | `ROS_DOMAIN_ID=5` |
| 와이파이 절전 | 두 노트북 모두 켜짐(노트북1 `iw dev wlo1 get power_save` → on, 노트북2 `wifi.powersave = 3`, 설정 파일 기준). 바꾸지 않고 측정 |

### 측정 방법

- 수업 자료의 ping/pong 코드로 RTT를 쟀다. ping이 번호와 보낸 시각을 실어 보내고, pong이 그대로 되돌려 주면 ping이 자기 시계로 뺀다. 한쪽 시계만 쓰므로 두 PC의 시계 차이와 상관없다.
- 한 번 실행에 200개를 10Hz로 보낸다. 손실은 돌아오지 않은 번호의 비율이고, 평균과 p95를 함께 출력한다.
- 원래 코드에서 한 가지를 바꿨다. **시작 후 2초 동안은 보내지 않는다.** PC 1대로 연습할 때 아무 조건 없이도 손실이 2% 나왔는데, 발견·매칭이 끝나기 전에 보낸 앞쪽 메시지가 빠진 것으로 보였기 때문이다.
- reliable은 `ping.py` + `pong.py`, best_effort는 `ping_be.py` + `pong_be.py`로 짝을 맞춰 실행했다. 두 파일은 QoS(reliability)만 다르고 depth는 10으로 같다.
- 조건마다 3번씩 측정했다.

### 실행한 명령

```bash
# 노트북2 (먼저 실행)
ROS_DOMAIN_ID=5 python3 pong.py        # best_effort일 때는 pong_be.py

# 노트북1
ROS_DOMAIN_ID=5 python3 ping.py        # best_effort일 때는 ping_be.py

# 노트북1: 지연·손실 걸기 → 확인 → 해제 → 확인
sudo tc qdisc add dev wlo1 root netem delay 100ms 20ms loss 5%
tc qdisc show dev wlo1      # qdisc netem 8004: root refcnt 2 limit 1000 delay 100ms  20ms loss 5%
sudo tc qdisc del dev wlo1 root
tc qdisc show dev wlo1      # qdisc noqueue 0: root refcnt 2
```

## 4. 증거

### 측정 결과 (조건별 3회)

| 조건 | QoS | 회차 | loss | mean | p95 |
|---|---|---|---|---|---|
| netem 없음 | reliable | 1 | 0.0% | 6.3ms | 10.5ms |
| | | 2 | 0.0% | 8.4ms | 13.1ms |
| | | 3 | 0.0% | 27.8ms | 146.2ms |
| netem 없음 | best_effort | 1 | 2.5% | 18.6ms | 90.6ms |
| | | 2 | 0.0% | 5.0ms | 8.8ms |
| | | 3 | 0.0% | 7.5ms | 9.1ms |
| netem 켜짐 | best_effort | 1 | 15.5% | 114.7ms | 177.8ms |
| | | 2 | 8.5% | 115.7ms | 183.0ms |
| | | 3 | 2.5% | 128.0ms | 211.0ms |
| netem 켜짐 | reliable | 1 | 1.0% | 204.8ms | 699.7ms |
| | | 2 | 0.5% | 227.2ms | 746.7ms |
| | | 3 | 1.0% | 358.9ms | 1109.7ms |

### 조건별 평균 (3회 평균)

| 조건 | QoS | loss | mean | p95 |
|---|---|---|---|---|
| netem 없음 | reliable | 0.0% | 14.2ms | 56.6ms |
| netem 없음 | best_effort | 0.8% | 10.4ms | 36.2ms |
| netem 켜짐 | best_effort | 8.8% | 119.5ms | 190.6ms |
| netem 켜짐 | reliable | 0.8% | 263.6ms | 852.0ms |

netem 없음의 평균은 튄 회차 하나에 끌려 올라갔다(reliable 3회차, best_effort 1회차). 평소 수준을 보려고 3회 중 가운데 값을 보면 reliable mean 8.4ms, best_effort mean 7.5ms다.

## 5. 결론

**손실이 있는 와이파이에서 reliable은 손실을 줄이는 대신 지연을 크게 늘렸고, best_effort는 지연이 건 만큼만 늘어나는 대신 손실을 그대로 드러냈다.**

- 같은 netem 조건에서 reliable의 손실은 0.8%로, best_effort(8.8%)의 약 10분의 1이었다. 대신 p95는 852.0ms로 best_effort(190.6ms)의 약 4.5배였고, 한 번은 1.1초를 넘었다. 재전송을 기다리는 시간이 더해진 결과다.
- best_effort의 mean은 3회 중 가운데 값 기준으로 netem 전 7.5ms에서 netem 후 115.7ms로 약 108ms 늘었다. netem은 노트북1에서 나가는 패킷에만 걸리므로, 가는 길에만 100ms ± 20ms가 더해지고 돌아오는 길에는 지연이 없다는 설명과 맞는다.
- 수업 자료의 "명령은 조금 늦어도 다 도착해야 한다(reliable)", "센서는 늦은 옛 값보다 최신 값이 낫다(best_effort)"는 선택이 숫자로 확인됐다. 정지 명령처럼 빠지면 안 되는 데이터라도, 손실이 많은 링크에서는 p95가 1초 가까이 늦을 수 있다는 점을 설계할 때 고려해야 한다.
- **평균보다 p95를 봐야 하는 이유도 확인했다.** netem을 걸지 않았는데도 reliable 3회차는 mean이 27.8ms로 조금 늘어난 정도였지만 p95는 146.2ms였다. 가끔 생기는 큰 지연은 평균보다 p95에서 훨씬 잘 드러났다.

### 예상과 달랐던 점

1. **reliable의 지연이 예상보다 훨씬 많이 늘었다.** 재전송 때문에 약간 늘어날 거라고 생각했는데, p95가 best_effort의 약 4.5배(852ms)였고 한 번은 1.1초를 넘었다. 손실 5%, 지연 100ms 조건에서 재전송 대기가 이렇게 커질 수 있었다.
2. **best_effort 손실이 설정한 5%보다 많았고 회차마다 크게 달랐다.** 2.5%, 8.5%, 15.5%로 평균 8.8%였다. netem 5%에 실제 와이파이 손실이 더해졌을 수 있다.
3. **reliable인데도 손실이 0%가 아니었다.** 0.5~1%(200개 중 1~2개)가 빠졌다.
4. **netem 없이도 와이파이 자체가 가끔 튀었다.** reliable 3회차 p95 146ms, best_effort 1회차는 손실 2.5%와 p95 90.6ms. 두 노트북 모두 와이파이 절전 모드가 켜져 있었는데, 수업 자료의 '와이파이의 함정'에 절전 모드는 가끔 수백 ms 튄다고 나와 있다.

## 6. 아직 모르는 것

- best_effort 손실이 5%보다 컸던 이유와 reliable에 손실이 남은 이유를 확실히 모른다. 가설은 두 가지다.
  - **매칭 전 손실**: netem이 발견 패킷도 늦추고 버려서, 2초 대기로는 매칭이 다 끝나지 않았고 앞쪽 메시지가 빠졌다.
  - **늦은 답장**: reliable은 p95가 1초를 넘은 회차도 있었으니, 가장 늦은 답장은 결과를 출력하기 전 2초 대기보다도 늦게 도착해 손실로 잡혔다.
  - 확인 방법: 빠진 번호를 출력해서 앞쪽에 몰렸는지 보고, 결과 출력 뒤에도 몇 초 더 기다리며 늦게 온 번호를 센다.
- 와이파이 튐이 절전 모드 때문인지는 절전을 끄고 다시 재 봐야 알 수 있다.

## 7. 실패한 시도

| 시도 | 결과 | 원인과 해결 |
|---|---|---|
| PC 1대에서 `lo`에 netem(100ms, 5%)을 걸고 측정 | RTT가 1.4ms에서 1.7ms로 거의 그대로, 손실만 0%에서 4%로 늘어남 | 같은 PC 안에서는 Fast DDS가 공유메모리로 데이터를 보내 `lo`(netem)를 거치지 않는 것으로 추정. 그래서 노트북 2대로 다시 실험했다 |
| PC 1대에서 `wlo1`에 netem을 걸고 측정하려 함 | 의미 없음 | 같은 PC 안의 통신은 와이파이 인터페이스를 지나지 않는다 |
| `ROS_DOMAIN_ID` 없이 `ping.py` 실행 | `no reply` | pong은 도메인 5, ping은 기본 도메인 0이라 서로 발견하지 못함 |
| ping만 best_effort로 바꾸고 pong은 reliable로 실행 | `incompatible QoS ... RELIABILITY` 경고, `no reply` | 구독자가 요청한 reliable을 발행자(best_effort)가 제공하지 못해 매칭 실패(제공 ≥ 요청 규칙). 4곳을 모두 바꿔 해결 |
| 노트북2의 `pong.py`로 reliable 측정 | 같은 `incompatible QoS` 경고 | 노트북2의 `pong.py`가 예전에 best_effort로 고쳐 둔 파일이었다. reliable 원본으로 되돌려 해결 |
| `netem dely`, `QosProfile`, 들여쓰기 | 각각 명령 오류, `NameError`, `IndentationError` | 오타(`delay`, `QoSProfile`)와 들여쓰기 수정 |