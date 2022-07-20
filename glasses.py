from object_detection import ObjectDetection
from speech_to_text import  SpeechToText
from display_control import DisplayControl
import time
from gpiozero import Button

OBJECT_DETECTION = 0
SPEECH_TO_TEXT = 1 
TRANSLATION = 2 


mode = 0
func_running = [0]
dc = DisplayControl()
od = ObjectDetection(dc)
sp = SpeechToText(dc)


def object_detection(running):
    dc.write("Object Detection Mode")
    od.detect_objects(running)
    print("done detecting objects")

def speech_to_text(running):
    dc.write("Speech to Text Mode")
    sp.run(running, False)
    print("done speech to text")

def translate(running):
    dc.write("Translation Mode")
    sp.run(running, True)
    print("done translating")

def change_mode():
    global func_running
    global mode
    mode += 1 
    mode %= 3
    func_running[0] = False
    print("changing mode...\n")


if __name__ == "__main__":
    # od = object_detection.ObjectDetection()
    # od.detect_objects()

    button = Button(23)
    button.when_pressed = change_mode
    

    while True:
        func_running[0] = True
        if mode == 0:
            speech_to_text(func_running)
        elif mode == 1:
            translate(func_running)
        elif mode == 2:
            object_detection(func_running)




