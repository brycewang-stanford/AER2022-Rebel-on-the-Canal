# Data — 原始数据

来源：AEA openICPSR 复现包 **157781-V1**（Cao & Chen 2022, AER）。各数据的出处见 [Materials/157781-V1-Readme.pdf](../Materials/157781-V1-Readme.pdf)。

```text
Data/
├── Raw/       原始数据（本地已放置，约 398M）：rawrebellion.dta、CHGIS shape files、GTOPO30 高程、GAEZ 适宜度、Mann 气候等
├── Interim/   中间文件，由 Program/Clean/clean.do 生成
└── Final/     rebellion.dta 分析面板，由 Program/Clean/clean.do 生成
```

> 本文件夹内容已在 `.gitignore` 中排除，**不会上传到 GitHub**（仅保留本说明和空目录占位）：数据受 openICPSR 许可约束，且 `Raw/towns/town1911.dbf`（245M）超过 GitHub 单文件 100MB 上限。换机器时需从 openICPSR 重新下载并放回 `Data/Raw/`。
