import os
import cv2
import numpy as np
from tqdm import tqdm
from pathlib import Path

def convert_to_deepsort_dataset(image_folder, label_file, output_folder):
    """
    将VisDrone格式的数据集转换为DeepSORT训练所需的格式
    
    参数:
    image_folder: 包含连续帧图片的文件夹
    label_file: 对应的标签txt文件
    output_folder: 输出数据集的根目录
    """
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)
    
    # 读取标签文件
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    # 按帧号分组
    frame_data = {}
    for line in lines:
        parts = line.strip().split(',')
        frame_id = int(parts[0])
        track_id = int(parts[1])
        x = int(float(parts[2]))  # 左上角x坐标
        y = int(float(parts[3]))  # 左上角y坐标
        w = int(float(parts[4]))  # 宽度
        h = int(float(parts[5]))  # 高度
        class_id = int(parts[6])  # 类别ID
        
        # 只处理车辆类别(假设类别ID为1)
        if class_id != 1:
            continue
            
        if frame_id not in frame_data:
            frame_data[frame_id] = []
            
        frame_data[frame_id].append({
            'track_id': track_id,
            'bbox': (x, y, w, h)
        })
    
    # 处理每一帧
    for frame_id, detections in tqdm(frame_data.items(), desc="Processing frames"):
        # 构建图像路径
        image_path = os.path.join(image_folder, f"{frame_id:07d}.jpg")  # 假设图像格式为0000001.jpg
        
        # 检查图像是否存在
        if not os.path.exists(image_path):
            print(f"Warning: Image {image_path} not found, skipping frame {frame_id}")
            continue
            
        # 读取图像
        img = cv2.imread(image_path)
        
        # 裁剪每个检测框并保存
        for det in detections:
            track_id = det['track_id']
            x, y, w, h = det['bbox']
            
            # 确保边界框有效
            if x < 0: x = 0
            if y < 0: y = 0
            if x + w > img.shape[1]: w = img.shape[1] - x
            if y + h > img.shape[0]: h = img.shape[0] - y
            
            if w <= 0 or h <= 0:
                continue
                
            # 裁剪图像
            crop = img[y:y+h, x:x+w]
            
            # 创建ID对应的文件夹
            id_folder = os.path.join(output_folder, f"{track_id:04d}")
            os.makedirs(id_folder, exist_ok=True)
            
            # 保存裁剪的图像
            crop_path = os.path.join(id_folder, f"{frame_id:07d}_{track_id:04d}.jpg")
            cv2.imwrite(crop_path, crop)
    
    print(f"数据集转换完成，输出路径: {output_folder}")

# 使用示例
if __name__ == "__main__":
    image_folder = "data\\original_data\\uav0000140_01590_v"  # 连续帧图片文件夹
    label_file = "data\\original_data\\uav0000140_01590_v.txt"  # 标签文件
    output_folder = "data\\new_data"  # 输出数据集路径
    
    convert_to_deepsort_dataset(image_folder, label_file, output_folder)