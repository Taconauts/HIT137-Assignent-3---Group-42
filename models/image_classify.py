# General image classifier for any image. No curated labels.
# Uses Transformers pipeline; returns [{"label": str, "score": float}, ...].

from .model_base import ModelBase
from transformers import pipeline
from PIL import Image, UnidentifiedImageError
from utils.mixins import TimestampMixin
from utils.decorators import timeit, ensure_path


class ImageClassify(ModelBase, TimestampMixin):  # multiple inheritance via mixin
    def __init__(self):
        super().__init__("Image Classification", "General top-k labels from a vision model.")
        self._clf = None
        self._last_stamp = None  # provenance tag from mixin

        # prefer ViT; fallback to ResNet; final fallback: default pipeline model
        for model_name in ["google/vit-base-patch16-224","microsoft/resnet-50",None,]:  # let pipeline choose
            try:
                self._clf = pipeline("image-classification", model=model_name) if model_name else pipeline("image-classification")
                break
            except Exception:
                self._clf = None

        if self._clf is None:
            raise RuntimeError("No image classification model available (transformers not installed?).")

    def _validate_image(self, path: str):
        # accept anything Pillow can read (jpg, png, webp, tiff, heic, …)
        try:
            img = Image.open(path)
            img.verify()
        except UnidentifiedImageError:
            raise ValueError("File is not a valid image.")
        except Exception as e:
            raise ValueError(f"Error opening image: {e}")

    @timeit
    @ensure_path
    def run(self, input_path: str, top_k: int = 5) -> list:
        # decorators: ensure_path checks existence; timeit logs duration
        self._validate_image(input_path)

        results = self._clf(input_path, top_k=top_k)
        # normalize labels (underscores → spaces)
        out = []
        for r in results:
            lbl = str(r.get("label", "")).replace("_", " ").strip()
            scr = float(r.get("score", 0.0))
            out.append({"label": lbl, "score": scr})

        self._last_stamp = self.stamp()  # record when run() executed (mixin)
        return out
