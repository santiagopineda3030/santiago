"""Como trozos.py, pero corta los trozos con el detector de VOZ (Silero) y no por silencio:
sirve cuando se graba en un lugar con ruido de fondo (centro comercial, calle).
Uso: python3 trozos_vad.py <carpeta_crudos> <salida/trozos>"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.vad import VadOptions, get_speech_timestamps
crudos, salida = Path(sys.argv[1]), Path(sys.argv[2]); salida.mkdir(parents=True, exist_ok=True)
wm = WhisperModel("medium", device="cpu", compute_type="int8")
prompt = open(Path(__file__).with_name("trozos.py")).read().split('initial_prompt="')[1].split('"')[0]
for clip in sorted(crudos.glob("*.MP4")):
    pcm = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(clip), "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    ts = get_speech_timestamps(audio, VadOptions(threshold=0.5, min_silence_duration_ms=350, speech_pad_ms=60))
    voz = []
    for t in ts:
        a, b = t["start"] / 16000, t["end"] / 16000
        if voz and a - voz[-1][1] < 0.35: voz[-1] = (voz[-1][0], b)
        else: voz.append((a, b))
    trozos = []
    for i, (a, b) in enumerate(voz):
        seg = audio[int(max(0, a - 0.1) * 16000):int((b + 0.1) * 16000)]
        res, _ = wm.transcribe(seg, language="es", word_timestamps=True, condition_on_previous_text=False, beam_size=5,
                               initial_prompt=prompt, vad_filter=False)
        off = max(0, a - 0.1)
        words = [{"w": w.word.strip(), "s": round(off + w.start, 3), "e": round(off + w.end, 3)}
                 for s in res for w in (s.words or []) if w.word.strip()]
        trozos.append({"i": i, "s": round(a, 3), "e": round(b, 3), "texto": " ".join(w["w"] for w in words), "palabras": words})
        print(f"  #{i:<3} {a:7.2f}-{b:7.2f}  {trozos[-1]['texto']}", flush=True)
    (salida / f"{clip.stem}.json").write_text(json.dumps(trozos, ensure_ascii=False, indent=1))
