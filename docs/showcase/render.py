"""Render the Animation Production Skills showcase.

Install Pillow and FFmpeg. Run: python docs/showcase/render.py --output ./video-output
On Windows, the default narration uses an installed System.Speech voice.
On other systems use --silent for the captioned cut.
"""

import argparse
from functools import lru_cache
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFont, ImageOps


W, H, FPS = 1280, 720, 24
INK = "#f6f3ff"
MUTED = "#b2bdde"
DIM = "#7889b2"
PANEL = "#141c36"
LINE = "#36466c"
PURPLE = "#bba5ff"
CYAN = "#64e9e0"
YELLOW = "#ffd58a"
GREEN = "#8ee6aa"
PINK = "#fb9eb8"

SCENES = (
    ("01 / INTRO", ("Animation", "Production Skills"), ("For Codex and Claude Code.",),
     "Meet Animation Production Skills, a workflow for making visual explainers with Codex or Claude Code.", PURPLE, 6.8),
    ("02 / THE WORKFLOW", ("Start with", "the story."), ("Choose a format and visual style.", "Then find the right tools."),
     "Start with the audience and the result you want. The entry skill recommends an animation style and the tools that fit.", CYAN, 8.1),
    ("03 / AT WORK", ("Show how", "AI helps."), ("Employee showcase", "Use a familiar example to explain the value."),
     "For an employee showcase, start with a familiar problem, show what the AI does, and make the next step clear.", YELLOW, 7.9),
    ("04 / AT HOME", ("Let the", "story branch."), ("Children's story", "Make a video or add clickable choices."),
     "For a children's story, make a short animation or build a browser story with choices, like helping a seed find water.", GREEN, 8.2),
    ("05 / THE TOOLKIT", ("Pick the", "right toolkit."), ("4 production workflows", "10 repositories  /  41 example prompts"),
     "Four specialist skills cover stylized motion, Three.js, Blender, and maths diagrams. Ten repositories and forty-one prompts give you examples to adapt.", PINK, 9.2),
    ("06 / GET STARTED", ("Install and", "start a brief."), ("Animation Production Skills", "Available on GitHub  /  v1.0.0"),
     "Install the five skill folders, then run Video Production in Codex or Claude Code to start your first brief.", PURPLE, 8.2),
)


def rgb(hex_color):
    return tuple(int(hex_color[index:index + 2], 16) for index in (1, 3, 5))


def blend(a, b, amount):
    return tuple(round(first + (second - first) * amount) for first, second in zip(rgb(a), rgb(b)))


def clamp(value):
    return max(0.0, min(1.0, value))


def ease(value):
    return 1 - (1 - clamp(value)) ** 3


@lru_cache(maxsize=None)
def font(size, kind="normal"):
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    names = {
        "normal": ("segoeui.ttf", "DejaVuSans.ttf"),
        "bold": ("segoeuib.ttf", "DejaVuSans-Bold.ttf"),
        "mono": ("consola.ttf", "DejaVuSansMono.ttf"),
    }[kind]
    for name in names:
        for candidate in (str(windows / name), name):
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def text(draw, x, y, value, size, color=INK, kind="normal", anchor=None):
    draw.text((x, y), value, fill=color, font=font(size, kind), anchor=anchor)


def box(draw, xy, fill=PANEL, outline=LINE, radius=17, width=1):
    draw.rounded_rectangle(xy, radius, fill, outline, width)


def wrap(draw, value, size, max_width):
    lines, line = [], ""
    for word in value.split():
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=font(size)) > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    lines.append(line)
    if len(lines) == 2:
        words = value.split()
        def line_width(words):
            return draw.textlength(" ".join(words), font=font(size))
        splits = [i for i in range(1, len(words))
                  if max(line_width(words[:i]), line_width(words[i:])) <= max_width]
        if splits:
            i = min(splits, key=lambda n: abs(line_width(words[:n]) - line_width(words[n:])))
            return [" ".join(words[:i]), " ".join(words[i:])]
    return lines


def circle(draw, x, y, r, color, outline=None, width=1):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=outline, width=width)


@lru_cache(maxsize=1)
def background():
    tiny = Image.new("RGB", (160, 90))
    px = tiny.load()
    for y in range(90):
        for x in range(160):
            light = max(0, 1 - math.hypot((x - 113) / 128, (y - 39) / 88)) ** 1.6
            px[x, y] = (int(10 + light * 13), int(15 + light * 12), int(32 + light * 28))
    base = tiny.resize((W, H), Image.Resampling.BICUBIC)
    draw = ImageDraw.Draw(base)
    for x in range(648, 1222, 24):
        for y in range(102, 574, 24):
            draw.point((x, y), fill="#364162")
    return base


