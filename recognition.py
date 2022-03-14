import speech_recognition

def google_recognize():
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    with microphone as audio_file:
        recognizer.adjust_for_ambient_noise(audio_file)
        audio = recognizer.listen(audio_file)
        try:
            result = recognizer.recognize_google(audio, language = "ru")
        except:
            return ("Не распознано")
        return result

if __name__ == "__main__":
    while True:
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()
        print("Говорите")
        print(google_recognize())
