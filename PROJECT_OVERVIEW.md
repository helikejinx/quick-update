---
document_type: project-overview
status: current
verification: verified_by_code
last_verified: 2026-10-28
---

# QuickUpdate (一键更新) 项目总览

## 项目目标

解决主流安卓手机系统自带“自动更新”策略过于严苛（要求充电 + 凌晨深睡 + 手机静止）导致应用更新长期积压的痛点。通过超轻量级（~12 KB）无界面跳板应用，在桌面一键秒开各品牌系统应用商店的“应用更新列表”，跳过开屏广告与推荐流。

## 构建单元与技术栈

- **构建单元**：原生 Android Application (`:app`)。
- **语言与底层环境**：Java 8，Android SDK 30+，无第三方冗余依赖。
- **界面与主题**：`Theme.Translucent.NoTitleBar` 全透明主题，`excludeFromRecents="true"` 避免残留在多任务卡片。
- **权限与资源占用**：
  - **零权限**：无需网络、存储、手机识别码等任何危险权限。
  - **零常驻**：唤起系统商店后立即在 `onCreate` 中触发 `finish()` 退出进程。
- **核心入口**：[`MainActivity.java`](file:///D:/Projects/quick-update/app/src/main/java/com/user/quickupdate/MainActivity.java)

## 运行架构

采用透明跳板（Transparent Trampoline）调度架构：
1. **意图接收**：用户点击桌面图标启动 `MainActivity`。
2. **厂商适配与探测**：通过 `PackageManager` 依次核验主流安卓厂商（小米、荣耀、OPPO、vivo、三星、Google Play）应用商店包名存在性。
3. **精准 DeepLink 调度**：优先构造私有协议或更新 Action；若特定协议拉起失败，则安全降级到常规市场启动页。当前小米（MIUI / HyperOS）已实测验证通过，其余品牌为社区协议方案（待真机进一步回归验证）。
4. **即刻自毁**：调用 `finish()` 销毁 Activity 并退出，全过程通常小于 10 毫秒。

## 模块地图

| 模块 | 职责 | 代码位置 | 文档 | 状态 |
|---|---|---|---|---|
| **商店协议调度引擎** | 各大厂商市场包名检测、更新 Action 与私有 Scheme 派发、兜底容灾 | [`app/src/main/java/com/user/quickupdate/MainActivity.java`](file:///D:/Projects/quick-update/app/src/main/java/com/user/quickupdate/MainActivity.java) | [商店分发机制](docs/modules/market-dispatcher.md) | 小米实测通过，其余待真机验证 |
| **清单与配置** | 透明样式定义、无最近任务清单配置、极简图标资源 | [`app/src/main/AndroidManifest.xml`](file:///D:/Projects/quick-update/app/src/main/AndroidManifest.xml) | [应用清单](file:///D:/Projects/quick-update/app/src/main/AndroidManifest.xml) | 已实现 |

## 跨模块与平台契约

1. **协议支持矩阵**：
   - 小米/红米：`com.xiaomi.market.UPDATE_APP_LIST` / `mimarket://update`（实测已通过）
   - 荣耀：`honorappmarket://appUpdates`
   - OPPO/一加/realme：`heytapmarket://update` / `oppomarket://update`
   - vivo/iQOO：`vivomarket://app_update`
   - 三星：`samsungapps://AppUpdates`
   > [!IMPORTANT]
   > **系统兼容性说明**：本项目不支持华为及 HarmonyOS（包括鸿蒙纯血系统 HarmonyOS NEXT 及华为应用市场生态）。
2. **Flag 契约**：所有发出的 Intent 均显式携带 `Intent.FLAG_ACTIVITY_NEW_TASK`，确保拉起的目标市场处于独立任务栈。

## 文档索引

### 模块文档
- [商店分发机制](docs/modules/market-dispatcher.md)：厂商适配逻辑、DeepLink 协议与降级执行链。

## 构建与验证入口

- **构建 Release APK**：`./gradlew assembleRelease`
- **安装至手机**：`adb install -r app/build/outputs/apk/release/app-release.apk`
