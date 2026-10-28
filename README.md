# QuickUpdate (一键更新)

> 🚀 **12 KB 超轻量级安卓小工具**：秒开各大手机厂商应用商店的“应用更新列表”，跳过开屏广告与推荐流，实现真正的一键更新。

---

## 💡 为什么需要它？

目前主流安卓手机（小米、OPPO、vivo、荣耀等）的系统自带“自动更新”机制普遍存在以下痛点：
1. **隐形门槛极高**：系统底层调度通常强制要求 **【插着充电器 + 凌晨深睡时段（2:00~6:00）+ 手机完全静止（Deep Doze）】**；
2. **只要有一个条件不满足，自动更新就会无限期推迟**，导致手机常年积压几十甚至上百个待更新应用；
3. 手动更新又极其繁琐：必须点进应用商店 → 等待几秒开屏摇一摇广告 → 关掉首页弹窗 → 切换到“我的” → 找到“应用更新”。

**QuickUpdate** 为解决这一痛点而生：在桌面放一个极简图标，点击瞬间直达【全部升级】页面，省去所有冗余步骤。

---

## ✨ 核心特性

* **🚀 0 毫秒启动**：采用透明跳板技术（Transparent Trampoline），启动耗时不到 10 毫秒，用完即毁。
* **🛡️ 纯粹安全**：
  * **0 权限声明**：无需网络权限、无需存储权限、无需设备信息，完全透明。
  * **0 后台驻留**：呼起系统商店后立即 `finish()` 退出进程，不消耗任何电量与内存。
* **📱 厂商应用商店适配（实测状态）**：
  * **小米 / 红米 (Xiaomi / Redmi / POCO)**：HyperOS / MIUI 专属协议直达【已真机实测通过】。
  * **索尼 / 魅族 (Sony Xperia / Meizu Flyme)**：Flyme 应用中心专属协议直达【已真机实测通过】。
  * **OPPO / 一加 / realme**：ColorOS 软件商店专属协议直达【待真机验证】。
  * **vivo / iQOO**：OriginOS 应用商店专属协议直达【待真机验证】。
  * **荣耀 (Honor)**：MagicOS 荣耀应用市场直达【待真机验证】。
  * **三星 (Samsung)**：One UI Galaxy Store 直达【待真机验证】。
  * **通用兜底**：智能识别本地预装的官方市场，安全唤醒。
  > ⚠️ **注意**：本项目不支持华为及 HarmonyOS（包括鸿蒙纯血系统 HarmonyOS NEXT 及华为应用市场生态）。
* **📦 极简轻量**：整包体积仅约 **12 KB**（比一张聊天截图还小）。

---

## 🛠️ 实现原理

```
[ 用户点击桌面图标 ]
         │
         ▼
[ QuickUpdate (Transparent Activity) ]
         │
         ├─ 1. 检测本地系统预装的应用商店品牌 (Xiaomi/OPPO/vivo/Honor/Samsung...)
         ├─ 2. 构造专属更新 Intent / Deep Link (如 `com.xiaomi.market.UPDATE_APP_LIST`)
         ├─ 3. 向系统 AMS 抛出直达意图，直冲更新界面
         │
         ▼
[ 立即执行 finish() 销毁自身，0 后台驻留 ]
```

---

## 📥 下载安装

1. 前往本项目的 [Releases](../../releases) 页面下载最新版 `QuickUpdate.apk`；
2. 在手机上直接安装即可；
3. 安装完成后，桌面上会直接生成专属的 **【一键更新】** 图标，点击即可秒开更新列表。

---

## 🔨 自行编译

如果你想自行编译修改源码：

```bash
git clone https://github.com/helikejinx/quick-update.git
cd quick-update
./gradlew assembleRelease
```

编译产物位于 `app/build/outputs/apk/release/`。

---

## 📄 开源许可

本项目遵循 [MIT License](LICENSE) 开源协议。
