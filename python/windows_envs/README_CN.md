# Windows 环境变量比较工具

一个用于导出和比较不同主机 Windows 环境变量的 Python 工具。

## 功能特点

- 导出本地 Windows 环境变量到 CSV
- 比较不同主机之间的环境变量
- 跟踪环境变量随时间的变化
- 支持多主机比较

## 系统要求

- Python 3.6+
- pandas
- csv 模块（内置）
- socket 模块（内置）

## 安装

1. 克隆此仓库
2. 安装所需包：

```bash
pip install -r requirements.txt
```

## 使用方法

使用 Python 运行脚本：

```bash
python environments.py
```

工具提供三个选项：
1. 导出本地环境变量
2. 比较主机环境变量
3. 退出

## 输出

工具会生成名为 `windows_environment.csv` 的 CSV 文件，包含：
- 主机名
- 变量名
- 变量值
- 变量类型

## 许可证

MIT 许可证

## 作者

Stein Gu