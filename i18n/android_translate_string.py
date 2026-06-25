import os
import requests
import time
import re
from dotenv import load_dotenv

'''
功能：将单个翻译文本根据字典里的语言代码全部翻译，并替换到对应的翻译文件string.xml内
升级：支持传入 previous_string_name 锚点，若不存在则根据英文顺序向前追溯插入。


问题：
报错【400 Client Error: Bad Request for url:】时，说明google翻译语言代码有误
'''

# ==================== 配置区域 ====================
RES_PATH = "D:/AndroidStudioProjects/Baseline_main/module-diag/src/main/res"  # 当前模块的绝对路径
ORIGINAL_TEXT = "VIN Code"  # 待翻译文本
ORIGINAL_LANG = "en"  # 原始文本的语言代码（参考 google翻译语言代码：https://docs.cloud.google.com/translate/docs/languages?hl=zh-cn）
STRING_NAME = "sh_diag_report_vin"  # string的标签名

# 插入位置的锚点标签名。为空串，则放入</resources>上方；若不为空，则会在英文顺序中向前追溯，找到第一个存在于当前目标xml文件的标签名，并插入到其后。
PREVIOUS_STRING_NAME = "sh_diag_report_year"  

# Android 文件夹后缀与 Google 翻译语言代码的映射字典
LANG_MAPPING = {
    '': 'en',           # 英文
    'ar': 'ar',         # 阿拉伯语【反向语言】
    'cs': 'cs',         # 捷克语
    'de-rDE': 'de',     # 德语
    'el-rGR': 'el',     # 希腊语
    'es': 'es',         # 西班牙语
    'fa-rIR': 'fa',     # 波斯语【反向语言】
    'fr-rFR': 'fr',     # 法语
    'in-rID': 'id',     # 印尼语
    'it-rIT': 'it',     # 意大利语
    'iw': 'iw',         # 希伯来语【反向语言】
    'ja': 'ja',         # 日语
    'ko-rKR': 'ko',     # 韩语
    'nl-rNL': 'nl',     # 荷兰语
    'no': 'no',         # 挪威语
    'pl': 'pl',         # 波兰语
    'pt-rPT': 'pt-PT',  # 葡萄牙语【反向语言】
    'ru-rRU': 'ru',     # 俄语
    'sv': 'sv',         # 瑞典语
    'th-rTH': 'th',     # 泰语
    'tr-rTR': 'tr',     # 土耳其语
    'vi': 'vi',         # 越南语
    'zh-rCN': 'zh-CN',  # 中文简体
    'zh-rTW': 'zh-TW',  # 中文繁体
}

google_translate_key = ""
google_translate_url = "https://translation.googleapis.com/language/translate/v2"
translate_max_retries = 3
translate_delay = 1
# ==================================================


