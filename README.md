# 解析 .bag 文件数据
这个项目旨在解析 ROS 的 .bag 文件，并将数据按照消息主题进行保存。在解析过程中，图像数据被保存为 PNG 格式的图像文件，IMU 数据被保存为 JSON 文件，LiDAR 数据被保存为二进制文件，并且每个保存的文件都有对应的格式信息保存为 JSON 文件。以下是项目的结构和数据说明。

## 项目结构
```
├── your_bag_file.bag            # 你使用的原始 .bag 文件
├── output_data                  # 解析后的数据保存文件夹
│   ├── camera_color_image_raw   # 图像消息 '/camera/color/image_raw' 的数据保存文件夹
│   │   ├── image_1.png          # 图像消息 1 的图像数据
│   │   ├── image_1.json         # 图像消息 1 的格式信息
│   │   ├── image_2.png          # 图像消息 2 的图像数据
│   │   ├── image_2.json         # 图像消息 2 的格式信息
│   │   ├── ...                  # 其他图像数据及格式信息
│   ├── ir_image_raw             # 图像消息 '/ir/image_raw' 的数据保存文件夹
│   │   ├── ...
│   ├── livox_imu                # IMU 消息 '/livox/imu' 的数据保存文件夹
│   │   ├── imu_1.json           # IMU 消息 1 的数据和格式信息
│   │   ├── imu_2.json           # IMU 消息 2 的数据和格式信息
│   │   ├── ...                  # 其他 IMU 数据及格式信息
│   ├── livox_lidar              # LiDAR 消息 '/livox/lidar' 的数据保存文件夹
│   │   ├── lidar_1.bin          # LiDAR 消息 1 的二进制数据
│   │   ├── lidar_1.json         # LiDAR 消息 1 的格式信息
│   │   ├── lidar_2.bin          # LiDAR 消息 2 的二进制数据
│   │   ├── lidar_2.json         # LiDAR 消息 2 的格式信息
│   │   ├── ...                  # 其他 LiDAR 数据及格式信息
├── parser.py                    # 解析 .bag 文件的 Python 脚本
├── README.md                    # 项目说明文件
```
## 数据说明
### 图像数据
- 图像数据保存为 PNG 格式的图像文件，对应的格式信息保存为 JSON 文件。图像文件命名规则为 `image_x.png`，对应的格式信息文件命名规则为 `image_x.json`，其中 `x` 为图像消息的序号。JSON 格式信息包含以下字段：
    - `height`: 图像高度
    - `width`: 图像宽度
    - `encoding`: 图像编码方式
    - `is_bigendian`: 是否为 big-endian 编码
    - `step`: 图像每行的字节数
### IMU 数据
- IMU 数据保存为 JSON 文件，格式信息包含在其中。IMU 数据文件命名规则为 `imu_x.json`，其中 x 为 IMU 消息的序号。JSON 格式信息包含以下字段：
    - `header`: 消息头信息，包含序列号、时间戳和坐标系
    - `orientation`: 传感器方向信息
    - `orientation_covariance`: 方向协方差矩阵
    - `angular_velocity`: 角速度信息
    - `angular_velocity_covariance`: 角速度协方差矩阵
    - `linear_acceleration`: 线性加速度信息
    - `linear_acceleration_covariance`: 线性加速度协方差矩阵
### LiDAR 数据
- LiDAR 数据保存为二进制文件，对应的格式信息保存为 JSON 文件。LiDAR 数据文件命名规则为 `lidar_x.bin`，对应的格式信息文件命名规则为 `lidar_x.json`，其中 x 为 LiDAR 消息的序号。JSON 格式信息包含以下字段：

    - `header`: 消息头信息，包含序列号、时间戳和坐标系
    - `height`: 点云数据高度
    - `width`: 点云数据宽度
    - `fields`: 点云数据字段信息
    - `is_bigendian`: 是否为 big-endian 编码
    - `point_step`: 点云数据每个点的字节数
    - `row_step`: 点云数据每行的字节数
### 解析脚本
`parser.py` 是用于解析 .bag 文件并保存数据的 Python 脚本。你可以运行该脚本来执行解析过程，并将数据保存到 `output_data` 文件夹中。 -->

### 使用方法
1. 确保你已经安装了相关依赖库，包括 `rosbag、ros_numpy、std_msgs、sensor_msgs、geometry_msgs、visualization_msgs、actionlib_msgs、nav_msgs、tf2_msgs、cv_bridge `等。

2. 将你想要解析的 .bag 文件放置在项目根目录，并将文件名替换为 `your_bag_file.bag`。

3. 运行 `parser.py` 脚本，将会解析 .bag 文件并保存数据到 `output_data` 文件夹中。

4. 解析完成后，你可以在 `output_data` 文件夹中找到保存的数据和格式信息。 -->
