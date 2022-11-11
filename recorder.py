
import pyaudio
import wave 
import numpy as np
import librosa
import pandas as pd
import tensorflow as tf
from tensorflow import keras

model_path = r"C:\Users\justi\Documents\emotional-speech\src\Emotion_Voice_Detection_Model.h5"
model = tf.keras.models.load_model(model_path)

def record(outputFile):
    CHUNK = 1024 * 2
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    DURATION = 5

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording....")
    frames = []
    for i in range(0, int(RATE/CHUNK *DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#record('output.wav')

def predict(file):
  X, fs = librosa.load(file, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
  mfccs = np.mean(librosa.feature.mfcc(y=X, sr=fs, n_mfcc=13),axis=0)
  featurelive = mfccs
  livedf2 = featurelive
  livedf2= pd.DataFrame(data=livedf2)
  livedf2 = livedf2.stack().to_frame().T
  twodim = np.expand_dims(livedf2, axis=2)
  
  return model.predict(twodim, batch_size=1)