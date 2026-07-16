import os
import sys
import json
import asyncio

# إجبار نظام ويندوز فوراً على استخدام الـ ProactorEventLoop في هذه العملية المستقلة! 💻🔥
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from app.services import upload_to_tiktok_real

async def main():
    if len(sys.argv) < 4:
        print("🔴 Missing arguments for independent uploader process.")
        sys.exit(1)
        
    video_path = sys.argv[1]
    title = sys.argv[2]
    cookies_str = sys.argv[3]
    proxy_str = sys.argv[4] if len(sys.argv) > 4 else "Direct Connection"

    try:
        cookies = json.loads(cookies_str)
    except Exception as parse_err:
        print(f"🔴 Cookies parsing failed: {parse_err}")
        sys.exit(1)

    print(f"🚀 [Process] Executing real upload for video path: {video_path}")
    
    # استدعاء دالة الرفع التي تحتوي على كود الـ Playwright بأمان تام
    await upload_to_tiktok_real(
        video_path=video_path,
        title=title,
        cookies=cookies,
        proxy_str=proxy_str if proxy_str != "Direct Connection" else ""
    )

if __name__ == "__main__":
    asyncio.run(main())