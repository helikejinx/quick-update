package com.user.quickupdate;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;

/**
 * QuickUpdate - 一键秒开系统应用商店更新列表
 * 零后台驻留、零权限需求、全品牌自适应
 */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        boolean launched = false;
        PackageManager pm = getPackageManager();

        // 1. 小米 / 红米 (HyperOS / MIUI)
        if (isInstalled(pm, "com.xiaomi.market")) {
            launched = tryIntent(new Intent("com.xiaomi.market.UPDATE_APP_LIST"))
                    || tryUri("mimarket://update");
        }

        // 2. 荣耀 (MagicOS)
        if (!launched && isInstalled(pm, "com.hihonor.appmarket")) {
            launched = tryUri("honorappmarket://appUpdates")
                    || tryUri("market://updates");
        }

        // 3. OPPO / 一加 / realme (ColorOS)
        if (!launched && (isInstalled(pm, "com.heytap.market") || isInstalled(pm, "com.oppo.market"))) {
            launched = tryUri("heytapmarket://update")
                    || tryUri("oppomarket://update");
        }

        // 4. vivo / iQOO (OriginOS)
        if (!launched && isInstalled(pm, "com.bbk.appstore")) {
            launched = tryUri("vivomarket://app_update");
        }

        // 5. 三星 (One UI)
        if (!launched && isInstalled(pm, "com.sec.android.app.samsungapps")) {
            launched = tryUri("samsungapps://AppUpdates");
        }

        // 6. 通用兜底（如果上述未匹配，直接安全拉起对应市场的原生入口）
        if (!launched) {
            String[] markets = {
                "com.xiaomi.market", "com.hihonor.appmarket", "com.heytap.market",
                "com.oppo.market", "com.bbk.appstore", "com.sec.android.app.samsungapps",
                "com.android.vending"
            };
            for (String pkg : markets) {
                if (isInstalled(pm, pkg)) {
                    Intent launch = pm.getLaunchIntentForPackage(pkg);
                    if (launch != null) {
                        tryIntent(launch);
                        break;
                    }
                }
            }
        }

        // 执行完毕后立即退出，不占用任何后台资源
        finish();
    }

    private boolean isInstalled(PackageManager pm, String pkg) {
        try {
            pm.getPackageInfo(pkg, 0);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private boolean tryIntent(Intent intent) {
        try {
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private boolean tryUri(String uriStr) {
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(uriStr));
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
