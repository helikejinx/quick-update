import os
import sys
import subprocess
import asyncio
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"D:\Projects\quick-update\video_assets"
OUTPUT_DIR = r"D:\Projects\quick-update\video_output"
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

SCENES = [
    {
        "id": 1,
        "tag": "痛点揭秘 · 为什么总是红点满天飞？",
        "title": "手机从来不自动更新？",
        "subtitle": "明明开了空闲+Wi-Fi，为何还是积压几十个更新？",
        "text": "你是不是也经常纳闷：明明开启了 Wi-Fi 闲时自动更新，为什么应用从来不更新，每次打开商店都堆了几十上百个小红点？",
        "cards": [
            ("🚨 待更新应用堆积如山", "系统常年显示：数十个应用等待更新..."),
            ("📉 自动更新形同虚设", "无论放多久，应用从来不会主动更新"),
            ("🤯 强迫症极其难受", "每次必须手动一个个点，极度心累")
        ],
        "badge_color": "#FF4D4F"
    },
    {
        "id": 2,
        "tag": "底层排查 · 调度器到底卡在哪里？",
        "title": "暗藏三大严苛硬性门槛",
        "subtitle": "深挖系统底层 JobScheduler，真相令人无语！",
        "text": "深挖底层调度才发现，厂商暗藏了三大严苛门槛：必须插着充电器、必须半夜凌晨两点到六点、还必须手机完全静止，只要漏掉一个就彻底罢工！",
        "cards": [
            ("🔌 必须处于充电状态", "Requires Charging: 只要没插充电线，任务直接挂起"),
            ("🌙 仅限凌晨深睡时段", "Timing Window: 严格锁定在凌晨 2:00 ~ 6:00 时间窗口"),
            ("🛑 必须进入 Deep Doze", "Device Idle: 手机必须长时间完全静止，轻微晃动即打断")
        ],
        "badge_color": "#FAAD14"
    },
    {
        "id": 3,
        "tag": "恶心体验 · 手动更新步步是坑",
        "title": "手动更新到底有多烦？",
        "subtitle": "每一步都在挑战耐心与注意力",
        "text": "而每次手动点进应用商店，不仅要等 5 秒恶心的摇一摇开屏广告，还要关掉乱七八糟的推荐弹窗，极其烦人！",
        "cards": [
            ("💢 恶心的开屏摇一摇", "稍微一动就误触跳转第三方电商平台"),
            ("💢 广告弹窗满天飞", "必须手动连关两三个全屏推广弹窗"),
            ("💢 路径深层繁琐", "商店主页 -> 我的 -> 应用升级 -> 手动点击全部更新")
        ],
        "badge_color": "#FF7A45"
    },
    {
        "id": 4,
        "tag": "开源神器 · QuickUpdate 闪亮登场",
        "title": "QuickUpdate 一键更新",
        "subtitle": "极简 8.8 KB，专治自动更新不干活！",
        "text": "为了彻底干掉繁琐，我们做了一款开源小神器——QuickUpdate 一键更新！整个安装包仅有 8.8 KB，零权限、零后台、零广告！",
        "cards": [
            ("📦 仅 8.8 KB 极致轻量", "纯原生极简构建，比一张表情包还要小几十倍"),
            ("🛡️ 0 权限声明 · 绝不越界", "无联网、无读取文件、无敏感权限，纯本地透明运行"),
            ("⚡ 0.01 秒极速响应", "透明跳板技术，呼起即退，零后台常驻")
        ],
        "badge_color": "#1890FF"
    },
    {
        "id": 5,
        "tag": "真机实测 · 小米 HyperOS 现场演示",
        "title": "戳一下，秒开直达！",
        "subtitle": "跳过所有开屏广告，瞬间拉起更新列表",
        "text": "在桌面戳一下图标，0.01 秒透明跳板直达系统更新列表，点击全部升级即刻搞定！小米、OPPO、vivo、荣耀、索尼等主流品牌全适配！",
        "cards": [],
        "badge_color": "#52C41A"
    },
    {
        "id": 6,
        "tag": "开源发布 · 免费获取与体验",
        "title": "现已全面开源发布！",
        "subtitle": "GitHub 与 JustToyBox 官网均可免费下载",
        "text": "项目现已在 GitHub 全面开源并发布 v1.1.0 正式版，纯粹极客手作，代码完全透明，快去下载体验吧！",
        "cards": [
            ("⭐ GitHub 开源项目", "https://github.com/helikejinx/quick-update"),
            ("📦 Releases v1.1.0 现已发布", "提供官方独立签名的轻量 APK，即下即用"),
            ("🌐 妙具盒官网高速直链", "JustToyBox 官网支持手机扫码一键直下")
        ],
        "badge_color": "#722ED1"
    }
]