def iso_block(draw, x, y, width, height, accent):
    depth = int(width * 0.30)
    half = width // 2
    draw.polygon([(x-half, y), (x, y+depth), (x, y+depth+height), (x-half, y+height)],
                 fill=blend("#1a224a", accent, .29))
    draw.polygon([(x+half, y), (x, y+depth), (x, y+depth+height), (x+half, y+height)],
                 fill=blend("#28375d", accent, .52))
    draw.polygon([(x-half, y), (x, y-depth), (x+half, y), (x, y+depth)],
                 fill=blend("#34466c", accent, .77), outline=accent, width=2)


def intro_art(draw, t):
    # Isometric tiles represent the authoring workflow and carry a travelling signal.
    points = [(754, 370), (913, 281), (1075, 367)]
    draw.line(points, fill="#586a9b", width=5)
    for index, ((x, y), accent) in enumerate(zip(points, (CYAN, PURPLE, PINK))):
        iso_block(draw, x, y + 17 - round(35 * ease(t * 2.2 - index * .23)), 126, 48, accent)
    phase = (t / 3.6) % 1
    segment = min(1, int(phase * 2))
    frac = phase * 2 - segment
    x, y = (points[segment][axis] * (1-frac) + points[segment+1][axis] * frac for axis in (0, 1))
    circle(draw, x, y-19, 8, INK)
    for x, label in zip((754, 913, 1075), ("BRIEF", "STYLE", "BUILD")):
        text(draw, x, 454, label, 17, MUTED, "mono", "mm")
    box(draw, (819, 501, 1010, 537), fill="#202750", outline="#4b5082")
    text(draw, 915, 519, "SKILL SET  /  v1.0.0", 15, PURPLE, "mono", "mm")


def workflow_art(draw, t):
    for i, (title, sub) in enumerate((
        ("01  BRIEF", "Audience and outcome"),
        ("02  STYLE", "Recommend an animation"),
        ("03  BUILD", "Use the matching workflow"),
    )):
        x = 685 + round(30 * (1 - ease(t * 1.6 - i * .26)))
        y = 188 + i * 111
        active = min(2, int(t / 2.25)) == i
        box(draw, (x, y, x + 464, y + 86), fill="#1d3451" if active else PANEL,
            outline=CYAN if active else LINE, width=2 if active else 1)
        text(draw, x+22, y+12, title, 16, CYAN, "mono")
        text(draw, x+22, y+36, sub, 25, INK, "bold")
        circle(draw, x+425, y+43, 7, CYAN if active else LINE)


def work_art(draw, t):
    x, y = 675, 171
    box(draw, (x, y, 1168, 511), fill="#131c35", outline="#657397", radius=22)
    for i, accent in enumerate((PINK, YELLOW, GREEN)):
        circle(draw, x+23+i*16, y+22, 4, accent)
    text(draw, x+474, y+15, "ILLUSTRATIVE SCREENS", 13, YELLOW, "mono", "ra")
    draw.line((x, y+44, 1168, y+44), fill=LINE)
    rows = (
        ("ASK", "How do I request access?"),
        ("ANSWER", "Start with the access policy."),
        ("NEXT STEP", "Open the request form"),
    )
    for i, (label, copy) in enumerate(rows):
        yy = y + 64 + i * 78
        active = t >= .45 + 1.45*i
        box(draw, (x+20, yy, 1148, yy+64), fill="#29354e" if active else "#171e34",
            outline="#5c5b61" if active else "#283554", radius=11)
        text(draw, x+37, yy+8, label, 13, YELLOW if active else DIM, "mono")
        text(draw, x+37, yy+27, copy, 23, INK if active else DIM, "bold")


