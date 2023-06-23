from gtts import gTTS
from io import BytesIO

class GttsUtils:
    @staticmethod
    def text_to_speech(text, lang="zh-cn"):
        tts = gTTS(text=text, lang=lang)
        audio_bytes = BytesIO()
        tts.save(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes