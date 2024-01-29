import pyaudio
import wave
import keyboard

def record_audio(wav_file, sample_rate=44100, chunk_size=1024, channels=1):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk_size)

    frames = []

    print("Press 'S' to start recording")
    keyboard.wait('s')
    print("Recording... Press 'E' to stop")

    while True:
        data = stream.read(chunk_size)
        frames.append(data)
        if keyboard.is_pressed('e'):  # 如果按下 'E' 键则结束录制
            print("Recording Stopped")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

record_audio("output.wav")
