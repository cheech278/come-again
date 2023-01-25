from typing import Union

import librosa
import numpy as np
import torch
from transformers import Wav2Vec2Processor, HubertForCTC


class Predictor:
    def __init__(self, name: str = "facebook/hubert-large-ls960-ft",
                 device: str = "cuda"):
        self.processor = Wav2Vec2Processor.from_pretrained(name)
        self.model = HubertForCTC.from_pretrained(name)
        self.device = device
        self.model.to(torch.device(self.device))

    def __call_(self, audio: Union[np.ndarray, torch.tensor], sample_rate: int = 16000):
        if isinstance(audio, np.ndarray):
            sr = librosa.get_samplerate(audio)
            if sr != sample_rate:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=sample_rate)
            audio = torch.tensor(audio)

        if not audio.is_cuda():
            audio = audio.to(torch.device(self.device))
        input_values = self.processor(audio,
                                      return_tensors="pt",
                                      sampling_rate=sample_rate).input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])

        return transcription
