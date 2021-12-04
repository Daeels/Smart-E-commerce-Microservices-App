#\x1aE\xdf\xa3 ?
from scipy.io import wavfile
samplerate, data = wavfile.read('blob.wav')
print(samplerate)