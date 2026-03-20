import os
import json
import random
from datetime import datetime
from faker import Faker

fake = Faker('zh_CN')

def create_random_package(target_dir):
    root_path = os.path.abspath(target_dir)
    os.makedirs(root_path, exist_ok=True)

    # 生成12位随机数字文件夹名
    folder_id = "".join([str(random.randint(0, 9)) for _ in range(12)])
    full_folder_path = os.path.join(root_path, folder_id)
    os.makedirs(full_folder_path, exist_ok=True)

    module_list = ["防盗", "UI测试", "遥控测频", "ECU克隆", "系统扫描"]
    module_name = module_list[random.randint(0, len(module_list)-1)]
    # 年款：2010-2026 之间
    year_name = random.randint(2010, 2026)
    brand_name = fake.company_prefix()
    # 故障码数量
    dtc_count = random.randint(0, 50)
    # 维修状态
    repair_status = random.randint(0, 1)
    # 图片路径
    picList = []
    for _ in range(random.randint(0, 6)):
        i = random.randint(1, 11)
        picList.append(f"/storage/emulated/0/DCIM/Camera/pic{i}.png")
    
    # 时间 指定年月范围
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 3, 20)
    random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    time_format_a = random_date.strftime("%Y-%m-%d %H-%M-%S")
    time_format_b = random_date.strftime("%Y-%m-%d %H:%M:%S")

    # 格式：(模块名)年款_品牌_时间_故障码数量_维修状态.json
    file_name = f"({module_name}){year_name}_{brand_name}_{time_format_a}_{dtc_count}_{repair_status}.json"
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
          "index": 0,
          "State": 0,
          "SysName": "SysName"
        },
        {
          "StateText": "主动的/静态的",
          "Description": "部件保护启用",
          "FaultCode": "U1110100",
          "index": 1,
          "State": 0,
          "SysName": "SysName"
        },
        {
          "StateText": "主动的/静态的",
          "Description": "钥匙没有信号",
          "FaultCode": "B104B31",
          "index": 2,
          "State": 0,
          "SysName": "SysName"
        },
        {
          "StateText": "消极的/偶发的",
          "Description": "钥匙不可信信号",
          "FaultCode": "B104V89",
          "index": 3,
          "State": 0,
          "SysName": "SysName"
        },
        {
          "StateText": "消极的/偶发的",
          "Description": "钥匙编程不正确-遥控器",
          "FaultCode": "B128B00",
          "index": 4,
          "State": 0,
          "SysName": "SysName"
        }
      ],
      "vehiclePlate": "cheliangpaizhao",
      "VinName": folder_id,
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

    print(f"✅ 生成成功！")
    print(f"路径: {file_path}")


if __name__ == "__main__":
    my_path = r"E:/adb_logcat/target111"

    n = 10
    for _ in range(n):
        create_random_package(my_path)