def story_art(draw, t):
    box(draw, (672, 170, 1172, 511), fill="#162b31", outline="#3e756d", radius=22)
    draw.polygon([(687, 377), (795, 300), (925, 382), (1041, 307), (1156, 374), (1156, 474), (687, 474)], fill="#25494d")
    draw.polygon([(687, 411), (812, 358), (940, 427), (1078, 358), (1156, 396), (1156, 477), (687, 477)], fill="#30594f")
    circle(draw, 1067, 244, 29, "#e4bb72")
    sway = round(4 * math.sin(t * 2))
    draw.line((923, 382, 923+sway, 299), fill=GREEN, width=6)
    draw.ellipse((880+sway, 301, 924+sway, 324), fill="#9be9a6")
    draw.ellipse((925+sway, 286, 975+sway, 313), fill="#5ab989")
    draw.ellipse((908, 373, 938, 391), fill="#d8af79")
    for x, caption in ((696, "Follow the drop"), (929, "Look under a leaf")):
        active = (x == 696 and t > 2.6)
        box(draw, (x, 439, x+219, 488), fill="#a5eab6" if active else "#203e46",
            outline=GREEN, radius=12)
        text(draw, x+109, 463, caption, 18, "#12332b" if active else INK, "bold", "mm")
    if t > 2.6:
        xx, yy = 741, 350+round(11*math.sin(t*2.1))
        draw.polygon([(xx, yy-16), (xx-10, yy+3), (xx+10, yy+3)], fill=CYAN)
        circle(draw, xx, yy+3, 10, CYAN)


