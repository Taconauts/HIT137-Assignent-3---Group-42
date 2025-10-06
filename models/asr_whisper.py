# Whisper ASR (supports wav/mp3/m4a/mp4 via ffmpeg). Returns plain text.

from .model_base import ModelBase
from transformers import pipeline
from utils.mixins import TimestampMixin
from utils.decorators import timeit, ensure_path
import os, shutil, urllib.request, zipfile, tempfile, subprocess


def _ensure_ffmpeg():
    # download a minimal static build if ffmpeg isn't in PATH
    if shutil.which("ffmpeg"):
        return
    print("FFmpeg not found — downloading minimal build...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    tmp_zip = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")
    urllib.request.urlretrieve(url, tmp_zip)

    extract_path = os.path.join(tempfile.gettempdir(), "ffmpeg_temp")
    with zipfile.ZipFile(tmp_zip, "r") as z:
        z.extractall(extract_path)

    bin_dir = None
    for root, dirs, files in os.walk(extract_path):
        if "ffmpeg.exe" in files:
            bin_dir = root
            break
    if not bin_dir:
        raise EnvironmentError("Failed to locate ffmpeg.exe after extraction.")

    os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL)  # verify


class ASRWhisper(ModelBase, TimestampMixin):  # multiple inheritance via mixin
    def __init__(self):
        _ensure_ffmpeg()
        super().__init__("Speech-to-Text", "Transcribes audio/video to text using Whisper tiny.")
        self._asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
        self._last_stamp = None  # provenance tag from mixin

    @timeit
    @ensure_path
    def run(self, input_path: str) -> str:
        # decorators: ensure_path checks existence; timeit logs duration
        result = self._asr(input_path, return_timestamps=True)  # handles long clips (>30s)
        text = result.get("text") if isinstance(result, dict) else str(result)
        self._last_stamp = self.stamp()  # record when run() executed (mixin)
        return text
