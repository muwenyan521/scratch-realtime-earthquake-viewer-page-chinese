import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import sys

# 检查并导入必要的库
try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False
    print("警告: fonttools 库未安装")
    print("请运行: pip install fonttools")

class SVGToPathConverter:
    def __init__(self):
        self.svg_namespace = "http://www.w3.org/2000/svg"
        ET.register_namespace("", self.svg_namespace)
        self.default_font = None
        self.font_cache = {}
        self.load_default_font()
    
    def load_default_font(self):
        """加载默认字体"""
        if not FONTTOOLS_AVAILABLE:
            return
        
        # 指定的字体路径
        font_path = "C:/Windows/Fonts/DreamHanSans-W17.ttc"
        
        # 备选字体路径
        fallback_fonts = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
        ]
        
        # 首先尝试加载指定字体
        if os.path.exists(font_path):
            try:
                self.default_font = TTFont(font_path, fontNumber=0)
                print(f"✅ 成功加载指定字体: {font_path}")
                return
            except Exception as e:
                print(f"❌ 加载指定字体失败 {font_path}: {e}")
        else:
            print(f"❌ 指定字体文件不存在: {font_path}")
        
        # 尝试备选字体
        for font_path in fallback_fonts:
            if os.path.exists(font_path):
                try:
                    self.default_font = TTFont(font_path)
                    print(f"✅ 成功加载备选字体: {font_path}")
                    return
                except Exception as e:
                    print(f"❌ 加载备选字体失败 {font_path}: {e}")
                    continue
        
        print("❌ 无法加载任何字体文件，文本将转换为占位符")
    
    def recording_pen_to_svg_path(self, recording_pen):
        """将RecordingPen的记录转换为SVG路径"""
        path_data = []
        
        for operation, args in recording_pen.value:
            if operation == 'moveTo':
                x, y = args[0]
                path_data.append(f"M {x:.2f} {y:.2f}")
            elif operation == 'lineTo':
                x, y = args[0]
                path_data.append(f"L {x:.2f} {y:.2f}")
            elif operation == 'curveTo':
                # 三次贝塞尔曲线
                if len(args) >= 3:
                    x1, y1 = args[0]
                    x2, y2 = args[1]
                    x3, y3 = args[2]
                    path_data.append(f"C {x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f} {x3:.2f} {y3:.2f}")
            elif operation == 'qCurveTo':
                # 二次贝塞尔曲线
                if len(args) >= 2:
                    for i in range(len(args) - 1):
                        x1, y1 = args[i]
                        x2, y2 = args[i + 1]
                        path_data.append(f"Q {x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f}")
            elif operation == 'closePath':
                path_data.append("Z")
        
        return " ".join(path_data)
    
    def text_to_path_advanced(self, x, y, text_content, font_size=16, font_family="Arial"):
        """使用fonttools将文本转换为路径"""
        if not FONTTOOLS_AVAILABLE or not self.default_font:
            print(f"⚠️  文本转换失败，使用占位符: {text_content}")
            return self.text_to_path_placeholder(x, y, text_content, font_size)
        
        try:
            font = self.default_font
            glyph_set = font.getGlyphSet()
            cmap = font.getBestCmap()
            
            if not cmap:
                print("❌ 字体缺少字符映射表")
                return self.text_to_path_placeholder(x, y, text_content, font_size)
            
            # 计算缩放因子
            units_per_em = font['head'].unitsPerEm
            scale = font_size / units_per_em
            
            path_segments = []
            current_x = x
            
            print(f"🔄 正在转换文本: '{text_content}' (字体大小: {font_size})")
            
            for i, char in enumerate(text_content):
                char_code = ord(char)
                
                if char_code in cmap:
                    glyph_name = cmap[char_code]
                    
                    if glyph_name in glyph_set:
                        glyph = glyph_set[glyph_name]
                        
                        # 使用RecordingPen记录路径
                        recording_pen = RecordingPen()
                        
                        # 创建变换笔，应用缩放和位置变换
                        transform = Transform(scale, 0, 0, -scale, current_x, y)
                        transform_pen = TransformPen(recording_pen, transform)
                        
                        # 绘制字形
                        glyph.draw(transform_pen)
                        
                        # 转换为SVG路径
                        char_path = self.recording_pen_to_svg_path(recording_pen)
                        
                        if char_path and char_path.strip():
                            path_segments.append(char_path)
                            print(f"  ✅ 字符 '{char}' 转换成功")
                        else:
                            print(f"  ⚠️  字符 '{char}' 路径为空")
                        
                        # 移动到下一个字符位置
                        advance_width = glyph.width * scale
                        current_x += advance_width
                    else:
                        print(f"  ❌ 字符 '{char}' 不在字形集中")
                        current_x += font_size * 0.5
                else:
                    print(f"  ❌ 字符 '{char}' (U+{char_code:04X}) 不在字符映射表中")
                    current_x += font_size * 0.5
            
            if path_segments:
                result_path = " ".join(path_segments)
                print(f"  ✅ 文本转换完成，生成路径长度: {len(result_path)}")
                return result_path
            else:
                print(f"  ❌ 没有生成任何路径，使用占位符")
                return self.text_to_path_placeholder(x, y, text_content, font_size)
            
        except Exception as e:
            print(f"❌ 高级文本转换出错: {e}")
            import traceback
            traceback.print_exc()
            return self.text_to_path_placeholder(x, y, text_content, font_size)
    
    def text_to_path_placeholder(self, x, y, text_content, font_size=16):
        """文本转换为路径的占位符实现"""
        text_width = len(text_content) * font_size * 0.6
        text_height = font_size * 0.8
        
        # 创建文本边界框
        return f"M {x} {y-text_height} L {x+text_width} {y-text_height} L {x+text_width} {y} L {x} {y} Z"
    
    def circle_to_path(self, cx, cy, r):
        """将圆形转换为path"""
        return f"M {cx-r} {cy} A {r} {r} 0 1 0 {cx+r} {cy} A {r} {r} 0 1 0 {cx-r} {cy} Z"
    
    def rect_to_path(self, x, y, width, height, rx=0, ry=0):
        """将矩形转换为path"""
        if rx == 0 and ry == 0:
            return f"M {x} {y} L {x+width} {y} L {x+width} {y+height} L {x} {y+height} Z"
        else:
            rx = min(rx, width/2)
            ry = min(ry, height/2)
            return f"M {x+rx} {y} L {x+width-rx} {y} A {rx} {ry} 0 0 1 {x+width} {y+ry} L {x+width} {y+height-ry} A {rx} {ry} 0 0 1 {x+width-rx} {y+height} L {x+rx} {y+height} A {rx} {ry} 0 0 1 {x} {y+height-ry} L {x} {y+ry} A {rx} {ry} 0 0 1 {x+rx} {y} Z"
    
    def line_to_path(self, x1, y1, x2, y2):
        """将直线转换为path"""
        return f"M {x1} {y1} L {x2} {y2}"
    
    def polyline_to_path(self, points):
        """将折线转换为path"""
        point_list = re.findall(r'[\d.-]+', points)
        if len(point_list) < 4:
            return ""
        
        path = f"M {point_list[0]} {point_list[1]}"
        for i in range(2, len(point_list), 2):
            if i + 1 < len(point_list):
                path += f" L {point_list[i]} {point_list[i+1]}"
        return path
    
    def polygon_to_path(self, points):
        """将多边形转换为path"""
        path = self.polyline_to_path(points)
        if path:
            path += " Z"
        return path
    
    def ellipse_to_path(self, cx, cy, rx, ry):
        """将椭圆转换为path"""
        return f"M {cx-rx} {cy} A {rx} {ry} 0 1 0 {cx+rx} {cy} A {rx} {ry} 0 1 0 {cx-rx} {cy} Z"
    
    def get_float_attr(self, element, attr_name, default=0):
        """安全获取浮点数属性"""
        try:
            value = element.get(attr_name, str(default))
            value = re.sub(r'[a-zA-Z%]+$', '', value)
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_text_content(self, element):
        """获取文本元素的内容"""
        text = element.text or ""
        for child in element:
            if child.tag.endswith('tspan'):
                text += child.text or ""
            text += child.tail or ""
        return text.strip()
    
    def parse_font_info(self, element):
        """解析字体信息"""
        font_size = 16
        font_family = "Arial"
        
        # 从属性中获取
        font_size = self.get_float_attr(element, 'font-size', font_size)
        font_family = element.get('font-family', font_family)
        
        # 从style属性中获取
        style = element.get('style', '')
        if style:
            # 解析font-size
            font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)
            if font_size_match:
                font_size = float(font_size_match.group(1))
            
            # 解析font-family
            font_family_match = re.search(r'font-family:\s*([^;]+)', style)
            if font_family_match:
                font_family = font_family_match.group(1).strip('\'"')
        
        return font_size, font_family
    
    def convert_element_to_path(self, element):
        """将SVG元素转换为path元素"""
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        
        if tag == 'circle':
            cx = self.get_float_attr(element, 'cx')
            cy = self.get_float_attr(element, 'cy')
            r = self.get_float_attr(element, 'r')
            if r > 0:
                return self.circle_to_path(cx, cy, r)
        
        elif tag == 'rect':
            x = self.get_float_attr(element, 'x')
            y = self.get_float_attr(element, 'y')
            width = self.get_float_attr(element, 'width')
            height = self.get_float_attr(element, 'height')
            rx = self.get_float_attr(element, 'rx')
            ry = self.get_float_attr(element, 'ry')
            if width > 0 and height > 0:
                return self.rect_to_path(x, y, width, height, rx, ry)
        
        elif tag == 'line':
            x1 = self.get_float_attr(element, 'x1')
            y1 = self.get_float_attr(element, 'y1')
            x2 = self.get_float_attr(element, 'x2')
            y2 = self.get_float_attr(element, 'y2')
            return self.line_to_path(x1, y1, x2, y2)
        
        elif tag == 'polyline':
            points = element.get('points', '')
            if points:
                return self.polyline_to_path(points)
        
        elif tag == 'polygon':
            points = element.get('points', '')
            if points:
                return self.polygon_to_path(points)
        
        elif tag == 'ellipse':
            cx = self.get_float_attr(element, 'cx')
            cy = self.get_float_attr(element, 'cy')
            rx = self.get_float_attr(element, 'rx')
            ry = self.get_float_attr(element, 'ry')
            if rx > 0 and ry > 0:
                return self.ellipse_to_path(cx, cy, rx, ry)
        
        elif tag == 'text':
            x = self.get_float_attr(element, 'x')
            y = self.get_float_attr(element, 'y')
            text_content = self.get_text_content(element)
            font_size, font_family = self.parse_font_info(element)
            
            if text_content:
                return self.text_to_path_advanced(x, y, text_content, font_size, font_family)
        
        return None
    
    def copy_attributes(self, source, target, exclude_attrs=None):
        """复制属性，排除指定的属性"""
        if exclude_attrs is None:
            exclude_attrs = set()
        
        for attr, value in source.attrib.items():
            if attr not in exclude_attrs:
                target.set(attr, value)
    
    def convert_svg_to_paths(self, svg_file):
        """转换SVG文件中的所有元素为path"""
        try:
            tree = ET.parse(svg_file)
            root = tree.getroot()
            
            # 需要转换的元素类型
            convertible_elements = ['circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'text']
            
            # 遍历所有元素
            elements_to_convert = []
            for elem in root.iter():
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if tag in convertible_elements:
                    elements_to_convert.append(elem)
            
            converted_count = 0
            
            print(f"  发现 {len(elements_to_convert)} 个需要转换的元素")
            
            # 转换元素
            for elem in elements_to_convert:
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                print(f"  正在转换 {tag} 元素...")
                
                path_d = self.convert_element_to_path(elem)
                if path_d:
                    # 创建新的path元素
                    path_elem = ET.Element('path')
                    path_elem.set('d', path_d)
                    
                    # 复制样式属性，排除几何属性
                    geometric_attrs = {
                        'cx', 'cy', 'r', 'x', 'y', 'width', 'height', 
                        'rx', 'ry', 'x1', 'y1', 'x2', 'y2', 'points',
                        'font-size', 'font-family'
                    }
                    self.copy_attributes(elem, path_elem, geometric_attrs)
                    
                    # 为原始元素添加数据属性
                    if tag == 'text':
                        text_content = self.get_text_content(elem)
                        path_elem.set('data-original-text', text_content)
                    path_elem.set('data-original-element', tag)
                    
                    # 替换原元素
                    parent = None
                    for p in root.iter():
                        if elem in p:
                            parent = p
                            break
                    
                    if parent is not None:
                        parent.remove(elem)
                        parent.append(path_elem)
                        converted_count += 1
                        print(f"    ✅ {tag} 元素转换成功")
                    else:
                        print(f"    ❌ 找不到 {tag} 元素的父节点")
                else:
                    print(f"    ❌ {tag} 元素转换失败")
            
            print(f"  总共转换了 {converted_count} 个元素")
            return tree
            
        except ET.ParseError as e:
            print(f"  ❌ 解析XML文件时出错: {e}")
            return None
        except Exception as e:
            print(f"  ❌ 转换过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def process_directory(self, directory="."):
        """处理目录中的所有SVG文件（直接覆盖源文件）"""
        if not os.path.exists(directory):
            print(f"目录 {directory} 不存在")
            return
        
        svg_files = [f for f in os.listdir(directory) if f.lower().endswith('.svg')]
        
        if not svg_files:
            print("当前目录中没有找到SVG文件")
            return
        
        print(f"找到 {len(svg_files)} 个SVG文件")
        print("警告：此操作将直接覆盖源文件！")
        
        success_count = 0
        
        for svg_file in svg_files:
            file_path = os.path.join(directory, svg_file)
            print(f"\n📁 处理文件: {svg_file} (直接覆盖源文件)")
            
            # 转换SVG
            converted_tree = self.convert_svg_to_paths(file_path)
            
            if converted_tree:
                # 直接覆盖源文件
                try:
                    # 格式化输出
                    rough_string = ET.tostring(converted_tree.getroot(), 'unicode')
                    reparsed = minidom.parseString(rough_string)
                    pretty_xml = reparsed.toprettyxml(indent="  ")
                    
                    # 移除多余的空行
                    lines = [line for line in pretty_xml.split('\n') if line.strip()]
                    pretty_xml = '\n'.join(lines)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(pretty_xml)
                    
                    print(f"  ✅ 转换完成并已覆盖: {svg_file}")
                    success_count += 1
                    
                except Exception as e:
                    print(f"  ❌ 保存文件时出错: {e}")
            else:
                print(f"  ❌ 跳过文件: {svg_file} (转换失败)")
        
        print(f"\n🎉 转换完成！成功处理 {success_count}/{len(svg_files)} 个文件")

def main():
    print("SVG元素转Path工具 (Windows专用版)")
    print("=" * 50)
    print("注意：此程序将直接覆盖原始SVG文件！")
    print("=" * 50)
    
    # 检查依赖
    if not FONTTOOLS_AVAILABLE:
        print("❌ fonttools 库未安装")
        print("请运行以下命令安装：")
        print("pip install fonttools")
        return
    else:
        print("✅ fonttools 库已安装")
    
    # 检查指定字体是否存在
    target_font = "C:/Windows/Fonts/DreamHanSans-W17.ttc"
    if os.path.exists(target_font):
        print(f"✅ 目标字体文件存在: {target_font}")
    else:
        print(f"❌ 目标字体文件不存在: {target_font}")
    
    print("\n支持的元素类型:")
    print("• circle (圆形)")
    print("• rect (矩形)")
    print("• line (直线)")
    print("• polyline (折线)")
    print("• polygon (多边形)")
    print("• ellipse (椭圆)")
    print("• text (文本) - 转换为真实路径")
    
    converter = SVGToPathConverter()
    converter.process_directory(".")

if __name__ == "__main__":
    main()