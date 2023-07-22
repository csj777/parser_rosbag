import os
import rosbag
from sensor_msgs.msg import Image, Imu, PointCloud2
from cv_bridge import CvBridge
import cv2
import json

# 定义输入 .bag 文件所在文件夹路径
input_folder = '/space0/imagelab/need_label'

# 定义输出文件夹的根目录
output_folder = 'output_data'
os.makedirs(output_folder, exist_ok=True)

# 初始化 CvBridge
cv_bridge = CvBridge()

# 定义函数用于保存 Image 类型的数据到文件夹中
# def save_image_msg(msg, folder):
#     cv_image = cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
#     file_name = os.path.join(folder, f"{msg.header.stamp}.jpg")
#     cv2.imwrite(file_name, cv_image)
def save_image_msg(msg, folder):
    image = cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    # 创建文件名
    image_file = os.path.join(folder, f"{msg.header.stamp}.png")

    # 保存图像数据到文件
    cv2.imwrite(image_file, image)

    # 创建并保存格式信息到 JSON 文件
    format_info = {
        'height': msg.height,
        'width': msg.width,
        'encoding': msg.encoding,
        'is_bigendian': msg.is_bigendian,
        'step': msg.step,
    }
    json_file = os.path.join(folder, f"{msg.header.stamp}.json")
    with open(json_file, 'w') as f:
        json.dump(format_info, f)

# # 定义函数用于保存 Imu 类型的数据到文件夹中
# def save_imu_msg(msg, folder):
#     file_name = os.path.join(folder, f"{msg.header.stamp}.txt")
#     with open(file_name, 'w') as f:
#         f.write(f"Linear Acceleration: x={msg.linear_acceleration.x}, y={msg.linear_acceleration.y}, z={msg.linear_acceleration.z}\n")
#         f.write(f"Angular Velocity: x={msg.angular_velocity.x}, y={msg.angular_velocity.y}, z={msg.angular_velocity.z}\n")

# # 定义函数用于保存 PointCloud2 类型的数据到文件夹中
# def save_lidar_msg(msg, folder):
#     lidar_data = msg.data
#     file_name = os.path.join(folder, f"{msg.header.stamp}.bin")
#     with open(file_name, 'wb') as f:
#         f.write(lidar_data)

def save_imu_msg(msg, folder):
    imu_data = {
        'header': {
            'seq': msg.header.seq,
            'stamp': {
                'secs': msg.header.stamp.secs,
                'nsecs': msg.header.stamp.nsecs,
            },
            'frame_id': msg.header.frame_id,
        },
        'orientation': {
            'x': msg.orientation.x,
            'y': msg.orientation.y,
            'z': msg.orientation.z,
            'w': msg.orientation.w,
        },
        'orientation_covariance': msg.orientation_covariance,
        'angular_velocity': {
            'x': msg.angular_velocity.x,
            'y': msg.angular_velocity.y,
            'z': msg.angular_velocity.z,
        },
        'angular_velocity_covariance': msg.angular_velocity_covariance,
        'linear_acceleration': {
            'x': msg.linear_acceleration.x,
            'y': msg.linear_acceleration.y,
            'z': msg.linear_acceleration.z,
        },
        'linear_acceleration_covariance': msg.linear_acceleration_covariance,
    }
    file_name = os.path.join(folder, f"{msg.header.stamp}.json")
    with open(file_name, 'w') as f:
        json.dump(imu_data, f)

def save_lidar_msg(msg, folder):
    # 提取 PointCloud2 的元数据
    header = msg.header
    height = msg.height
    width = msg.width
    fields = msg.fields
    is_bigendian = msg.is_bigendian
    point_step = msg.point_step
    row_step = msg.row_step
    data = msg.data

    # 创建文件名
    json_file = os.path.join(folder, f"{header.stamp}.json")
    bin_file = os.path.join(folder, f"{header.stamp}.bin")

    # 保存 PointCloud2 的元数据到 JSON 文件
    metadata = {
        'header': {
            'seq': header.seq,
            'stamp': {
                'secs': header.stamp.secs,
                'nsecs': header.stamp.nsecs,
            },
            'frame_id': header.frame_id,
        },
        'height': height,
        'width': width,
        'fields': [],
        'is_bigendian': is_bigendian,
        'point_step': point_step,
        'row_step': row_step,
    }

    for field in fields:
        metadata['fields'].append({
            'name': field.name,
            'offset': field.offset,
            'datatype': field.datatype,
            'count': field.count,
        })

    with open(json_file, 'w') as f:
        json.dump(metadata, f, indent=4)

    # 保存二进制数据到文件
    with open(bin_file, 'wb') as f:
        f.write(data)


# 遍历 .bag 文件所在文件夹并解析数据
bag_files = [f for f in os.listdir(input_folder) if f.endswith('.bag')]

for bag_file in bag_files:
    bag_path = os.path.join(input_folder, bag_file)
    bag = rosbag.Bag(bag_path)

    for topic, topic_info in bag.get_type_and_topic_info().topics.items():
        topic_fields = topic.strip('/').split('/')
        folder_name = '_'.join(topic_fields)
        folder = os.path.join(output_folder, folder_name)
        os.makedirs(folder, exist_ok=True)

        for _, msg, _ in bag.read_messages(topic):
            if topic_info.msg_type == 'sensor_msgs/Image':
                save_image_msg(msg, folder)
                # pass
            elif topic_info.msg_type == 'sensor_msgs/Imu':
                save_imu_msg(msg, folder)
                # pass
            elif topic_info.msg_type == 'sensor_msgs/PointCloud2':
                save_lidar_msg(msg, folder)
                # pass
            else:
                # Handle other message types if needed
                pass

    bag.close()

print("所有 .bag 文件的数据已成功整理到各个文件夹中。")