async def generate_tts(text, output_path):
    import edge_tts
    communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
    await communicate.save(output_path)

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def create_scene_image(scene, output_path):
    W, H = 1080, 1920
    im = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    draw = ImageDraw.Draw(im)

    # Gradient background
    for y in range(H):
        r = int(15 + (y / H) * 20)
        g = int(23 + (y / H) * 25)
        b = int(42 + (y / H) * 35)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Decorative top glow
    draw.ellipse([-200, -200, 600, 600], fill=(24, 144, 255, 30))
    draw.ellipse([700, 400, 1300, 1000], fill=(114, 46, 209, 25))

    # Fonts
    f_tag = ImageFont.truetype(FONT_BOLD, 36)
    f_title = ImageFont.truetype(FONT_BOLD, 74)
    f_sub = ImageFont.truetype(FONT_REG, 38)
    f_card_t = ImageFont.truetype(FONT_BOLD, 42)
    f_card_d = ImageFont.truetype(FONT_REG, 34)
    f_caption = ImageFont.truetype(FONT_BOLD, 46)

    # Tag Badge
    badge_color = scene["badge_color"]
    draw.rounded_rectangle([70, 160, 1010, 236], radius=38, fill=(30, 41, 59, 220), outline=badge_color, width=3)
    draw.text((95, 175), scene["tag"], font=f_tag, fill=badge_color)

    # Main Title & Subtitle
    draw.text((70, 280), scene["title"], font=f_title, fill=(255, 255, 255))
    draw.text((70, 385), scene["subtitle"], font=f_sub, fill=(148, 163, 184))

    # Separator
    draw.line([(70, 460), (1010, 460)], fill=(51, 65, 85, 255), width=2)

    # Content Cards or Real Device Mockup
    if scene["id"] == 5:
        # Phone frame placeholder
        draw.rounded_rectangle(
            [305, 480, 775, 1500],
            radius=28,
            fill=(10, 15, 30, 255),
            outline=badge_color,
            width=4
        )
        draw.text((810, 800), "小米 HyperOS", font=f_tag, fill=(148, 163, 184))
        draw.text((810, 860), "1080P 真机实录", font=f_sub, fill=(52, 196, 26))
        draw.text((810, 1020), "0 毫秒透明跳板", font=f_tag, fill=(56, 189, 248))
        draw.text((810, 1080), "直达系统更新页", font=f_sub, fill=(255, 255, 255))
    else:
        card_y = 510
        card_h = 240
        gap = 40
        for title, desc in scene["cards"]:
            draw.rounded_rectangle(
                [70, card_y, 1010, card_y + card_h],
                radius=24,
                fill=(30, 41, 59, 240),
                outline=(51, 65, 85, 255),
                width=2
            )
            draw.rounded_rectangle(
                [70, card_y, 82, card_y + card_h],
                radius=6,
                fill=badge_color
            )
            draw.text((110, card_y + 40), title, font=f_card_t, fill=(241, 245, 249))
            draw.text((110, card_y + 120), desc, font=f_card_d, fill=(148, 163, 184))
            card_y += card_h + gap

    # Bottom Subtitle Banner
    draw.rounded_rectangle([60, 1550, 1020, 1820], radius=30, fill=(15, 23, 42, 245), outline=(56, 189, 248, 200), width=3)
    draw.text((90, 1575), "🎙️ AI 旁白解读", font=f_tag, fill=(56, 189, 248))
    
    words = scene["text"]
    line1 = words[:20]
    line2 = words[20:42] if len(words) > 20 else ""
    line3 = words[42:65] if len(words) > 42 else ""
    draw.text((90, 1635), line1, font=f_caption, fill=(255, 255, 255))
    if line2:
        draw.text((90, 1695), line2, font=f_caption, fill=(255, 255, 255))
    if line3:
        draw.text((90, 1755), line3, font=f_caption, fill=(203, 213, 225))

    im.convert("RGB").save(output_path, "PNG", quality=95)

async def main():
    print("=== 开始全自动制作短视频 ===")
    clip_files = []
    real_demo_path = os.path.join(ASSETS_DIR, "real_demo.mp4")
    
    for scene in SCENES:
        sid = scene["id"]
        print(f"\n[处理场景 {sid}/6] {scene['title']}")
        
        # 1. 生成语音
        audio_path = os.path.join(ASSETS_DIR, f"scene_{sid}.mp3")
        await generate_tts(scene["text"], audio_path)
        duration = get_audio_duration(audio_path)
        clip_duration = duration + 0.3
        print(f"  - 语音合成完成: {duration:.2f}s, 设定片段时长: {clip_duration:.2f}s")

        # 2. 生成配图
        img_path = os.path.join(ASSETS_DIR, f"scene_{sid}.png")
        create_scene_image(scene, img_path)
        print(f"  - 高清场景海报已生成: {img_path}")

        # 3. 渲染单场景视频
        clip_path = os.path.join(ASSETS_DIR, f"clip_{sid}.mp4")
        
        if sid == 5 and os.path.exists(real_demo_path):
            print(f"  - 正在合成真机录屏至场景 5...")
            cmd_render = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", img_path,
                "-ss", "0.3", "-i", real_demo_path,
                "-i", audio_path,
                "-filter_complex",
                "[1:v]scale=450:1000:force_original_aspect_ratio=decrease,pad=450:1000:(ow-iw)/2:(oh-ih)/2:black[phone];"
                "[0:v][phone]overlay=315:490:shortest=0[v]",
                "-map", "[v]",
                "-map", "2:a",
                "-c:v", "libx264",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-t", f"{clip_duration:.2f}",
                clip_path
            ]
        else:
            cmd_render = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", img_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-t", f"{clip_duration:.2f}",
                "-vf", "scale=1080:1920,setsar=1",
                clip_path
            ]
            
        subprocess.run(cmd_render, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        print(f"  - 视频片段渲染完成: {clip_path}")
        clip_files.append(clip_path)

    # 4. 拼接所有片段
    concat_list_path = os.path.join(ASSETS_DIR, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for cp in clip_files:
            f.write(f"file '{cp}'\n")

    final_mp4 = os.path.join(OUTPUT_DIR, "QuickUpdate_一键更新介绍.mp4")
    print(f"\n[最终合成] 正在合并全片至: {final_mp4}")
    
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        final_mp4
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    
    total_dur = get_audio_duration(final_mp4)
    file_size_mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print("==========================================")
    print(f"🎉 视频制作大功告成！")
    print(f"输出文件: {final_mp4}")
    print(f"总时长: {total_dur:.1f} 秒")
    print(f"文件大小: {file_size_mb:.2f} MB")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(main())
