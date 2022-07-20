from gpiozero import Button
from time import sleep

def deepgram(running):
	#global func_running
	while running[0]:
		print("Deepgram")
		sleep(1)
	print("exit deepgram")

def speechtotext(running):
	#global func_running
	while running[0]:
		print("Speech-to-text")
		sleep(1)
	print("exit stt")


mode = 0
func_running = [False]
def changemode():
	global func_running
	global mode
	mode += 1
	mode %= 2
	func_running[0] = False
	print("change mode")
	

button = Button(23)
button.when_pressed = changemode

while True:
	func_running[0] = True
	print("main loop")
	if mode == 0:
		deepgram(func_running)
	elif mode == 1:
		speechtotext(func_running)
