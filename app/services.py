import os
import sys
import asyncio
import random
from playwright.async_api import async_playwright

async def human_type(element, text: str):
    """
    محاكاة الكتابة البشرية حرف حرف مع توقفات عشوائية قصيرة ✍️
    """
    for char in text:
        await element.type(char)
        await asyncio.sleep(random.uniform(0.1, 0.3)) # انتظار عشوائي بين الحروف

async def upload_to_tiktok_real(video_path: str, title: str, cookies: dict, proxy_str: str):
    """
    الرفع الحقيقي الآمن بـ Playwright مع حماية ضد البوتات وفترات انتظار عشوائية 🛡️⚙️
    """
    
    # 1. حل مشكلة الـ NotImplementedError على نظام التشغيل ويندوز 💻🔥
    if sys.platform == 'win32':
        try:
            # نضمن إن الـ Event Loop الحالي شغال بالـ ProactorPolicy اللي بيسمح بالـ Subprocesses
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            print("🟢 Active Thread Event Loop Policy forced to Proactor successfully!")
        except Exception as loop_err:
            print(f"⚠️ Warning while setting Proactor loop policy: {loop_err}")

    # 2. التأكد من وجود ملف الفيديو على الجهاز أولاً
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"⚠️ Video file not found at path: {video_path}")
        
    async with async_playwright() as p:
        # 3. تجهيز البروكسي وتفكيكه
        proxy_config = None
        if proxy_str and "://" in proxy_str:
            try:
                raw_proxy = proxy_str.split("//")[1]
                auth_and_ip = raw_proxy.split("@")
                if len(auth_and_ip) == 2:
                    auth = auth_and_ip[0].split(":")
                    ip_port = auth_and_ip[1]
                    proxy_config = {
                        "server": f"http://{ip_port}",
                        "username": auth[0],
                        "password": auth[1]
                    }
                else:
                    proxy_config = {"server": proxy_str}
            except Exception as e:
                print(f"⚠️ Proxy parsing failed, uploading directly: {e}")

        # 4. تشغيل المتصفح بشكل مرئي (headless=False) عشان نتفرج ونطمن 👀
        # مع تمرير وسيط لمنع كشف أوتوميشن المتصفح
        browser = await p.chromium.launch(
            headless=False, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        
        # تحضير الـ Context بالبروكسي والـ User Agent لتبدو كمتصفح طبيعي تماماً
        context = await browser.new_context(
            proxy=proxy_config,
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 5. زرع الكوكيز في الـ Context
        playwright_cookies = []
        for name, value in cookies.items():
            playwright_cookies.append({
                "name": name,
                "value": value,
                "domain": ".tiktok.com",
                "path": "/"
            })
        await context.add_cookies(playwright_cookies)
        
        page = await context.new_page()
        
        try:
            print(f"🚀 Navigating to TikTok Creator Center...")
            await page.goto("https://www.tiktok.com/creator-center/upload", timeout=60000)
            
            # انتظار عشوائي لمحاكاة تفكير البشر بعد فتح الصفحة
            await asyncio.sleep(random.uniform(4.0, 7.0))
            
            print(f"📥 Selecting video file: {video_path}")
            file_input = await page.wait_for_selector("input[type='file']", timeout=20000)
            await file_input.set_input_files(video_path)
            
            # انتظار عشوائي أثناء تحميل الفيديو
            print("⏳ Uploading video file to TikTok servers (simulating progress delay)...")
            await asyncio.sleep(random.uniform(8.0, 12.0))
            
            print(f"✍️ Writing Title with human-like typing...")
            caption_box = await page.wait_for_selector("div[contenteditable='true']", timeout=15000)
            await caption_box.click()
            
            # مسح أي نص افتراضي بذكاء
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # الكتابة كبشر
            await human_type(caption_box, title)
            
            # انتظار عشوائي قبل الضغط على زر النشر النهائي
            await asyncio.sleep(random.uniform(3.0, 6.0))
            
            print("🔘 Clicking Post Button...")
            post_button = await page.wait_for_selector("button:has-text('Post')", timeout=15000)
            
            # حيا الله المكنة! لو عايز تجرب "بدون ضغط فعلي" في أول مرة خوفاً من الحساب،
            # ممكن نعمل كومنت للسطر اللي تحت ده. لو واثق وجاهز دوس!
            await post_button.click()
            
            # انتظار أخير لرؤية شاشة النجاح
            await asyncio.sleep(10.0)
            print("🟢 Video Posted Successfully with Anti-Ban Guard! 🛡️")
            
        except Exception as e:
            print(f"🔴 Upload process encountered an error: {e}")
            raise e
            
        finally:
            await context.close()
            await browser.close()