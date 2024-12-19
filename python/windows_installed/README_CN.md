# Windows 已安装程序工具

一个用于管理和比较不同 Windows 主机已安装程序的 Python 工具。

## 功能特点

- 获取当前主机已安装程序信息
- 比较不同主机之间的已安装程序
- 支持单机模式和多主机比较模式
- 导出结果为 CSV 格式
- 长时间操作显示进度条
- 交互式命令行界面

## 系统要求

- Python 3.x
- 所需包：
  - wmi
  - tqdm

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行脚本：
```bash
python installed.py
```

2. 选择操作模式：
   - 模式 1：获取当前主机安装程序信息
   - 模式 2：比较不同主机安装程序信息
   - 模式 3：退出

3. 按照交互提示完成操作

## 输出文件

- 单机模式：`installed_programs_YYYYMMDD.csv`
- 比较模式：`compare_result_[common/different]_YYYYMMDD_HHMMSS.csv`

## 许可证

MIT License

## 作者

Stein Gu