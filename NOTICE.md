# Project Notice

This repository (`multimode_lidarslam`) is a **standalone modified copy** of
[`rsasaki0109/lidarslam_ros2`](https://github.com/rsasaki0109/lidarslam_ros2)
adapted for the fault-tolerant LiDAR-Visual-GNSS multimodal localization
pipeline ([`fault-tolerant-localization-pipeline`](https://github.com/jeonseoknam/fault-tolerant-localization-pipeline)).

## Upstream

- Source: https://github.com/rsasaki0109/lidarslam_ros2
- Branch: `develop`
- License: BSD 2-Clause (see `LICENSE`)
- Original copyright: © 2020 Ryohei Sasaki, all rights reserved

## Modifications in this fork

- MORAI simulator integration parameters (`localization.yaml`, `mapping.rviz`)
- Dynamic object filtering (`graph_based_slam/include/.../dynamic_object_filter.hpp`)
- GNSS weighting in graph-based SLAM
- BEV / scan-context / SOLID descriptors for loop closure
- Fault-injection topic plumbing (`/lidar/points_faulty`)
- Localization launch arguments (`use_faulty`, `use_sim_time`)

The original `LICENSE` and copyright notices are preserved.
