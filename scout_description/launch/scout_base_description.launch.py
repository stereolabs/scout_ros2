import launch
import launch_ros
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch.substitutions import Command


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='false',
                                             description='Use simulation clock if true')

    model_name_arg = DeclareLaunchArgument('model_name', default_value='scout_mini.xacro',
                                           description='The xarco filename of the robot model.')

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution(
            [FindPackageShare("scout_description"), "urdf",
             launch.substitutions.LaunchConfiguration('model_name')]
        ),
    ])

    return launch.LaunchDescription([
        use_sim_time_arg,
        model_name_arg,
        launch.actions.LogInfo(msg='use_sim_time: '),
        launch.actions.LogInfo(
            msg=launch.substitutions.LaunchConfiguration('use_sim_time')),

        launch_ros.actions.Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': launch.substitutions.LaunchConfiguration('use_sim_time'),
                'robot_description': robot_description_content
            }]),

        #launch_ros.actions.Node(
        #    package='joint_state_publisher',
        #    executable='joint_state_publisher',
        #    name='joint_state_publisher')
    ])
