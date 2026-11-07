"""Divide cada clip en trozos de voz (entre silencios) y transcribe cada trozo por separado."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

crudos, salida = Path(sys.argv[1]), Path(sys.argv[2])
salida.mkdir(parents=True, exist_ok=True)
wm = WhisperModel("medium", device="cpu", compute_type="int8")

def silencios(clip, th=-35, d=0.30):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(clip), "-vn", "-af", f"silencedetect=noise={th}dB:d={d}",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(ini, fin + [None] * (len(ini) - len(fin))))

for clip in sorted(crudos.glob("*.MP4")):
    pcm = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(clip), "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    dur = len(audio) / 16000
    sil = [(a, b if b else dur) for a, b in silencios(clip)]
    # trozos de voz = complemento de los silencios
    voz, t = [], 0.0
    for a, b in sil:
        if a - t > 0.12: voz.append((t, a))
        t = b
    if dur - t > 0.12: voz.append((t, dur))
    trozos = []
    for i, (a, b) in enumerate(voz):
        seg = audio[int(max(0, a - 0.15) * 16000):int(min(dur, b + 0.15) * 16000)]
        res, _ = wm.transcribe(seg, language="es", word_timestamps=True, condition_on_previous_text=False,
                               beam_size=5, initial_prompt="IA, Claude, Airbnb, SWAT, Estados Unidos, USA Today, Google, Gemini, Cursor, India, Corea del Sur, hackers, bancos.")
        off = max(0, a - 0.15)
        words = [{"w": w.word.strip(), "s": round(off + w.start, 3), "e": round(off + w.end, 3)}
                 for s in res for w in (s.words or []) if w.word.strip()]
        trozos.append({"i": i, "s": round(a, 3), "e": round(b, 3), "texto": " ".join(w["w"] for w in words), "palabras": words})
    (salida / f"{clip.stem}.json").write_text(json.dumps(trozos, ensure_ascii=False, indent=1))
    print(f"\n=== {clip.stem[18:22]} ({dur:.1f}s)")
    for tr in trozos:
        print(f"  #{tr['i']:<2} {tr['s']:6.2f}-{tr['e']:6.2f}  {tr['texto']}")
