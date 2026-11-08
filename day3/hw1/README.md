# 과제1 보고서

```bash
# 키보드로 turtle1을 조종하는 명령어
ros2 run turtlesim turtle_teleop_key
# turtle1이 turtle2 기준으로 어느 방향에 있는지 1초마다 출력하는 명령어
ros2 run tf2_ros tf2_echo turtle2 turtle1
# TF 트리를 PDF로 저장한느 명려어(home에 저장됨)
ros2 run tf2_tools view_frames
```

+ 과제 1-1[![과제1-1](https://drive.google.com/thumbnail?id=1Hr4SR2O1x5eNtg0hdS_YzfOvqGNds7G8&sz=w640)](https://drive.google.com/file/d/1Hr4SR2O1x5eNtg0hdS_YzfOvqGNds7G8/view?usp=drive_link)
+ 과제 1-2[![실행 영상](https://drive.google.com/thumbnail?id=1ozWDmn0WGFM-FWtanD2hu-G2aAa14SQh&sz=w640)](https://drive.google.com/file/d/1ozWDmn0WGFM-FWtanD2hu-G2aAa14SQh/view?usp=drive_link)
+ 과제 1-2 단독실행[![실행 영상](https://drive.google.com/thumbnail?id=1cQ4wYDwNiCkO9gH0ABEC_bILraOUHGlP&sz=w640)](https://drive.google.com/file/d/1cQ4wYDwNiCkO9gH0ABEC_bILraOUHGlP/view?usp=drive_link)

+ lookup_transform은 A가 본 B의 위치와 방향을 나타낸다.