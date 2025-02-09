import cv2
import numpy as np
import time
import RPi.GPIO as GPIO


MODEL_FPATH = "face-detection-retail-0004.bin"
ARCH_FPATH = "face-detection-retail-0004.xml"
CONF_THRESH = 0.5 # confidence of each object detected

# Define GPIO pins for LEDs using BCM board numbering
LED = 23

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(LED, GPIO.LOW)
time.sleep(2)
GPIO.output(LED, GPIO.HIGH)
time.sleep(2)

net = cv2.dnn.readNet(ARCH_FPATH, MODEL_FPATH)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD) 

vid_cap = cv2.VideoCapture(0)
if not vid_cap.isOpened():
    raise IOError("Webcam cannot be opened!")

while True:
    print("hi")
    # Capture frames
    ret, frame = vid_cap.read()
    
    # Prepare input blob and perform inference
    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv2.CV_8U)
    net.setInput(blob)
    out = net.forward()
    
    # Draw detected faces
    for detect in out.reshape(-1, 7):
        conf = float(detect[2])
        xmin = int(detect[3] * frame.shape[1])
        ymin = int(detect[4] * frame.shape[0])
        xmax = int(detect[5] * frame.shape[1])
        ymax = int(detect[6] * frame.shape[0])
        
        if conf > CONF_THRESH:
            print("Face Detected")
            GPIO.output(LED, GPIO.LOW)  # Turn off the green LED
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0), thickness=2)
            break                   
          
        else:
            GPIO.output(LED, GPIO.HIGH)  # Turn on the green LED
            print("No Face Detected")
            break
           
   
    cv2.imshow('Input', frame)   
    
    # Press "ESC" key to stop webcam
    if cv2.waitKey(1) == 27:
        break

# Release video capture object and close the window
vid_cap.release()
# Release GPIO resources
GPIO.cleanup()
cv2.destroyAllWindows()
cv2.waitKey(1)
