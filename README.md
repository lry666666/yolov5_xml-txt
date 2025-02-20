
```markdown
# YOLO XML转TXT标注格式转换工具

一个用于将XML格式的目标检测标注文件转换为YOLO格式TXT文件的Python工具，支持自定义类别顺序。

## 功能特点

- 支持自定义类别顺序，确保生成的类别ID符合预期顺序
- 支持批量转换XML文件
- 自动计算YOLO格式所需的归一化坐标
- 支持中文路径和文件名
- 提供详细的转换进度和错误信息
- 支持自定义图片文件扩展名

## 环境要求

- Python 3.x
- OpenCV (cv2)
- numpy
- xml.etree.ElementTree

安装依赖：
```bash
pip install opencv-python numpy
```

## 使用方法

1. 运行程序：
```bash
python xml_to_txt_converter.py
```

2. 按照提示输入：
   - 类别顺序（用逗号分隔，如：苹果,橘子）
   - 图片目录路径
   - XML文件目录路径
   - TXT输出目录路径
   - 图片文件扩展名（默认：jpg）

## 输入格式说明

### XML文件格式
必须是标准的目标检测XML标注格式，包含以下结构：
```xml
<annotation>
    <object>
        <name>类别名称</name>
        <bndbox>
            <xmin>100</xmin>
            <ymin>200</ymin>
            <xmax>300</xmax>
            <ymax>400</ymax>
        </bndbox>
    </object>
</annotation>
```

### 输出TXT格式
每行的格式为：`类别ID x_center y_center width height`
- 所有值都是归一化后的浮点数（0-1之间）
- 每个标注框占一行
- 类别ID基于用户定义的顺序从0开始编号

## 示例

1. 设置类别顺序：
```
请按照期望顺序输入类别名称，用逗号分隔: 苹果,橘子
```

2. 最终在TXT文件中：
- 苹果的类别ID为0
- 橘子的类别ID为1

## 注意事项

1. 确保XML文件中的类别名称与输入的类别名称完全匹配（包括大小写和空格）
2. 程序会自动跳过未定义的类别并给出警告
3. 图片文件名必须与XML文件名相对应（除了扩展名）
4. 请确保所有路径都存在且有正确的读写权限

## 错误处理

- 如果转换过程中出现错误，程序会显示具体的错误信息
- 在转换完成后会列出所有转换失败的文件
- 对于未定义的类别，程序会给出警告并继续处理其他标注

