import cv2
import os
from natsort import natsorted

# 设置参数
image_folder = 'data\\original_data\\uav0000140_01590_v'            # 图像序列所在的文件夹
video_output_path = 'data\\original_data\\output.mp4'   # 输出视频路径
fps = 10                           # 帧率（可以根据你的帧时间间隔调整）

# 获取所有图像文件名（按数字自然排序）
images = [img for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png'))]
images = natsorted(images)  # 使用自然排序，例如 frame1.jpg, frame2.jpg, ...

# 读取第一张图像获取尺寸
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape

# 定义视频编码器和输出对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 也可用 'XVID'
video = cv2.VideoWriter(video_output_path, fourcc, fps, (width, height))

# 将每一帧写入视频
for image_name in images:
    img_path = os.path.join(image_folder, image_name)
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"Warning: Skipped {image_name}")
        continue
    video.write(frame)

video.release()
print(f"✅ 视频保存成功: {video_output_path}")
