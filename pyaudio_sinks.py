import pyaudio
p = pyaudio.PyAudio()
print("Starting===========")
[p.get_device_info_by_index(i) for i in range(p.get_device_count())]