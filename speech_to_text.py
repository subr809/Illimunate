import json
import websockets
import asyncio
import time
import wave
import pyaudio
import sys
import audioop
from googletrans import Translator
from display_control import DisplayControl

class SpeechToText:

    def __init__(self, display):
        self.stream_in = pyaudio.PyAudio().open(
                    format=pyaudio.paInt32,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=3,
                    frames_per_buffer=2048,
                    )
        self.dc = display
        self.translator = Translator()
#        print("Test translator")
#        print(self.translator.translate("test de la fonction de synthèse vocale", src="fr"))


    # Create socket to connect to deepgram 
    def connect(self, translate):
        url = "wss://api.deepgram.com/v1/listen?punctuate=true&channels=1&sample_rate=16000&encoding=linear16"
        if translate:
            url = url + "&language=fr"
        return websockets.connect(
            url,
            extra_headers={
                "Authorization": "Token {}".format('02997569d98e807300e46573e7f41f0e82195e3f')
            },
        )

    async def main(self, running, translate):
        async with self.connect(translate) as dg_socket:
            if not translate:
                print("Speech to Text mode activated")
            else:
                print("Translation activated")

            async def sender(dg_socket):
                while running[0]:
                    input_audio = self.stream_in.read(2048, exception_on_overflow = False)
                    input_audio2 = audioop.lin2lin(input_audio, 4, 2) # converts from 32 bit to 16 bit
                    await dg_socket.send(bytes(input_audio2))
                    await asyncio.sleep(0)
                await dg_socket.send(b'')

            async def receiver(dg_socket):
                # receive message and print
                #dc = DisplayControl()
                async for msg in dg_socket:
                    msg = json.loads(msg)
                    if "channel" in msg and msg["is_final"]:
#                        print(msg)
                        transcript = msg["channel"]["alternatives"][0]["transcript"]
#                        print(transcript)
                        if (transcript != '' and not translate):
                            print(f"Transcript: {transcript}")
                            self.dc.write(transcript)
                        elif transcript != '':
                            translation = self.translator.translate(transcript).text
                            print(f"Translation: {translation}")
                            self.dc.write(translation)

            await asyncio.wait([asyncio.ensure_future(sender(dg_socket)), asyncio.ensure_future(receiver(dg_socket))])
    
    def run(self, running, status = False):
        asyncio.get_event_loop().run_until_complete(self.main(running, status))

if __name__ == "__main__":
    dc = DisplayControl()
    st = SpeechToText(dc)
    st.run([True], True)
