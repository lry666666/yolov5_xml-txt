import xml.etree.ElementTree as ET
import os, cv2
import numpy as np
from os import listdir
from os.path import join

classes = []

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xmlpath, xmlname, imgpath, txtpath, postfix):
    with open(xmlpath, "r", encoding='utf-8') as in_file:
        txtname = xmlname[:-4] + '.txt'
        txtfile = os.path.join(txtpath, txtname)
        tree = ET.parse(in_file)
        root = tree.getroot()
        filename = root.find('filename')
        img = cv2.imdecode(np.fromfile('{}/{}.{}'.format(imgpath, xmlname[:-4], postfix), np.uint8), cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        res = []
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                classes.append(cls)
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            res.append(str(cls_id) + " " + " ".join([str(a) for a in bb]))
        if len(res) != 0:
            with open(txtfile, 'w+') as f:
                f.write('\n'.join(res))

if __name__ == "__main__":
    print("YOLO XML转TXT转换工具")
    print("--------------------------")
    
    # 从用户获取输入路径
    imgpath = input("请输入图片目录路径: ").strip()
    xmlpath = input("请输入XML文件目录路径: ").strip()
    txtpath = input("请输入TXT输出目录路径: ").strip()
    postfix = input("请输入图片文件扩展名（默认: jpg）: ").strip() or "jpg"
    
    # 如果输出目录不存在，则创建
    if not os.path.exists(txtpath):
        os.makedirs(txtpath, exist_ok=True)
        
    # 验证路径
    if not os.path.exists(imgpath):
        print(f"错误: 图片路径 '{imgpath}' 不存在。")
        exit(1)
    
    if not os.path.exists(xmlpath):
        print(f"错误: XML路径 '{xmlpath}' 不存在。")
        exit(1)
        
    # 处理文件
    list_files = os.listdir(xmlpath)
    error_file_list = []
    
    print(f"\n正在处理 {len([f for f in list_files if f.lower().endswith('.xml')])} 个XML文件...")
    
    for i in range(0, len(list_files)):
        try:
            path = os.path.join(xmlpath, list_files[i])
            if ('.xml' in path.lower()):
                convert_annotation(path, list_files[i], imgpath, txtpath, postfix)
                print(f'文件 {list_files[i]} 转换成功。')
            else:
                continue  # 静默跳过非XML文件
        except Exception as e:
            print(f'文件 {list_files[i]} 转换错误。')
            print(f'错误信息:\n{e}')
            error_file_list.append(list_files[i])
    
    print("\n转换完成！")
    if error_file_list:
        print(f'\n转换失败的文件 ({len(error_file_list)}):\n{error_file_list}')
    print(f'\n数据集类别: {classes}')