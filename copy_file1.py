from datetime import datetime
import os
import subprocess

"""
==============================================================================
脚本名称: Git 提交文件自动提取与转存工具
功能描述:
    1. 自动获取当前用户在该 Git 项目中的所有历史提交文件清单。
    2. 将清单保存为文本文件，并自动进行去重与排序处理。
    3. 按照项目的原始目录结构，将提交过的源码文件逐行读取并复制导出至目标路径。
    4. 导出时自动在原文件名末尾追加 `.txt` 后缀（如 `MainActivity.kt` -> `MainActivity.kt.txt`）

环境要求:
    - Python 3.6+
    - 本地已安装并配置好 Git 环境
==============================================================================
"""

def generate_git_files_list(project_root, txt_file_path):
    """
    在项目根目录下自动执行 git 命令，生成包含当前用户提交文件列表的 txt 文件。
    """
    if not os.path.exists(project_root):
        print(f"❌ 错误：项目根目录不存在 -> {project_root}")
        return False

    # 1. 确保目标 TXT 文件的父目录存在
    dir_name = os.path.dirname(txt_file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    # 2. 先独立获取 Git 用户名（解决 Windows 下 $(git config ...) 语法失效问题）
    user_name_cmd = "git config user.name"
    user_name_res = subprocess.run(
        user_name_cmd,
        cwd=project_root,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    author_name = user_name_res.stdout.strip()
    
    if not author_name:
        print("❌ 错误：未能获取到当前系统的 git user.name，请检查 git 配置。")
        return False

    print(f"检测到当前 Git 用户: [{author_name}]")
    print(f"正在项目目录 [{project_root}] 中获取提交文件列表...")

    # 3. 构造带明确作者名字的 Git 命令
    #   git log --author="$(git config user.name)" --name-only --pretty=format:"" | sort -u | sed '/^$/d' > git_all_commit_files.txt
    git_cmd = f'git log --author="{author_name}" --name-only --pretty=format:""'
    
    try:
        result = subprocess.run(
            git_cmd,
            cwd=project_root,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode != 0:
            print(f"❌ Git 命令执行失败: {result.stderr}")
            return False

        # 对文件路径去重、排序并过滤空行
        raw_lines = result.stdout.splitlines()
        clean_files = sorted(list(set(line.strip() for line in raw_lines if line.strip())))

        if not clean_files:
            print(f"⚠️ 警告：未查找到用户 [{author_name}] 在此仓库中的任何提交文件。")
            return False

        # 将结果写入列表 txt 文件
        with open(txt_file_path, 'w', encoding='utf-8') as f:
            for file_path in clean_files:
                f.write(file_path + '\n')

        print(f"✓ 成功生成文件列表，共计 {len(clean_files)} 个文件 -> {txt_file_path}")
        return True

    except Exception as e:
        print(f"❌ 执行 Git 指令发生异常: {e}")
        return False


def read_and_write_as_txt(project_root, txt_file_path, output_dir):
    """
    根据 txt 文件中的相对路径列表，逐行读取源文件内容，
    并在目标文件夹（OUTPUT_DIR）保留原有目录结构，直接在原文件名末尾加上 .txt 后缀导出。
    """
    project_root = os.path.abspath(project_root)
    output_dir = os.path.abspath(output_dir)

    if not os.path.exists(txt_file_path):
        print(f"❌ 错误：找不到文件列表文件 -> {txt_file_path}")
        return

    success_count = 0
    fail_count = 0

    with open(txt_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for line in lines:
        rel_path = line.strip().replace('\\', '/')
        
        if not rel_path:
            continue

        src_path = os.path.join(project_root, rel_path)

        if os.path.exists(src_path) and os.path.isfile(src_path):
            target_rel_path = rel_path + ".txt"
            dest_txt_path = os.path.join(output_dir, target_rel_path)

            try:
                dest_dir = os.path.dirname(dest_txt_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)

                with open(src_path, 'r', encoding='utf-8', errors='ignore') as src_file, \
                     open(dest_txt_path, 'w', encoding='utf-8') as target_file:
                    
                    for src_line in src_file:
                        target_file.write(src_line)

                success_count += 1
            except Exception as e:
                print(f"✗ 读取/写入异常: {rel_path} -> 原因: {e}")
                fail_count += 1
        else:
            print(f"✗ 缺失/无效: {rel_path} (源文件不存在或不是标准文件)")
            fail_count += 1

    print("\n" + "=" * 40)
    print(f"处理完成！成功写入 {success_count} 个文件到目标文件夹，失败/缺失 {fail_count} 个。")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    current_time = datetime.now().strftime("%Y%m%d")
    PROJECT_NAME = "Baseline_main"
    
    # ------------------ 配置参数 ------------------
    PROJECT_ROOT = r"D:/AndroidStudioProjects/" + PROJECT_NAME
    OUTPUT_DIR = r"E:/" + PROJECT_NAME + "_Copy_Files_" + current_time
    TXT_FILE = OUTPUT_DIR + "/git_all_commit_files.txt"
    # ----------------------------------------------

    # 1. 自动生成 TXT_FILE 文件
    if generate_git_files_list(PROJECT_ROOT, TXT_FILE):
        # 2. 读取列表并导出带 .txt 后缀的文件
        read_and_write_as_txt(PROJECT_ROOT, TXT_FILE, OUTPUT_DIR)

        # 3. 处理完成后删除临时的 TXT_FILE
        if os.path.exists(TXT_FILE):
            os.remove(TXT_FILE)
            print(f"已删除文件列表文件: {TXT_FILE}")
        else:
            print(f"文件列表文件不存在，无法删除: {TXT_FILE}")

