import os.path
import subprocess
import sys
import xlrd

'''
读取excel表头
'''

# 读取excel表头
def read_excel_header(file_path):
    # key为sheet name   value：为表头list
    excel_head_dict = {}
    xls_file = xlrd.open_workbook(file_path)
    # 遍历所有的sheet
    for sheet in xls_file.sheets():
        key = sheet.name
        value_list = []
        columns = sheet.ncols
        for columIndex in range(columns):
            value = sheet.cell(0, columIndex).value
            value_list.append(value)
        excel_head_dict[key] = value_list

    return excel_head_dict


# 根据表头查找sheet名称
def find_sheet_by_head(excel_head_dict, head_name):
    for k, v_list in excel_head_dict.items():
        flag = False
        for v in iter(v_list):
            if head_name == v:
                flag = True
                break
        if flag:
            print(k)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    file_path = "D:/DOC/平板界面文本 string完整版.xls"
    head_name = "SV"

    excel_head_dict = read_excel_header(file_path)
    print('tips: 输出格式为：{sheet名称: [该sheet名称下所有表头]}')
    for sheet in excel_head_dict.keys():
        print(f"{sheet}: {excel_head_dict.get(sheet)}")

    print(f"\n'{head_name}' 表头所在的sheet页：")
    find_sheet_by_head(excel_head_dict, head_name)
