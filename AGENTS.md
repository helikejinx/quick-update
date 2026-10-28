# Agent Guidelines for QuickUpdate

本文件为智能体在维护与开发 `quick-update` 项目时的开发规范。

## 1. 文档第一事实源
- 修改或排查任何逻辑前，优先阅读 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)。
- 厂商分发协议细节以 `docs/modules/market-dispatcher.md` 为依据。

## 2. 行为准则与绝对约束
- **严禁引入常驻与后台组件**：本项目必须保持“0 后台、用完即毁”，严禁引入任何 Service、JobScheduler、WorkManager 或常驻接收器。
- **严禁新增危险权限**：严禁在 `AndroidManifest.xml` 中添加网络权限、存储权限或设备状态权限。保持纯粹的透明跳板工具属性。
- **UI 纯粹性**：保持 `Theme.Translucent.NoTitleBar` 全透明配置，不新增多余的前台 UI 阻塞用户。
- **Git 操作规范**：严禁未经用户明确授权自动执行 commit 或 push。
