import numpy as np
import sounddevice as sd
from scipy.fft import fft
from settings import SAMPLE_RATE, BUFFER_SIZE

class AudioAnalyzer:
    def __init__(self, device_name_or_index=None):
        self.audio_data = np.zeros(BUFFER_SIZE, dtype=np.float32)
        self.stream = None
        self.device = device_name_or_index

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)  # Debugging audio issues
        self.audio_data = indata[:, 0]  #first channel from stereo 

    def start_stream(self):
        # loopback is stereo, use channels=2
        self.stream = sd.InputStream(
            device=1,
            callback=self.audio_callback,
            samplerate=SAMPLE_RATE,
            channels=2,      # stereo/mono 2/1
            blocksize=BUFFER_SIZE
        )
        self.stream.start()

    def stop_stream(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def get_frequency_spectrum(self):
        N = len(self.audio_data)
        fft_output = fft(self.audio_data)
        freq_bins = np.fft.fftfreq(N, 1 / SAMPLE_RATE)
        return freq_bins[:N // 2], np.abs(fft_output[:N // 2])  # Positive frequencies
