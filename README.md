# auto-ip-update
自动获取网上分享的优选ip 
# 优选IP自动采集与分发

## 项目简介

本项目可以自动从多个API接口抓取优选IP，格式化输出，并定时推送到GitHub仓库。你可以用来分享、同步、自动分发最新的优选IP，无需手动操作。

- **云端自动化**：GitHub Actions 每3小时自动抓取、更新一次，无需本地开机。
- **本地可用**：也可以在本地运行采集脚本，效果和云端一样。
- **格式统一**：输出格式和本地GUI工具一致，方便复制、导出、自动化使用。

## 目录结构

```
├── api_config.json                # API接口配置（根目录，必需）
├── 优选ip.txt                     # 自动生成的优选IP列表
├── ip_auto_update/
│   └── fetch_and_format_ip.py     # 自动采集脚本
└── .github/
    └── workflows/
        └── update-ip.yml          # GitHub Actions自动化配置
```

## 如何自定义API

1. 打开根目录下的 `api_config.json` 文件。
2. 按照已有格式，添加/修改/删除API地址和备注。
3. 保存后，无论是本地运行还是云端自动化，都会用最新的API列表。

## 如何本地运行

1. 安装依赖：
   ```bash
   pip install requests
   ```
2. 运行采集脚本：
   ```bash
   python ip_auto_update/fetch_and_format_ip.py
   ```
3. 运行后会在根目录生成/更新 `优选ip.txt` 文件。

## 如何云端自动运行（GitHub Actions）

1. 确保仓库有 `.github/workflows/update-ip.yml` 和 `ip_auto_update/fetch_and_format_ip.py`。
2. 每3小时GitHub会自动运行采集脚本，自动更新 `优选ip.txt`。
3. 你也可以在GitHub Actions页面手动触发一次。

## 常见问题
- **API接口失效/变更**：只需修改 `api_config.json`，无需改动代码。
- **依赖问题**：云端自动安装依赖，本地只需 `pip install requests`。
- **输出格式**：和本地GUI工具一致，方便自动化对接。

---

如有问题或建议，欢迎提issue或PR！ 
