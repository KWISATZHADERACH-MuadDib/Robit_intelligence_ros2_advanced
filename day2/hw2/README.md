# 과제2

+과제2[![실행 영상](https://drive.google.com/thumbnail?id=1hikHmoS_vIoSWhtJsYCWgIpnBGn1nWCr&sz=w640)](https://drive.google.com/file/d/1hikHmoS_vIoSWhtJsYCWgIpnBGn1nWCr/view?usp=drive_link)

+ ros2 launch turtle_adv multisim.launch.py를 실행시키면 /sim1/sim, sim2/sim과 mimic 노드가 실행된다.
+ turtlesim.yaml이 sim1에만 적용되어 sim1 배경만 남색으로 바뀐다. 
+ mimic의 입력을 sim1/turtle1/pose, 출력을 /sim2/turtle1/cmd_vel에 연결해서 sim1이 움직이면 sim2가 똑같이 움직인다.
+ ros2 param set /sim2/sim background_r 150 으로 실행중에도 sim2의 배경색이 바로 바뀌었다.