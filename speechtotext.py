import random
import time

import speech_recognition as sr


import argparse



	
def recognize_speech(filepath):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer arguments is of appropriate type
    recognizer= sr.Recognizer()
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
		

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the saved file
    audio_file = sr.AudioFile(filepath)
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.record(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None,
		"source_API": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"]= recognizer.recognize_google(audio)
        response["source_API"]= "Google Web Speech"          

    except sr.RequestError:
        # Google Web Speech API was unreachable or unresponsive
        try:
            response["transcription"]= recognizer.recognize_sphinx(audio)
            response["source_API"]= "CMU Sphinx"
            
        except:    
            response["success"] = False
            response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="provide the relative file path w.r.t current directory or absolute path to audio file")
    args = parser.parse_args()
    result= recognize_speech(args.source)
    print(result)
    
	

    