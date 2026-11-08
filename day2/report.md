# 3D nav 2일차 보고서
#### 예비단원 예희원

## 과제 1
+ 기본 내비게이션 실행 <br>
 ```bash
 ~/nav2_edu_ws/scripts/lab1_basic.sh
 ```
+ RViz 상단에 2D Pose Estimate를 누르고 로봇의 위치를 지정한다.
+ Nav2 Goal로 목표 지점을 찍으면 로봇이 이동한다(드래그하면 로봇이 바라보는 방향도 정할 수 있다.)
+ ![](lab1.png)
+ Nav2 Goal 로 도착 지점을 설정하면 로봇의 이동 경로가 생성되고 가제보에서 로봇이 도착 지점으로 이동한는 것을 확인할 수 있다.

## 과제2
+ SLAM : 지도 만들기
+ 초기 맵없는 RViz 실행 명령어  
 ```bash
 ~/nav2_edu_ws/scripts/lab2_slam.sh
 ```
+ slam_toolbox가 지도를 실시간으로 만든다.  
+ ![](lab2_1.png)
+ Nav2 Goal로 돌아다니면서 미탐색 영역을 찍거나 키보드로 운전하면서 맵을 업데이트 할 수 있다.  
+ ![](lab2_2.png)
+ ![](lab2_3.png)
+ 탐색을 완료하고 생성된 지도를 저장할 수 있다.
 ```bash
 source /opt/ros/jazzy/setup.bash && source ~/nav2_edu_ws/scripts/edu_env.sh
ros2 run nav2_map_server map_saver_cli -f ~/nav2_edu_ws/maps/my_map
 ```
+ 저장된 맵은 my_map.yaml과 my_map.pgm으로 생긴다.

## 과제3
+ 파라미터 튜닝
+ 과제 3 실행 명령어
 ``` bash
 /home/heewon-ye/nav2_edu_ws/maps/my_map.yaml
 ```
+ inflation_radius 0.3
+ ![](lab3_IR_0.3.png)
+ inflation_radius 0.7
+ ![](lab3_IR_0.7.png)
+ inflation_radius 1.0
+ ![](lab3_IR_1.0.png)
+ MPPI 주행
+ ![](lab3_MPPI.png)
+ MPPI 로그에서는 오류가 한번도 발생하지 않는다.
+ RPP 주행 ()
+ ![](lab3_RPP.png)
+ RPP 로그
+ ![](lab3_error1.png)![](lab3_error2.png)
+ looke_ahead_dist를 1.0, disired_linear_vel을 0.5로 설정했다.  
  RegulatedPurePursuitController detected collision ahead! 경고와 [ERROR] Controller patience exceeded가 발생한 것을 볼 수 있고 총 2번 발생했다.

## 과제4
+ python으로 웨이포인트 순회하기
```bash
# 터미널 1
~/nav2_edu_ws/scripts/lab1_basic.sh
# 터미널 2 (lab1이 다 뜬 뒤)
source /opt/ros/jazzy/setup.bash
python3 ~/nav2_edu_ws/scripts/lab4_commander.py
```
+ (-2.0, -0.5, 0), (0.5, -1.5), (1.8, 0.0), (0.5, 1.8)로 이동
+ ![](lab4_1.png)![](lab4_2.png)![](lab4_3.png)![](lab4_log1.png)
+ python 파일 수정해서 (-2.0, -0.5, 0), (1.8, -0.6), (0.0, 1.75), (-1.5, -1.5)로 이동
+ ![](lab4_4.png)![](lab4_5.png)![](lab4_6.png)![](lab4_log2.png)

## 과제5
+ STVL   
+ 초기 실행 명령어
```bash
~/nav2_edu_ws/scripts/lab5_stvl.sh
```
+ ![](lab5_1.png)![](lab5_2.png)
+ yaml 파일에서 voxel delay를 조절해 장애물을 치웠을 때 맵에서 사라지는데 걸리는 시간을 조절할 수 있다.