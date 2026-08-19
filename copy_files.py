import os
import shutil

def copy_files_from_list(project_root, txt_file_path, output_dir):
    """
    根据 txt 文件中的相对路径列表，将文件复制到新的文件夹中并保留原有目录结构。
    """
    # 确保根路径和输出路径格式统一
    project_root = os.path.abspath(project_root)
    output_dir = os.path.abspath(output_dir)

    # 检查 TXT 文件是否存在
    if not os.path.exists(txt_file_path):
        print(f"❌ 错误：找不到文件列表文件 -> {txt_file_path}")
        return

    success_count = 0
    fail_count = 0

    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # 去除首尾空格和换行符，同时统一将正反斜杠格式化
        rel_path = line.strip().replace('\\', '/')
        
        # 忽略空行
        if not rel_path:
            continue

        # 拼接完整的源文件路径和目标文件路径
        src_path = os.path.join(project_root, rel_path)
        dest_path = os.path.join(output_dir, rel_path)

        if os.path.exists(src_path):
            # 自动创建目标文件所在的子目录
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            # 复制文件（保留文件元数据）
            shutil.copy2(src_path, dest_path)
            # print(f"✓ 成功: {rel_path}")
            success_count += 1
        else:
            print(f"✗ 缺失: {rel_path} (源文件不存在)")
            fail_count += 1

    print("\n" + "=" * 40)
    print(f"处理完成！成功复制 {success_count} 个文件，失败/缺失 {fail_count} 个。")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    # ------------------ 配置参数 ------------------
    PROJECT_ROOT = r"D:/AndroidStudioProjects/Baseline_main"                           # 项目根目录
    TXT_FILE = r"D:/AndroidStudioProjects/Baseline_main/git_all_commit_files.txt"      # 包含相对路径列表的 txt 文件
    OUTPUT_DIR = r"E:/Demo_Exported_Files"                                             # 复制出来的目标文件夹
    # ----------------------------------------------

    copy_files_from_list(PROJECT_ROOT, TXT_FILE, OUTPUT_DIR)