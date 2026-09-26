// Mapping front-end entry point.
//
// The localization front-end is scanmatcher_node, which matches scans against a
// prior .pcd map. This one builds that map in the first place: it starts from an
// empty map, accumulates submaps as the vehicle drives, and publishes /map_array
// for graph_based_slam to optimise with its GNSS position constraints.
//
// Recovered from lidarslam2_ws @ dbf6fd2 (2026-03-30), the tree the K-City maps
// were built with before the front-end was rewritten for localization.
#include "scanmatcher/slam_component.h"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions options;
  options.use_intra_process_comms(true);
  rclcpp::spin(std::make_shared<graphslam::SlamComponent>(options));
  rclcpp::shutdown();
  return 0;
}
