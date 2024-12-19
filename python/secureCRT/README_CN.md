# SecureCRT 密码解密工具

这是一个用于解密 SecureCRT 会话配置文件中存储的密码的 Python 工具。

## 功能特点

- 支持搜索指定主机名的配置文件
- 支持两种 SecureCRT 密码加密方式的解密：
  - 传统加密方式（Blowfish CBC）
  - V2 加密方式（AES CBC）
- 自动定位 SecureCRT 配置文件目录
- 交互式操作界面

## 系统要求

- Python 3.x
- pycryptodome 库

## 安装依赖

```bash
pip install pycryptodome
```

## 使用方法

1. 运行脚本：
```bash
python cipher.py
```

2. 按提示输入要搜索的主机名（hostname）
3. 从搜索结果中选择要处理的配置文件
4. 查看解密后的密码

## 注意事项

- 仅支持 Windows 系统
- 需要有访问 SecureCRT 配置文件目录的权限
- 配置文件默认位置：`%APPDATA%\VanDyke\Config\Sessions`

## 技术细节

该工具支持两种解密方式：

1. 传统加密（SecureCRTCrypto）：
   - 使用 Blowfish CBC 模式
   - 使用固定的密钥对
   - UTF-16LE 编码

2. V2加密（SecureCRTCryptoV2）：
   - 使用 AES CBC 模式
   - 支持配置密码（Config Passphrase）
   - UTF-8 编码
   - 包含密码长度和SHA256校验

## 参考资料

- [SecureCRT 密码加密算法分析](https://blog.csdn.net/ly4983/article/details/131528552)

## 免责声明

本工具仅用于合法的配置文件恢复目的。使用者需要确保遵守相关法律法规和软件使用协议。

## License

MIT License
