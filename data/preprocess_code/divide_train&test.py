import os
import random
import shutil
from tqdm import tqdm

def split_dataset_by_id(input_dir, output_dir, test_ratio=0.2, seed=42):
    """
    按ID将数据集划分为训练集和测试集，确保同一ID的所有图像在同一集合中
    
    参数:
    input_dir: 输入数据集目录，格式为 input_dir/ID/图像.jpg
    output_dir: 输出目录，将创建 train/ 和 test/ 子目录
    test_ratio: 测试集ID占比，默认0.2
    seed: 随机种子，保证结果可复现
    """
    # 设置随机种子
    random.seed(seed)
    
    # 创建输出目录
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # 获取所有ID目录
    id_list = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    print(f"找到 {len(id_list)} 个ID")
    
    # 随机打乱ID列表
    random.shuffle(id_list)
    
    # 计算测试集ID数量
    test_size = int(len(id_list) * test_ratio)
    
    # 划分ID
    test_ids = id_list[:test_size]
    train_ids = id_list[test_size:]
    
    print(f"训练集ID数量: {len(train_ids)}")
    print(f"测试集ID数量: {len(test_ids)}")
    
    # 复制训练集ID的所有图像
    print("复制训练集数据...")
    for id_name in tqdm(train_ids):
        src_id_dir = os.path.join(input_dir, id_name)
        dst_id_dir = os.path.join(train_dir, id_name)
        shutil.copytree(src_id_dir, dst_id_dir)
    
    # 复制测试集ID的所有图像
    print("复制测试集数据...")
    for id_name in tqdm(test_ids):
        src_id_dir = os.path.join(input_dir, id_name)
        dst_id_dir = os.path.join(test_dir, id_name)
        shutil.copytree(src_id_dir, dst_id_dir)
    
    print(f"数据集划分完成！")
    print(f"训练集路径: {train_dir}")
    print(f"测试集路径: {test_dir}")

# 使用示例
if __name__ == "__main__":
    input_dataset = "data\\new_data"  # 输入数据集路径
    output_dataset = "data\\dataset"       # 输出数据集路径
    test_ratio = 0.2                        # 测试集ID占比
    
    split_dataset_by_id(input_dataset, output_dataset, test_ratio)