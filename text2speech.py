import azure.cognitiveservices.speech as speechsdk
# from playsound import playsound
import pygame

def play_wav(file_path):
    # 初始化pygame
    pygame.init()

    # 加载音频文件
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)

    # 播放音频
    pygame.mixer.music.play()

    # 保持脚本运行直到音频播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 创建语音配置实例，使用你的订阅密钥和服务区域。
speech_key, service_region = "d173b076a256495e94c4716a370d0cdb", "japaneast"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# 设置语音名称。
speech_config.speech_synthesis_voice_name = "en-US-AvaNeural"

# 创建语音合成器实例。
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

# 从控制台输入接收文本。
print("Type some text that you want to speak...")
text = input()

# 合成文本为语音，并获取结果。
result = speech_synthesizer.speak_text_async(text).get()

# 检查合成结果。
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Speech synthesized for text [{text}]")

    # 将合成的语音保存到文件
    audio_file_name = "output_audio.wav"
    with open(audio_file_name, "wb") as audio_file:
        audio_file.write(result.audio_data)
    print(f"Audio saved to '{audio_file_name}'")

    # 播放保存的音频文件
    play_wav(audio_file_name)

elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
    print("Did you update the subscription info?")
