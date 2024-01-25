import speech_recognition as sr
import random
import time

def recognize_speech_from_mic(recognizer, microphone):
    """
    Transcribe speech recorded from microphone
    
    Returns a Dictionary with Tthree keys:
    "success": a boolean indicating whether or not the transcription was successful
    "error": None if no error occured, otherwise a string containing an error message
    "transcription": None if speech could not be transcribed, otherwise a string containing the transcription
    
    """

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unvailable"
    except sr.UnknownValueError:
        response["error"] = "Unbale to recognize speech"
    
    return response

if __name__ == "__main__":
        WORDS = ["Apple", "Orange"]
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        while True:
            rand_idx = random.randint(0, len(WORDS) - 1)
            word = WORDS[rand_idx]
            print("Try to say: " + word )
            guess = recognize_speech_from_mic(recognizer, microphone)
            while not guess['transcription']:
                 guess = recognize_speech_from_mic(recognizer, microphone)
            print("You said: " + guess["transcription"])
            if (guess["transcription"] == word):
                print("You said the word correctly")
            else:
                print("You misspoke")
        
