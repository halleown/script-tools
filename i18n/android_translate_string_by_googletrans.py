import asyncio
import os

from googletrans import Translator
import sys
import time
import xml.etree.ElementTree as ET

'''
使用googletrans库翻译
'''


class AndroidStringTranslator:
    def __init__(self, language_code):
        self.delay = 1.0  # 请求间隔，避免API限制
        self.max_retries = 3  # 最大重试次数
        self.language_code = language_code

    async def translate_text(self, text: str) -> str:
        try:
            # 清理文本，移除多余的空白字符
            text = text.strip()
            if not text:
                return text
            for attempt in range(self.max_retries):
                try:
                    async with Translator() as translator:
                        result = await translator.translate(text, dest=self.language_code, src='en')
                        translated_text = result.text

                        print(f"原文: {text}")
                        print(f"译文: {translated_text}")
                        print("-" * 50)

                        return translated_text

                except Exception as e:
                    print(f"翻译尝试 {attempt + 1} 失败: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.delay * (attempt + 1))
                    else:
                        print(f"翻译失败，原文: {text}")
                        return ""
            return ""
        except Exception as e:
            print(f'翻译错误：{e}')
            return ""

    def translate_xml_file(self, input_file: str, output_file: str) -> bool:
        try:
            # 解析XML文件
            tree = ET.parse(input_file)
            root = tree.getroot()

            # 查找所有string标签
            string_elements = root.findall('.//string')
            total_strings = len(string_elements)

            print(f"{input_file} 共找到 {total_strings} 个string标签需要翻译")
            print("=" * 60)

            for i, string_elem in enumerate(string_elements, 1):
                if string_elem.text:
                    print(f"正在翻译第 {i}/{total_strings} 个标签【{string_elem.attrib['name']}】...")
                    original_text = string_elem.text
                    translated_text = asyncio.run(self.translate_text(original_text))
                    string_elem.text = translated_text

                    time.sleep(self.delay)

            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print("=" * 60)
            print(f"翻译完成！翻译结果已保存到: {output_file}")
            return True

        except ET.ParseError as e:
            print(f"XML解析错误: {e}")
            return False
        except Exception as e:
            print(f"处理文件时出错: {e}")
            return False


def get_en_file_path(project_path: str):
    # 各模块下的string_en.xml绝对路径
    en_xml_path_list = []
    # 各模块下res的绝对路径
    res_path_list = []
    # 遍历目录树
    for root, dirs, files in os.walk(project_path):
        # 检查当前目录是否是 res 目录
        if os.path.basename(root) == 'res':
            # 构建 values/strings.xml 路径
            strings_xml_path = os.path.join(root, 'values', 'strings.xml')
            # 多写了一个string_xml_path，为了防止values文件夹，是string.xml命名的
            string_xml_path = os.path.join(root, 'values', 'string.xml')
            # 检查文件是否存在
            if os.path.isfile(string_xml_path):
                en_xml_path_list.append(string_xml_path)
                res_path_list.append(root)
                print(f'找到英文string.xml：{string_xml_path}')
            elif os.path.isfile(strings_xml_path):
                en_xml_path_list.append(strings_xml_path)
                res_path_list.append(root)
                print(f'找到英文strings.xml：{strings_xml_path}')
            # else:
            #     print(f"找到 res 目录但未找到 values/strings.xml: {root}")
    return en_xml_path_list, res_path_list


def install_requirements():
    try:
        import googletrans
    except ImportError:
        print("正在安装 googletrans 库...")
        os.system("pip install googletrans==4.0.0rc1")
        print("安装完成！")


def main():
    install_requirements()

    # 自定义参数（需替换）
    project_path = "D:/AndroidStudioProjects/MyApplication"
    language_code = "sv"
    values_folder_name = f'values-{language_code}'

    en_xml_path_lists, res_path_lists = get_en_file_path(project_path)
    for i in range(len(en_xml_path_lists)):
        input_file = en_xml_path_lists[i]
        res_dir = f'{res_path_lists[i]}/{values_folder_name}'
        output_file = f'{res_dir}/strings.xml'
        try:
            with open(input_file, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            print(f"错误: 找不到输入文件 '{input_file}'")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 无法读取输入文件 '{input_file}': {e}")
            sys.exit(1)

        if not os.path.exists(res_dir):
            os.mkdir(res_dir)

        translator = AndroidStringTranslator(language_code)
        success = translator.translate_xml_file(input_file, output_file)

        if success:
            print(f"第 {i + 1}/{len(en_xml_path_lists)} 个翻译任务完成！")
        else:
            print(f"第 {i + 1}/{len(en_xml_path_lists)} 个翻译任务失败！")
            sys.exit(1)


if __name__ == "__main__":
    main()
