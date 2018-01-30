import pyaudio
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class GoogleSpeech:

    def __init__(self):
        self.create_audio_file()

    def create_audio_file(self):
        """
        creates an .raw audio to be analyzed by Google Cloud Speech API
        :return:
        """
        audio_format = pyaudio.paInt16

        channels = 1
        sample_rate = 16000
        chunk = int(sample_rate / 10)
        seconds = 5

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=audio_format, channels=channels,
                            rate=sample_rate, input=True,
                            frames_per_buffer=chunk)
        print("recording...")
        frames = []

        for i in range(0, int(sample_rate / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("finished recording")

        file = open("/Users/brandenkaestner/coding/PycharmProjects/hal/resources/audio.raw", "wb")
        file.write(b''.join(frames))
        file.close()

    def analyze_audio(self):
        """
        Takes audio and puts into string
        :return:
        """
        # Instantiates a client
        client = speech.SpeechClient()

        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'audio.raw')

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US')
        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            # print(type(result.alternatives[0].transcript))
            # print('Transcript: {}'.format(result.alternatives[0].transcript))
            return result.alternatives[0].transcript
