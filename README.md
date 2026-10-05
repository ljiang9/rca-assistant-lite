# rca-assistant-lite

故障根因分析小工具。按现象引导 5 Why，列出候选根因与所需证据。规则驱动、零第三方依赖。

## 功能

- 内置常见现象（服务宕机/响应慢/数据错误）的 5-Why 链；
- 未知现象用通用 5-Why 模板兜底；
- 每个候选根因附带要收集的证据；
- 输出文本报告或 JSON。

## 快速开始

```bash
python3 cli.py "线上服务宕机了"
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，规则分析全部本地完成。

## 目录结构

```
rca-assistant-lite/
├── rca.py      # 现象库、5why、候选根因、报告
├── cli.py
├── tests/test_rca.py
├── README.md / LICENSE / .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