def toolkit_art(draw, t):
    cards = (
        ("01", "Stylized motion", "Isometric / pixel / stories", CYAN),
        ("02", "Three.js", "Web 3D / data charts", PURPLE),
        ("03", "Blender", "Editable 3D scenes", YELLOW),
        ("04", "Maths diagrams", "Proofs / explanations", PINK),
    )
    for i, (number, title, subtitle, accent) in enumerate(cards):
        x = 658 + (i % 2) * 270
        y = 173 + (i // 2) * 151 + round(16*(1-ease(t*1.4-i*.22)))
        box(draw, (x, y, x+253, y+133), fill=PANEL, outline=LINE, radius=14)
        text(draw, x+18, y+17, number, 17, accent, "mono")
        text(draw, x+18, y+45, title, 23, INK, "bold")
        text(draw, x+18, y+87, subtitle, 16, MUTED)
        draw.line((x+18, y+113, x+54, y+113), fill=accent, width=3)


def install_art(draw, t):
    for index, (app, command, color) in enumerate((
        ("CODEX", "$video-production", CYAN),
        ("CLAUDE CODE", "/video-production", PURPLE),
    )):
        x, y = 674, 184 + index * 125
        box(draw, (x, y, 1170, y+102), fill=PANEL, outline=LINE, radius=15)
        text(draw, x+23, y+17, app, 15, color, "mono")
        text(draw, x+23, y+42, command, 30, INK, "mono")
        if int(t*2.6) % 2 == 0 and index == 0:
            draw.rectangle((x+331, y+49, x+337, y+75), fill=color)
    text(draw, 922, 465, "leowjs / animation-production-skills", 20, MUTED, "mono", "mm")


ART = (intro_art, workflow_art, work_art, story_art, toolkit_art, install_art)


def draw_frame(index, t, duration, captions=True, poster=False):
    label, title, details, caption, accent, _ = SCENES[index]
    frame = background().copy()
    draw = ImageDraw.Draw(frame)
    text(draw, 73, 44, "ANIMATION PRODUCTION", 15, MUTED, "mono")
    text(draw, 1205, 44, "CODEX  /  CLAUDE CODE", 15, MUTED, "mono", "ra")
    draw.line((73, 73, 1205, 73), fill=LINE)
    text(draw, 75, 141, label, 19, accent, "mono")
    offset = round(13 * (1 - ease(t * 4)))
    for i, line in enumerate(title):
        text(draw, 70, 184 + 83 * i + offset, line, 72, INK, "bold")
    draw.rounded_rectangle((76, 385, 133, 390), 2, accent)
    for i, line in enumerate(details):
        text(draw, 75, 413 + 35 * i, line, 24, MUTED)
    ART[index](draw, t)
    if poster:
        box(draw, (73, 609, 335, 662), fill=PURPLE, outline=None, radius=23)
        draw.polygon([(94, 625), (94, 646), (113, 636)], fill="#17213e")
        text(draw, 128, 619, "WATCH SHOWCASE", 21, "#17213e", "bold")
    elif captions:
        lines = wrap(draw, caption, 23, 1004)
        box(draw, (108, 572, 1172, 651), fill="#090f20", outline="#29375a", radius=14)
        y = 610 - (len(lines) - 1) * 14
        for i, line in enumerate(lines):
            text(draw, W//2, y + i*28, line, 23, INK, "normal", "mm")
    for i in range(len(SCENES)):
        start = 75 + i * 190
        end = start + 180
        draw.rounded_rectangle((start, 676, end, 680), 2, LINE)
        part = 1.0 if i < index else clamp(t/duration) if i == index else 0.0
        if part > 0:
            draw.rounded_rectangle((start, 676, start + round(180*part), 680), 2, accent)
    return frame


SPEECH_SCRIPT = """
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$job = Get-Content -LiteralPath $env:ANIMATION_SHOWCASE_SPEECH_JOB -Raw | ConvertFrom-Json
$voice = [System.Speech.Synthesis.SpeechSynthesizer]::new()
if ($voice.GetInstalledVoices().VoiceInfo.Name -contains 'Microsoft Zira Desktop') {
    $voice.SelectVoice('Microsoft Zira Desktop')
}
$voice.Rate = 0
foreach ($cue in $job) {
    $voice.SetOutputToWaveFile($cue.path)
    $voice.Speak($cue.text)
    $voice.SetOutputToNull()
}
$voice.Dispose()
"""


def narrate(work, silent):
    if silent:
        return [math.ceil(scene[-1]*FPS) for scene in SCENES], None
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if os.name != "nt" or not shell:
        raise RuntimeError("Windows System.Speech is required for narration. Use --silent for captions only.")
    manifest = work / "speech.json"
    script = work / "speech.ps1"
    wavs = [work / f"voice-{i}.wav" for i in range(len(SCENES))]
    manifest.write_text(json.dumps([{"text": s[3], "path": str(p)} for s, p in zip(SCENES, wavs)]), encoding="utf-8")
    script.write_text(SPEECH_SCRIPT, encoding="utf-8")
    env = dict(os.environ, ANIMATION_SHOWCASE_SPEECH_JOB=str(manifest))
    subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File", str(script)], env=env, check=True)
    cuts, track = [], work / "voice.wav"
    with wave.open(str(wavs[0]), "rb") as sample:
        channels, width, rate = sample.getnchannels(), sample.getsampwidth(), sample.getframerate()
    with wave.open(str(track), "wb") as result:
        result.setparams((channels, width, rate, 0, "NONE", "not compressed"))
        bytes_per_sample = channels * width
        elapsed_samples = 0
        elapsed_frames = 0
        for i, path in enumerate(wavs):
            with wave.open(str(path), "rb") as cue:
                if (cue.getnchannels(), cue.getsampwidth(), cue.getframerate()) != (channels, width, rate):
                    raise RuntimeError("Narration uses inconsistent audio settings")
                samples = cue.getnframes()
                pre = round(rate * .24)
                frames = math.ceil(max(SCENES[i][-1], samples/rate + .62)*FPS)
                elapsed_frames += frames
                cut_sample = round(elapsed_frames*rate/FPS)
                post = cut_sample - elapsed_samples - pre - samples
                result.writeframes(b"\0"*(pre*bytes_per_sample))
                result.writeframes(cue.readframes(samples))
                result.writeframes(b"\0"*(post*bytes_per_sample))
                elapsed_samples = cut_sample
                cuts.append(frames)
    return cuts, track


def previews(output):
    draw_frame(0, 1.75, 7, captions=False, poster=True).save(output / "showcase-cover.png", optimize=True)
    board = Image.new("RGB", (1280, 1080))
    for i in range(len(SCENES)):
        still = draw_frame(i, 3.6, SCENES[i][-1])
        still = ImageOps.contain(still, (640, 360))
        board.paste(still, ((i % 2)*640, (i // 2)*360))
    board.save(output / "storyboard.png", optimize=True)


def render(output, silent):
    with tempfile.TemporaryDirectory(prefix="animation-showcase-") as temp:
        cuts, audio = narrate(Path(temp), silent)
        dest = output / "animation-production-skills-showcase.mp4"
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
            "-pixel_format", "rgb24", "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "pipe:0",
        ]
        if audio:
            cmd += ["-i", str(audio), "-af", "loudnorm=I=-17:TP=-1.5:LRA=7", "-ar", "48000", "-c:a", "aac", "-b:a", "96k"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(dest)]
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as ffmpeg:
            for i, frames in enumerate(cuts):
                print(f"Rendering scene {i+1}: {frames/FPS:.2f}s", flush=True)
                for frame in range(frames):
                    ffmpeg.stdin.write(draw_frame(i, frame/FPS, frames/FPS).tobytes())
            ffmpeg.stdin.close()
            if ffmpeg.wait():
                raise RuntimeError("FFmpeg encode failed")
        print(f"{dest} ({sum(cuts)/FPS:.2f}s)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--silent", action="store_true")
    options = parser.parse_args()
    output = options.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    previews(output)
    if not options.preview_only:
        render(output, options.silent)


if __name__ == "__main__":
    main()
