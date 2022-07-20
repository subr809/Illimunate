#from playsound import playsound
import speech_recognition as sr 
from googletrans import Translator 
#from gtts import gTTS 
#import os

# class Translate:
#    def __init__(self, text):
#       self.text = text
  
#    def getTranslated(self):      
#       translator = Translator()

#       translation = translator.translate(self.text, dest = en)
#       text = translation.text
#       return text

# obj = Translate('')
# print(obj.getTranslated())

def translate(text):
   translator = Translator()
   translation = translator.translate(text)
   return translation.text


