import asyncio
import aiohttp
from aiohttp import web
import os
import urllib.parse
import socket

SAVE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../"))
os.makedirs(SAVE_DIR, exist_ok=True)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

async def handle_index(request):
    return web.FileResponse("./web/index.html")

async def handle_static(request):
    path = "./web/" + request.match_info["filename"]
    return web.FileResponse(path)

async def handle_upload(request):
    reader = await request.multipart()
    saved_files = []

    while True:
        part = await reader.next()
        if part is None:
            break

        if part.name == "files":
            filename = urllib.parse.unquote(part.filename)
            filename = os.path.basename(filename)
            save_path = os.path.join(SAVE_DIR, filename)

            print(f"Receiving: {filename}")

            with open(save_path, "wb") as f:
                while True:
                    chunk = await part.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)

            print(f"Saved: {filename}")
            saved_files.append(filename)

    if saved_files:
        return web.Response(text="Uploaded:<br>" + "<br>".join(saved_files),
                            content_type="text/html")
    else:
        return web.Response(text="No files uploaded.", content_type="text/html")


async def start_server():
    app = web.Application()

    app.router.add_get("/", handle_index)
    app.router.add_get("/{filename}", handle_static)
    app.router.add_post("/", handle_upload)

    runner = web.AppRunner(app)
    await runner.setup()

    ip = get_ip()
    site = web.TCPSite(runner, ip, 8000)
    await site.start()

    print(f"AirBridge Lite (AsyncIO) running at:")
    print(f"🌐 http://{ip}:8000")
    print(f"📁 Saving files to: {SAVE_DIR}")
    print("Press Ctrl + C to stop the server.")

    return runner   # return runner so we can shut it down


async def main():
    runner = await start_server()

    try:
        # Keep running until Ctrl + C
        while True:
            await asyncio.sleep(3600)

    except KeyboardInterrupt:
        print("\n🛑 Ctrl + C detected, stopping AirBridge Lite...")

    # Clean shutdown
    await runner.cleanup()
    print("🛑 AirBridge Lite stopped safely.")


if __name__ == "__main__":
    asyncio.run(main())
