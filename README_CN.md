# scripts
各类用途的脚本集合

## Python 脚本

### SecureCRT 工具
**位置**: `python/secureCRT/`
- `cipher.py`: SecureCRT 会话密码解密工具
  - 支持传统（Blowfish）和 V2（AES）加密方式
  - 自动检测 SecureCRT 配置目录
  - 交互式命令行界面

### Windows 系统工具
**位置**: `python/windows_installed/`
- `installed.py`: Windows 已安装程序管理工具
  - 列出 Windows 系统中所有已安装程序
  - 比较不同主机之间的已安装程序
  - 导出结果为 CSV 格式
  - 具有进度条显示和交互式命令行界面

### Windows 环境变量比较工具
**位置**: `python/windows_envs/`
- `environments.py`: Windows 环境变量比较工具
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

## 目录结构
```
scripts/
├── python/
│   ├── secureCRT/
│   │   ├── cipher.py
│   │   ├── README.md
│   │   ├── README_CN.md
│   │   └── requirements.txt
│   ├── windows_installed/
│   │   ├── installed.py
│   │   ├── README.md
│   │   ├── README_CN.md
│   │   └── requirements.txt
│   └── windows_envs/
│       ├── environments.py
│       ├── README.md
│       ├── README_CN.md
│       └── requirements.txt
└── README.md
```

## 使用方法
每个脚本都有其独立的 README 文件，包含详细的使用说明。请参考具体脚本目录中的说明文档获取更多信息。

## 依赖要求
每个脚本的依赖项单独管理。请查看各脚本目录中的 `requirements.txt` 文件了解具体依赖要求。

## 许可证
MIT License 