import os
import requests
import time

'''
功能：将单个翻译文本根据字典里的语言代码全部翻译，并替换到对应的翻译文件string.xml内

问题：
报错【400 Client Error: Bad Request for url:】时google翻译语言代码有误
'''

# ==================== 配置区域 ====================
RES_PATH = "D:/AndroidStudioProjects/Baseline_main/common-ui/src/main/res"  # 当前模块的绝对路径
ORIGINAL_TEXT = ""  # 待翻译文本
ORIGINAL_LANG = "en"  # 原始文本的语言代码（参考 google翻译语言代码：https://docs.cloud.google.com/translate/docs/languages?hl=zh-cn）
STRING_NAME = ""  # string的标签名

# Android 文件夹后缀与 Google 翻译语言代码的映射字典
LANG_MAPPING = {
    '': 'en',  # 英文
    'ar': 'ar',  # 阿拉伯语
    'cs': 'cs',  # 捷克语
    'de-rDE': 'de',  # 德语
    'el-rGR': 'el',  # 希腊语
    'es': 'es',  # 西班牙语
    'fa-rIR': 'fa',  # 波斯语
    'fr-rFR': 'fr',  # 法语
    'in-rID': 'id',  # 印尼语
    'it-rIT': 'it',  # 意大利语
    'iw': 'iw',  # 希伯来语
    'ja': 'ja',  # 日语
    'ko-rKR': 'ko',  # 韩语
    'nl-rNL': 'nl',  # 荷兰语
    'no': 'no',  # 挪威语
    'pl': 'pl',  # 波兰语
    'pt-rPT': 'pt-PT',  # 葡萄牙语（葡萄牙）
    'ru-rRU': 'ru',  # 俄语
    'sv': 'sv',  # 瑞典语
    'th-rTH': 'th',  # 泰语
    'tr-rTR': 'tr',  # 土耳其语
    'vi': 'vi',  # 越南语
    'zh-rCN': 'zh-CN',  # 中文简体
    'zh-rTW': 'zh-TW',  # 中文繁体
}

google_translate_key = ""
google_translate_url = "https://translation.googleapis.com/language/translate/v2"
translate_max_retries = 3
translate_delay = 1


# ==================================================


def translate_text(text, source_lang, target_lang):
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
                    # {'data': {'translations': [{'translatedText': 'Start'}]}}
                    translated_text = data['data']['translations'][0]['translatedText']
                    print(f"原文: {text}")
                    print(f"译文: {translated_text}")
                    print("-" * 50)
                    return translated_text

            except Exception as e:
                print(f"翻译尝试 {attempt + 1} 失败: {e}")
                if attempt < translate_max_retries - 1:
                    time.sleep(translate_delay * (attempt + 1))
                else:
                    print(f"翻译失败，原文: {text}")
                    return ""
        return ""
    except Exception as e:
        print(f'翻译错误：{e}')
        return ""


def append_string_pure_text(xml_path, name, text):
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 1. 防重检查：如果文件中已经包含 name="file_path" 字符串，则跳过
        search_marker = f'name="{name}"'
        if any(search_marker in line for line in lines):
            print(f"  警告: 标签名 '{name}' 已存在于 {xml_path}，跳过该文件。")
            return

        # 2. 寻找 </resources> 标签的位置
        target_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if "</resources>" in lines[i]:
                target_index = i
                break

        if target_index == -1:
            print(f"  错误: 在 {xml_path} 中未找到 </resources> 结束标签！")
            return

        # 3. 构造要插入的完整字符串（带标准的 4 空格缩进）
        new_string_line = f"    <string name=\"{name}\">{text}</string>\n"

        # 4. 在 </resources> 上方插入空行和新标签
        lines.insert(target_index, "\n")  # 插入空行
        lines.insert(target_index + 1, new_string_line)  # 插入新标签

        # 5. 写回文件
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"  成功追加至: {xml_path}")

    except Exception as e:
        print(f"  操作文件失败: {e}")


def main():
    if not os.path.exists(RES_PATH):
        print(f"错误: 路径不存在 -> {RES_PATH}")
        return

    print("开始遍历 res 目录...")

    for dir_name in os.listdir(RES_PATH):
        dir_path = os.path.join(RES_PATH, dir_name)

        if os.path.isdir(dir_path) and dir_name.startswith("values-"):
            lang_suffix = dir_name.replace("values-", "")

            if lang_suffix in LANG_MAPPING:
                target_lang = LANG_MAPPING[lang_suffix]
                strings_xml_path = os.path.join(dir_path, "strings.xml")

                if os.path.exists(strings_xml_path):
                    print(f"正在处理: {dir_name}...")

                    # 1. 翻译
                    translated_text = translate_text(ORIGINAL_TEXT, ORIGINAL_LANG, target_lang)

                    # 2. 追加
                    if translated_text:
                        append_string_pure_text(strings_xml_path, STRING_NAME, translated_text)


if __name__ == "__main__":
    main()
