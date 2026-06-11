import os
import json
import random
import time
from datetime import datetime
from faker import Faker

fake = Faker('zh_CN')

def create_random_package(target_dir):
    root_path = os.path.abspath(target_dir)
    os.makedirs(root_path, exist_ok=True)

    # --- 修改部分：匹配 HIS_yyyyMMdd_HHmmss_nano_random 格式 ---
    # 获取随机生成的日期（复用你下方的 random_date 以保持文件夹名和内容时间一致）
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 3, 20)
    random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    
    folder_time = random_date.strftime("%Y%m%d_%H%M%S")
    # 模拟 4 位纳秒后缀
    # nano_suffix = str(random.randint(1000, 9999)) 
    # 3 位随机数
    random_suffix = random.randint(100, 999)
    
    # 生成最终的 historyId (folder_id)
    # folder_id = f"HIS_{folder_time}_{nano_suffix}_{random_suffix}"
    # folder_id = f"HIS_{folder_time}_{random_suffix}"
    folder_id = f"HIS_{folder_time}_{random_suffix}_{"".join([str(random.randint(0, 9)) for _ in range(12)])}"
    # -------------------------------------------------------

    full_folder_path = os.path.join(root_path, folder_id)
    os.makedirs(full_folder_path, exist_ok=True)

    module_list = ["防盗", "UI测试", "遥控测频", "ECU克隆", "系统扫描"]
    module_name = random.choice(module_list)
    year_name = random.randint(2010, 2026)
    brand_name = fake.company_prefix()
    dtc_count = random.randint(0, 50)
    repair_status = random.randint(0, 1)
    
    picList = [f"/storage/emulated/0/DCIM/Camera/pic{random.randint(1, 11)}.png" 
               for _ in range(random.randint(0, 6))]
    
    time_format_a = random_date.strftime("%Y-%m-%d %H-%M-%S")
    time_format_b = random_date.strftime("%Y-%m-%d %H:%M:%S")

    # file_name = f"({module_name}){year_name}_{brand_name}_{time_format_a}_{dtc_count}_{repair_status}.json"
    file_name = "data.json"
    file_path = os.path.join(full_folder_path, file_name)

    data = {
      "HoursVal": "24",
      "MaintainState": repair_status,
      "MaintenanceStaff": fake.name(),
      "Remark": "维修备注",
      "Summarize": "",
      "BrandName": brand_name,
      "createTime": time_format_b,
      "isGeneratedSeparately": True,
      "MileageVaule": "123",
      "ModelName": module_name,
      "ownerName": fake.name(),
      "pageType": 0,
      "phoneNumber": fake.phone_number(),
      "picPaths": picList,
      "postalCode": fake.postcode(),
      "ReportName": f"{brand_name} {year_name} {module_name}",
      "SysItems": [
        {
          "StateText": "主动的/静态的",
          "Description": "燃油存量传感器1电阻太大",
          "FaultCode": "Code:xxxxx PID:xxx FMI:xxx",
          "index": 0, "State": 0, "SysName": "SysName"
        },
        # ... 这里保留你原本的 SysItems 列表即可
      ],
      "vehiclePlate": "cheliangpaizhao",
      # "VinName": "", # 这里通常 VinName 会对应文件夹 ID
      "VinName": folder_id, # 这里通常 VinName 会对应文件夹 ID
      "YearName": year_name,
      "ChildType": -1,
      "EnableCount": 0,
      "EnableSysBack": True,
      "BottomBtn": False,
      "FloatBtn": False,
      "MenuPath": "",
      "MsgType": 0,
      "TipPath": "",
      "Title": "历史记录",
      "TreeSideNodeCheck": False
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ 生成成功！ ID: {folder_id}")


if __name__ == "__main__":
    # 请确保路径在你的系统上有效
    my_path = r"E:/adb_logcat/target111"
    
    n = 15
    for _ in range(n):
        create_random_package(my_path)