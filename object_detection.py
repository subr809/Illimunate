import cv2
import time
from display_control import DisplayControl, ObjType

class ObjectDetection:
    def __init__(self, dc, camera=True):
        if(camera):
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture("vids/test_2.MP4")

        self.stop_sign_cascade = cv2.CascadeClassifier("imgs/stop_sign_classifier.xml")
        # self.yield_sign_cascade = cv2.CascadeClassifier("imgs/yield_sign_classifier.xml")
        self.traffic_light_cascade = cv2.CascadeClassifier("imgs/traffic_light_classifier.xml")
        self.dc = dc
        self.stop_sign_counter = 1
        self.traffic_light_counter = 1

    def detect_objects(self, running):
        while(running[0]):
            ret, frame = self.cap.read()
                
            imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            stop_signs = self.stop_sign_cascade.detectMultiScale(imgGray)
            traffic_lights = self.traffic_light_cascade.detectMultiScale(imgGray)

            for (x,y,w,h) in stop_signs:
                print("found stop sign, counter = " + str(self.stop_sign_counter) + "\n")
                self.dc.object_detected(ObjType.STOP_SIGN)
                self.stop_sign_counter+=1
                time.sleep(5)
            
            for (x,y,w,h) in traffic_lights:
                print("found traffic light, counter = " + str(self.traffic_light_counter) + "\n")
                self.dc.object_detected(ObjType.TRAFFIC_LIGHT)
                self.traffic_light_counter+=1
                time.sleep(5)

            #if cv2.waitKey(30) & 0xFF == ord('q'):
            #    break

# if __name__  == "__main__":
#     od = ObjectDetection(False)
#     od.detect_objects()
