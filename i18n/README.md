## Android项目国际化脚本

### 前置工作

**翻译excel文件格式**

| ID     | CN   | EN   | KR (Other Code...) |
| ------ | ---- | ---- | ------------------ |
| btn_ok | 确定 | OK   | 확인               |

> 第一行必须有表头
>
> 第一列必须为<string>标签的name值



**strings.xml格式** 

```
<string name="btn_ok">OK</string>
```



生成的`lack_translate_id.xlsx`：翻译文件中缺少这些ID，无法翻译，需手动替换



### 使用

```
python android_translate_string_by_excel.py --excel 'D:/DOC/平板界面文本 string完整版.xls' --project 'D:/AndroidStudioProjects/MyApplication' --lang 'fr' --exclude 'common' 'common-core'
```

> 参数说明：
>
> --excel：翻译文件绝对路径
>
> --project：待翻译Android项目绝对根路径
>
> --lang：带翻译的语言代码（对应excel表头）
>
> --exclude：忽略翻译的模块



### TODO

#### android_translate_string_by_excel.py

- [x] 优化搜索模块strings.xml方法：可视化搜索（添加进度条）
- [x] 添加搜索时排除模块strings.xml功能