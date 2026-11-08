import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('turtle_adv'), 'config', 'follow_params.yaml')

    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),

        Node(package='turtle_adv', executable='pose_broadcaster',
             name='broadcaster1', parameters=[{'turtlename': 'turtle1'}]),

        Node(package='turtle_adv', executable='pose_broadcaster',
             name='broadcaster2', parameters=[{'turtlename': 'turtle2'}]),

                Node(package='turtle_adv', executable='turtle_follower',
             name='turtle_follower', parameters=[config]),
    ])