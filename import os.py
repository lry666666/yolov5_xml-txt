iimport os
import xml.etree.ElementTree as ET
import io
import shutil

class Voc_Yolo(object):
    def __init__(self, input_root, output_root, class_map):
        self.input_root = input_root
        self.output_root = output_root
        self.class_map = class_map  # 类别映射字典

    def Make_txt(self, outfile):
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        out = open(outfile, 'w')
        print("Created: {}".format(outfile))
        return out

    def delete_xml_files(self):
        # 计数器
        deleted_count = 0
        
        # 遍历文件夹及其子文件夹
        for root, dirs, files in os.walk(self.output_root):
            for file in files:
                # 检查文件是否为XML格式
                if file.lower().endswith('.xml'):
                    try:
                        # 构建完整的文件路径
                        file_path = os.path.join(root, file)
                        # 删除文件
                        os.remove(file_path)
                        deleted_count += 1
                        print(f'已删除: {file_path}')
                    except Exception as e:
                        print(f'删除失败: {file_path}, 错误: {str(e)}')
        
        print(f'\n删除完成，共删除 {deleted_count} 个XML文件')

    def Work(self):
        count = 0
        # 遍历输入目录
        for root, dirs, files in os.walk(self.input_root):
            # 获取相对路径
            rel_path = os.path.relpath(root, self.input_root)
            
            for file in files:
                if not file.lower().endswith('.xml'):
                    # 如果不是xml文件，直接复制到目标目录
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(self.output_root, rel_path, file)
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    continue
                    
                count += 1
                # 构建输入和输出路径，保持文件名相同
                input_file = os.path.join(root, file)
                output_dir = os.path.join(self.output_root, rel_path)
                outfile = os.path.join(output_dir, file[:-4] + '.txt')

                try:
                    # 解析XML
                    tree = ET.parse(input_file)
                    xml_root = tree.getroot()
                    size = xml_root.find('size')
                    
                    if size is None:
                        print(f"Warning: No size information in {input_file}")
                        continue
                        
                    w_image = float(size.find('width').text)
                    h_image = float(size.find('height').text)

                    # 创建输出文件
                    out = self.Make_txt(outfile)

                    # 处理每个对象
                    for obj in xml_root.iter('object'):
                        classname = obj.find('name').text
                        # 使用类别映射获取对应的序号
                        cls_id = self.class_map.get(classname)
                        if cls_id is None:
                            print(f"Warning: Class {classname} not found in mapping")
                            continue
                            
                        xmlbox = obj.find('bndbox')
                        x_min = float(xmlbox.find('xmin').text)
                        y_min = float(xmlbox.find('ymin').text)
                        x_max = float(xmlbox.find('xmax').text)
                        y_max = float(xmlbox.find('ymax').text)

                        # 计算YOLO格式坐标
                        x_center = ((x_min + x_max) / 2) / w_image
                        y_center = ((y_min + y_max) / 2) / h_image
                        w = (x_max - x_min) / w_image
                        h = (y_max - y_min) / h_image

                        # 写入文件，使用数字类别ID
                        out.write(f"{cls_id} {x_center} {y_center} {w} {h}\n")
                    
                    out.close()
                    
                except Exception as e:
                    print(f"Error processing {input_file}: {str(e)}")
                    continue

        return count

def create_class_mapping():
    class_map = {}
    print("请输入类别映射，格式为 '序号.类别名称'（每行一个，输入空行结束）：")
    print("例如：")
    print("1.可回收垃圾")
    print("2.其他垃圾")
    
    while True:
        line = input().strip()
        if not line:  # 如果输入空行，结束输入
            break
        try:
            number, name = line.split('.')
            class_map[name.strip()] = int(number.strip()) - 1  # 转换为从0开始的索引
        except:
            print("格式错误，请使用正确的格式：'序号.类别名称'")
    
    return class_map

if __name__ == "__main__":
    input_root = "C:/Users/lenovo/Desktop/空白数据集"      # 输入目录
    output_root = "C:/Users/lenovo/Desktop/空白数据集"     # 输出目录
    
    # 创建类别映射
    class_map = create_class_mapping()
    if not class_map:
        print("未设置类别映射，程序退出")
        exit()
        
    print("\n使用的类别映射：")
    for name, idx in class_map.items():
        print(f"{idx+1}.{name}")
    
    # 确认是否继续
    confirm = input("\n是否继续处理文件？(y/n): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        exit()
    
    # 处理文件
    converter = Voc_Yolo(input_root, output_root, class_map)
    processed_files = converter.Work()
    print(f"转换完成，共处理 {processed_files} 个文件")
    
    # 确认是否删除XML文件
    confirm = input("\n是否删除所有XML文件？(y/n): ")
    if confirm.lower() == 'y':
        converter.delete_xml_files()
    else:
        print("保留XML文件")