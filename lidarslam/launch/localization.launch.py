import os

import launch
import launch_ros.actions
from launch.actions import DeclareLaunchArgument          
from launch.substitutions import LaunchConfiguration     
from launch_ros.actions import SetParameter   

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'localization.yaml'))
    
    rviz_param_dir = launch.substitutions.LaunchConfiguration(
        'rviz_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping.rviz'))

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use /clock(simulation time)'
    )

    use_faulty_arg = DeclareLaunchArgument(
        'use_faulty',
        default_value='true',
        description='If true, scanmatcher subscribes /lidar/points_faulty instead of /morai/lidar/points'
    )

    use_ground_filter_arg = DeclareLaunchArgument(
        'use_ground_filter',
        default_value='false',
        description=(
            'If true, scanmatcher subscribes /lidar/no_ground and ignores '
            'use_faulty for its own input, leaving the raw-vs-faulty choice '
            'to whatever publishes that topic. NOTE: the pipeline no longer '
            'ships a ground filter — pointcloud_ground_filter_cpp was '
            'removed on 2026-09-28 because every HG-SCIF experiment ran on '
            'the unfiltered cloud. Setting this true without supplying your '
            'own /lidar/no_ground publisher leaves scanmatcher with no input.'
        )
    )

    set_sim_time = SetParameter(
        name='use_sim_time',
        value=LaunchConfiguration('use_sim_time')
    )

    # Three-way selection:
    #   use_ground_filter=true  -> /lidar/no_ground   (filter output)
    #   use_ground_filter=false + use_faulty=true  -> /lidar/points_faulty
    #   use_ground_filter=false + use_faulty=false -> /morai/lidar/points
    cloud_topic = launch.substitutions.PythonExpression([
        "'/lidar/no_ground' if '", LaunchConfiguration('use_ground_filter'),
        "'.lower() == 'true' else (",
        "'/lidar/points_faulty' if '", LaunchConfiguration('use_faulty'),
        "'.lower() == 'true' else '/morai/lidar/points')"
    ])

    localization = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud', cloud_topic)],
        output='screen'
        )


    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Spawn rviz2. Set false for headless bag-replay batches.')

    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_param_dir],
        condition=launch.conditions.IfCondition(
            launch.substitutions.LaunchConfiguration('use_rviz'))
        )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        use_sim_time_arg,
        use_faulty_arg,
        use_ground_filter_arg,
        use_rviz_arg,
        set_sim_time,
        localization,
        rviz,
            ])