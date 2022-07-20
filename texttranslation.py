#from playsound import playsound
import speech_recognition as sr 
from googletrans import Translator 
#from gtts import gTTS 
import os

class Translate:
   def __init__(self):
      self.dic = ('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 
         'arabic', 'ar', 'armenian', 'hy', 'azerbaijani', 'az',
      'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian',
         'bs', 'bulgarian', 'bg', 'catalan', 'ca',
      'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)',
         'zh-cn', 'chinese (traditional)', 'zh-tw',
      'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish',
         'da', 'dutch', 'nl', 'english', 'en', 'esperanto',
      'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi', 
         'french', 'fr', 'frisian', 'fy', 'galician', 'gl',
      'georgian', 'ka', 'german', 'de', 'greek', 'el', 'gujarati', 
         'gu', 'haitian creole', 'ht', 'hausa', 'ha', 
      'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 'hmong', 
         'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo',
      'ig', 'indonesian', 'id', 'irish', 'ga', 'italian', 'it', 
         'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn',
      'kazakh', 'kk', 'khmer', 'km', 'korean', 'ko', 'kurdish (kurmanji)',
         'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
      'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish',
         'lb', 'macedonian', 'mk', 'malagasy',
      'mg', 'malay', 'ms', 'malayalam', 'ml', 'maltese', 'mt', 'maori',
         'mi', 'marathi', 'mr', 'mongolian', 'mn',
      'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no',
         'odia', 'or', 'pashto', 'ps', 'persian',
         'fa', 'polish', 'pl', 'portuguese', 'pt', 'punjabi', 'pa',
         'romanian', 'ro', 'russian', 'ru', 'samoan',
         'sm', 'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho', 
         'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala',
         'si', 'slovak', 'sk', 'slovenian', 'sl', 'somali', 'so', 
         'spanish', 'es', 'sundanese', 'su', 
      'swahili', 'sw', 'swedish', 'sv', 'tajik', 'tg', 'tamil',
         'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr',
      'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 'uzbek', 
         'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
      'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

      self.query = self.getquery()
      self.to_lang = self.destination_language()

   def getquery(self):
      def takecommand():
         r = sr.Recognizer()
         with sr.Microphone(device_index=3) as source:
            print("Say something")
            r.pause_threshold = 1
            audio = r.listen(source)
      
         try:
            query = r.recognize_google(audio, language='en-in')
            print(f"user said {query}\n")
         except Exception as e:
            print("speak again")
            return "None"
         return query

      query = takecommand()
      while (query == "None"):
         query = takecommand()
      return query

   def destination_language(self):
      print("Enter the language in which you want to convert")
      print()

      def takecommand():
         r = sr.Recognizer()
         with sr.Microphone(device_index=3) as source:
            print("Say something")
            r.pause_threshold = 1
            audio = r.listen(source)
      
         try:
            query = r.recognize_google(audio, language='en-in')
            print(f"user said {query}\n")
         except Exception as e:
            print("speak again")
            return "None"
         return query

      to_lang = takecommand()
      while (to_lang == "None"):
         to_lang = takecommand()
      to_lang = to_lang.lower()
      return to_lang
  
   def getTranslated(self):
      # Mapping it with the code
      while (self.to_lang not in self.dic):
         print("Language not available")
         print()
         self.to_lang = self.destination_language()
      
      self.to_lang = self.dic[self.dic.index(self.to_lang)+1]
      # print(to_lang)

      translator = Translator()

      translation = translator.translate(self.query, dest=self.to_lang)
      text = translation.text
      return text

obj = Translate()
print(obj.getTranslated())
