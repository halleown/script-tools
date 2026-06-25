import os
import json
import random
import time
from datetime import datetime
from faker import Faker

fake = Faker('zh_CN')

def create_random_package(target_dir, count):
    root_path = os.path.abspath(target_dir)
    os.makedirs(root_path, exist_ok=True)

    # --- 修改部分：匹配 HIS_yyyyMMdd_HHmmss_nano_random 格式 ---
    # 获取随机生成的日期（复用你下方的 random_date 以保持文件夹名和内容时间一致）
    start_date = datetime(2026, 6, 1)
    end_date = datetime(2026, 6, 20)
    random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    
    folder_time = random_date.strftime("%Y%m%d_%H%M%S")
    # 模拟 4 位纳秒后缀
    # nano_suffix = str(random.randint(1000, 9999)) 
    # 3 位随机数
    random_suffix = random.randint(100, 999)


    vin_name = f"{count:017d}"
    
    # 生成最终的 historyId (folder_id)
    # folder_id = f"HIS_{folder_time}_{nano_suffix}_{random_suffix}"
    # folder_id = f"HIS_{folder_time}_{random_suffix}"


    folder_id = f"HIS_{folder_time}_{random_suffix}_{vin_name}"
    # folder_id = f"{vin_name}_HIS_{folder_time}_{random_suffix}"
    # -------------------------------------------------------

    full_folder_path = os.path.join(root_path, folder_id)
    os.makedirs(full_folder_path, exist_ok=True)

    module_list = ["防盗", "UI测试", "遥控测频", "ECU克隆", "系统扫描"]
    module_name = random.choice(module_list)
    year_name = random.randint(2026, 2026)
    brand_name = fake.company_prefix()
    dtc_count = random.randint(0, 50)
    repair_status = random.randint(0, 1)
    
    # picList = [f"/storage/emulated/0/DCIM/Camera/pic{random.randint(1, 11)}.png" 
    #            for _ in range(random.randint(0, 6))]
    
    time_format_a = random_date.strftime("%Y-%m-%d %H-%M-%S")
    time_format_b = random_date.strftime("%Y-%m-%d %H:%M:%S")

    # file_name = f"({module_name}){year_name}_{brand_name}_{time_format_a}_{dtc_count}_{repair_status}.json"
    file_name = "data.json"
    file_path = os.path.join(full_folder_path, file_name)



    data = {
          "HoursVal": "20",
          "MaintainState": 0,
          "MaintenanceStaff": "",
          "Summarize": "",
          "BrandName": "SOUO",
          "createTime": time_format_b,
          "isGeneratedSeparately": False,
          "MileageVaule": "80",
          "ModelName": "S2000CL",
          "ownerName": "",
          "pageType": 0,
          "phoneNumber": "",
          "picPaths": [],
          "postalCode": "",
          "ReportName": f"SOUO {year_name} S2000CL",
          "StoreAddress": "",
          "StoreEmail": "",
          "StoreName": "",
          "StorePhone": "",
          "SysItems": getSysetmItem(),
          "vehiclePlate": "",
          "VinName": vin_name,
          "YearName": year_name,
          "ChildType": -1,
          "EnableCount": 0,
          "EnableSysBack": False,
          "FloatBtn": False,
          "MenuPath": "",
          "MsgType": 0,
          "TipPath": "",
          "Title": "",
          "TreeSideNodeCheck": False
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ 生成成功！ ID: {folder_id}")


def getSysetmItem():
    sys_items = []
    random_count = random.randint(0, 10)
    
    for index in range(random_count):
        sys_item = {
            "StateText": random.choice(["历史故障码", "当前故障码", "存储故障码"]),
            "Description": random.choice(["请参考该车维修手册", "MIB已通过DIA禁用", "MHG外部故障", "传感器启动识别故障(后)–暂时性故障", "IMU–电气故障、信号超范围及通信故障", "IMU–合理性故障"]),
            "FaultCode": f"P{random.randint(1000, 9999)}",
            "index": index,
            "State": random.randint(0, 1),
            "SysName": random.choice(["ENG", "ABS", "SRS", "TCU"])
        }
        sys_items.append(sys_item)
    return sys_items



if __name__ == "__main__":
    my_path = r"E:/adb_logcat/target_same"
    
    n = 500
    for i in range(n):
        create_random_package(my_path, i)