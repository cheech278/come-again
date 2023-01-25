import logging
from threading import Thread

from omegaconf import OmegaConf

from model import Predictor


class ASRStream:
    def __init__(self, name: str, config: OmegaConf, state, audio_reader):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.config = config
        self.asr_thread = None
        self.state = state
        self.audio_reader = audio_reader

        self.predictor = Predictor(config.model_name, config.model_name)

        self.logger.info("Create ASRStream")

    def _ocr_loop(self):
        try:
            frame = self.audio_reader.read()
            pred = self.predictor(frame)
            self.state.text = pred

        except Exception as e:
            self.logger.exception(e)
            self.state.exit_event.set()

    def _start_asr(self):
        self.asr_thread = Thread(target=self._ocr_loop)
        self.asr_thread.start()

    def start(self):
        self._start_asr()
        self.logger.info("Start OcrStream")

    def stop(self):
        if self.asr_thread is not None:
            self.asr_thread.join()
        self.logger.info("Stop OcrStream")