def translate_text(text, source_lang, target_lang):
    if not text:
        return ""
    try:
        for attempt in range(translate_max_retries):
            try:
                params = {
                    "q": text,
                    "target": target_lang,
                    "source": source_lang,
                    "key": google_translate_key
                }
                response = requests.get(google_translate_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if response.status_code == 200:
                    # 服务器返回的 JSON 数据示例：
                    #   {'data': {'translations': [{'translatedText': 'Start'}]}}
                    translated_text = data['data']['translations'][0]['translatedText']
                    print(f"原文: {text}")
                    print(f"译文: {translated_text}")
                    return translated_text
            except Exception as e:
                print(f"翻译尝试 {attempt + 1} 失败: {e}")
                if attempt < translate_max_retries - 1:
                    time.sleep(translate_delay * (attempt + 1))
                else:
                    print(f"翻译失败，使用原文: {text}")
                    return text
        return text
    except Exception as e:
        print(f'翻译错误：{e}')
        return text


def get_en_string_order(en_xml_path):
    """
    解析默认英文 values/strings.xml 中所有 string 标签的 name 属性，按顺序返回列表
    """
    order = []
    if not os.path.exists(en_xml_path):
        return order
    try:
        with open(en_xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 正则匹配 <string name="xxx">
        names = re.findall(r'<string\s+name="([^"]+)"', content)
        return names
    except Exception as e:
        print(f"解析英文基础顺序失败: {e}")
        return order


def append_string_pure_text(xml_path, name, text, previous_name, en_string_order):
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 1. 防重检查：如果文件中已经包含 name="file_path" 字符串，则跳过
        search_marker = f'name="{name}"'
        if any(search_marker in line for line in lines):
            print(f"  警告: 标签名 [{name}] 已存在于 {xml_path}，跳过该文件。")
            return

        target_index = -1
        find_anchor = None

        # 2. 如果指定了前置标签，启动追溯逻辑
        if previous_name and en_string_order:
            # 找到当前锚点在英文队列里的索引
            if previous_name in en_string_order:
                start_idx = en_string_order.index(previous_name)
                # 从当前锚点开始，往前依次寻找哪个标签在当前目标 xml 中存在
                for i in range(start_idx, -1, -1):
                    check_name = en_string_order[i]
                    # 检查当前 xml 文件的哪一行包含这个 check_name
                    for line_num, line in enumerate(lines):
                        if f'name="{check_name}"' in line:
                            target_index = line_num + 1  # 插入在这个标签的下一行
                            find_anchor = check_name
                            break
                    if target_index != -1:
                        break

        # 3. 如果没找到锚点，或者 previous_name 为空，走默认逻辑：插入到 </resources> 上方
        if target_index == -1:
            for i in range(len(lines) - 1, -1, -1):
                if "</resources>" in lines[i]:
                    target_index = i
                    break

        if target_index == -1:
            print(f"  错误: 在 {xml_path} 中未找到任何可插入的位置（包括 </resources>）！")
            return

        # 4. 构造要插入的字符串
        new_string_line = f"    <string name=\"{name}\">{text}</string>\n"

        # 5. 插入数据
        if find_anchor:
            # 找到了有效的兄弟锚点，紧跟其后插入
            lines.insert(target_index, new_string_line)
            print(f"  成功插入到锚点标签 [{find_anchor}] 之后 -> {xml_path}")
        else:
            # 降级放入 </resources> 标签上方
            lines.insert(target_index, "\n")  # 保持原有空行习惯
            lines.insert(target_index + 1, new_string_line)
            print(f"  未匹配到任何锚点，默认追加至末尾 </resources> 前 -> {xml_path}")

        # 6. 写回文件
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    except Exception as e:
        print(f"  操作文件失败: {e}")


def main():
    # 加载当前目录下的 .env 文件
    load_dotenv()

    # 从环境变量中读取 Key，如果找不到则返回 None
    global google_translate_key
    google_translate_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")

    if not google_translate_key:
        print("错误：未在 .env 文件中找到 GOOGLE_TRANSLATE_API_KEY")
        return

    if not os.path.exists(RES_PATH):
        print(f"错误: 路径不存在 -> {RES_PATH}")
        return

    # 获取默认英文包中的标签顺序，作为追溯的基准字典
    en_xml_path = os.path.join(RES_PATH, "values", "strings.xml")
    en_string_order = get_en_string_order(en_xml_path)
    print(f"解析英文基础顺序完成，共获取到 {len(en_string_order)} 个标签。")

    print("开始遍历 res 目录...")

    # 先处理默认 values 目录（如果有的话），确保它也能正常插入
    all_dirs = os.listdir(RES_PATH)
    if "values" in all_dirs:
        all_dirs.remove("values")
        all_dirs.insert(0, "values")  # 让默认包排在最前面处理

    for dir_name in all_dirs:
        dir_path = os.path.join(RES_PATH, dir_name)

        # 匹配 values 或者 values-xxx
        if os.path.isdir(dir_path) and (dir_name == "values" or dir_name.startswith("values-")):
            
            lang_suffix = "" if dir_name == "values" else dir_name.replace("values-", "")

            if lang_suffix in LANG_MAPPING:
                target_lang = LANG_MAPPING[lang_suffix]
                strings_xml_path = os.path.join(dir_path, "strings.xml")

                if os.path.exists(strings_xml_path):
                    print("-" * 50)
                    print(f"\n正在处理: {dir_name} (语言代码: {target_lang})...")

                    # 1. 翻译（如果是默认英文包 values，直接用原文，不需要调 Google 接口）
                    if dir_name == "values":
                        translated_text = ORIGINAL_TEXT
                    else:
                        translated_text = translate_text(ORIGINAL_TEXT, ORIGINAL_LANG, target_lang)

                    # 2. 追加或定位插入
                    if translated_text:
                        append_string_pure_text(
                            strings_xml_path, 
                            STRING_NAME, 
                            translated_text, 
                            PREVIOUS_STRING_NAME, 
                            en_string_order
                        )


if __name__ == "__main__":
    main()