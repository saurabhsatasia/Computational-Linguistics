import speech_recognition as sr # offline Google API
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
recognizer = sr.Recognizer()

# a function that splits audio file files into chunks
# and applies speech recognition
def generateTranscipt(path, folderPath):
    """Splitting the large audio files into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_wav(file=path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(audio_segment=sound,
                  # experiment with this value for your target audio file
                  min_silence_len=500,
                  # adjust this pr requirement
                  silence_thresh=sound.dBFS-14,
                  # keep the silence for 1 second, adjustable as well
                  keep_silence=500,)

    # folder_name = "audio_chunks"
    # create a directory to store the audio file

    if not os.path.isdir(folderPath):
        os.mkdir(folderPath)
    whole_text = ""
    textMap={}

    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folderPath, f"speech_chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            # try converting it to text
            try:
                text = recognizer.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
                textMap[chunk_filename] = text
    # return the text for all chunks detected
    return textMap