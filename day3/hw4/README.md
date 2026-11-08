# 과제 4

+ [![과제4](https://drive.google.com/thumbnail?id=18TdvRYjdYhfeWDOJdLfforpeJoECRC_v&sz=w640)](https://drive.google.com/file/d/18TdvRYjdYhfeWDOJdLfforpeJoECRC_v/view?usp=drive_link)

+ 1-2 에서 터미널 4개로 실행하던 노드들(turtlesim_node, pose_broadcaster 2개, turtle_follower)를 follow.launch.py 파일 하나로 실행하고, 따라가기에 관련된 파라미터를 follow_params.yaml으로 분리했다.
+  pose_broadcaster를 broadcaster1, broadcaster2로 이름을 다르게 붙이고, turtlename 파라미터로 각각 turtle1, turtle2의 TF를 발행하게 했다.
+ follow_params.yaml의 최상위 키를 노드 이름(turtle_follower)과 같게 작성하고 get_package_share_directory()로 경로를 구해 parameters=[config]로 전달했다.
+ k_ang는 5.0, k_lin은 0.7로 설정했다.
+ 새 파일을 추가한 것이므로 colcon build를 다시해야 install/에 반영된다.
+ turtle1이 제자리에서 회전하더라도 turtle2가 움직이지는 않는다. 왜냐하면 follower는 TF의 위치만을 사용해 움직이기 때문이다.