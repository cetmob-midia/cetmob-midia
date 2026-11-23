"""Renderiza o Reel: um MP4 por cena (30 fps, 1080x1920), concat -c copy, trilha silenciosa."""
import asyncio, pathlib, subprocess, os
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).parent
FPS = 30
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto((D / "exemplo_reel01.html").as_uri())
        await pg.wait_for_timeout(600)
        scenes = await pg.evaluate("SCENES")
        files = []
        for sid, dur in scenes.items():
            tmp, out = D / f"_{sid}.tmp.mp4", D / f"{sid}.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                                   "-c:v", "mjpeg", "-i", "-", *ENC, str(tmp)], stdin=subprocess.PIPE)
            for i in range(round(dur * FPS)):
                await pg.evaluate(f"render('{sid}', {i / FPS})")
                ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
            ff.stdin.close()
            if ff.wait() == 0:
                os.replace(tmp, out)
            files.append(out)
            print(sid, dur, "ok", flush=True)
        # capa: último quadro da cena 1
        await pg.evaluate("render('s1', 3.6)")
        await pg.screenshot(path=str(D / "capa.jpg"), type="jpeg", quality=92)
        await b.close()
    (D / "list.txt").write_text("".join(f"file '{f.name}'\n" for f in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "_video.mp4"], cwd=D, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "_video.mp4", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags", "+faststart",
                    "reel.mp4"], cwd=D, check=True)
    print("done")

asyncio.run(main())
