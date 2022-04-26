import json
import websockets
import asyncio
import time
import wave
import pyaudio
import sys
import audioop
import DisplayControl

class Deepgram:
    # PyAudio configurations 
    CHUNK = 2048
    CHANNELS = 1
    RATE = 16000
    audio_client = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt32 # default depth format of mic is 32 bit 

    def __init__(self):
        self.loop = asyncio.get_event_loop().run_until_complete(self.main())

    # Open audio stream
    def handle(self):
        self.stream_in = pyaudio.PyAudio().open(
            format=pyaudio.paInt32,
            channels=1,
            rate=16000,
            input=True,
            input_device_index=,
            frames_per_buffer=2048,
        )

    # Create socket to connect to deepgram 
    def connect(self):
        return websockets.connect(
            "wss://api.deepgram.com/v1/listen?punctuate=true&channels=1&sample_rate=16000&encoding=linear16",
            extra_headers={
                "Authorization": "Token {}".format(DEEPGRAM_API_KEY)
            },
        )

    async def main(self):
        async with self.connect() as dg_socket:
            print("Speech to Text mode activated")
            async def sender(dg_socket):
                frames = []
                try:
                    while True:
                        input_audio = self.stream_in.read(2048, exception_on_overflow = False)
                        #frames.append(input_audio)
                        input_audio2 = audioop.lin2lin(input_audio, 4, 2) # converts from 32 bit to 16 bit
                        await dg_socket.send(bytes(input_audio2))
                        await asyncio.sleep(0)
                except Exception as e:
                    print(e)
                except websockets.ConnectionClosed:
                    print("connection closed")
                except KeyboardInterrupt:
                    print("interrupted")
                    # Send audio stream to wav file to test 
                    '''waveFile = wave.open('server_system3.wav', 'wb')
                    waveFile.setnchannels(1)
                    waveFile.setsampwidth(4)
                    #waveFile.setsampwidth(2)
                    waveFile.setframerate(RATE)
                    waveFile.writeframes(b''.join(frames))
                    waveFile.close()'''

            async def receiver(dg_socket):
                # receive message and print
                dc = DisplayControl()
                async for msg in dg_socket:
                    msg = json.loads(msg)
                    if "alternatives" in msg:
                        transcript = msg["alternatives"][0]["transcript"]
                        print(f"transcript from alternatives - {transcript}")

                    elif "channel" in msg and msg["is_final"]:
                        transcript = msg["channel"]["alternatives"][0]["transcript"]
                        if (transcript != ''):
                            #print(f"Transcript: {transcript}")
                            dc.write(transcript)
                            #time.sleep(20)

            await asyncio.wait([asyncio.ensure_future(sender(dg_socket)), asyncio.ensure_future(receiver(dg_socket))])

#if __name__ == "__main__":
#   asyncio.get_event_loop().run_until_complete(main()) 
