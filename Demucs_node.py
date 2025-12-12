# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import random
import torch
import numpy as np
import logging
import folder_paths
from pathlib import Path
import torchaudio

from .demucs.api import Separator,save_audio
from .demucs.audio import pre_audio
node_cur_path = os.path.dirname(os.path.abspath(__file__))
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"


class Demucs_Loader:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "d_model": ("STRING", {"default": "htdemucs"}),
                "overlap": ("FLOAT", {"default": 0.25, "min": 0.01, "max": 1.0, "step": 0.01,}),
                "shifts": (
                    "INT", {"default": 1, "min": 1, "max": 4096, "step": 1, "display": "number"}),
                "split": ("BOOLEAN", {"default": True},),
            }
        }
    
    RETURN_TYPES = ("Demucs_MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "main_"
    CATEGORY = "Demucs"
    
    def main_(self, d_model,overlap,shifts,split):
        repo=None
        model = Separator(
            model=d_model,
            repo=repo,
            device=device,
            shifts=shifts,
            overlap=overlap,
            split=split,
            segment=None,
            jobs=0,
            callback=print
        )
        # out = args.out / args.name
        # out.mkdir(parents=True, exist_ok=True)
        logging.info("loading checkpoint done.")
        
        return (model,)


class Demucs_Sampler:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("Demucs_MODEL",),
                "audio": ("AUDIO",),
                "ext": (["mp3","flac","wav"],),
                "bits_per_sample": ([24, 16,],),
                "as_float": (["float32", "float16", ],),
                "clip_mode": (["rescale", "clamp", "tanh","none"],),
                "mp3_bitrate": (
                    "INT", {"default": 320, "min": 1, "max": 4096, "step": 1, "display": "number"}),
                "audio_save": ("BOOLEAN", {"default": True},),
                "preset": ([2,3,4,5,6,7],),
            },
        }
    
    RETURN_TYPES = ("AUDIO","AUDIO","AUDIO","AUDIO","AUDIO",)
    RETURN_NAMES = ("mixed","bass","drums","other","vocals",)
    FUNCTION = "main"
    CATEGORY = "Demucs"
    
    def main(self, model, audio, ext, bits_per_sample, as_float, clip_mode, mp3_bitrate,audio_save,preset):
        
        #pre input audio
        audio_file_prefix = ''.join(random.choice("0123456789abcdefg") for _ in range(6))
        file = os.path.join(folder_paths.get_input_directory(), f"audio_{audio_file_prefix}.{ext}")
        torchaudio.save(file, audio["waveform"].squeeze(0), audio["sample_rate"])
        
        out=Path(folder_paths.get_output_directory())
        
        separated = model.separate_audio_file(file)[1]
        kwargs = {
            "samplerate": model.samplerate,
            "bitrate": mp3_bitrate,
            "clip": clip_mode,
            "as_float": as_float,
            "bits_per_sample": bits_per_sample,
        }
        samplerate=44100
        audio_list=[]
        for stem, source in separated.items():
            audio_dict=pre_audio(source,ext,samplerate,clip_mode)
            audio_list.append(audio_dict)
            if audio_save:
                stem = out / "{track}/{stem}.{ext}".format(
                    track=Path(file).name.rsplit(".", 1)[0],
                    trackext=Path(file).name.rsplit(".", 1)[-1],
                    stem=stem,
                    ext=ext,
                )
                stem.parent.mkdir(parents=True, exist_ok=True)
                save_audio(source, str(stem), **kwargs)
                output_ = os.path.join(folder_paths.get_output_directory(), f"audio_{audio_file_prefix}")
                logging.info(f"save audio in {output_} dir...")
        
        mixed_wav=audio_list[0]["waveform"]+audio_list[1]["waveform"]+audio_list[2]["waveform"]
        mixed={"waveform": mixed_wav, "sample_rate": samplerate}
        return (mixed,audio_list[0],audio_list[1],audio_list[2],audio_list[3],)


NODE_CLASS_MAPPINGS = {
    "Demucs_Loader": Demucs_Loader,
    "Demucs_Sampler": Demucs_Sampler,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Demucs_Loader": "Demucs_Loader",
    "Demucs_Sampler": "Demucs_Sampler",
}
