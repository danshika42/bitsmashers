from flask import Flask, render_template, Response
from unittest import result
import numpy as np
import cv2
import time
import tensorflow as tf
import tensorflow_hub as hub
from matplotlib import pyplot as plt
import ret
# import win32api
# import pyttsx3
# import pythoncom
from time import sleep
# import schedule
import time
import matplotlib.pyplot as plt
# import gtts
# from playsound import playsound
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


app=Flask(__name__)


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def gen_frames():  
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                 landmarks = results.pose_landmarks.landmark
                 l_elbow=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                 r_elbow=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                 l_knee=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                 r_knee=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                #calculate angles
                 r_hand=int(calculate_angle(([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]),(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y),([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y])))
                 l_hand=int(calculate_angle(([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]),(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y])))
                 l_leg=int(calculate_angle(([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]),([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]),([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])))
                 r_leg=int(calculate_angle(([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]),([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]),([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])))

               # Visualize angle
                 cv2.putText(image, str(l_hand), 
                                   tuple(np.multiply(r_elbow, [1250, 350]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                                        )
                 cv2.putText(image, str(r_hand), 
                                   tuple(np.multiply(r_elbow, [550, 350]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA
                                        )
                 cv2.putText(image, str(l_leg), 
                                   tuple(np.multiply(l_knee, [800, 600]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                                        )
                 cv2.putText(image, str(r_leg), 
                                   tuple(np.multiply(r_knee, [400, 600]).astype(int)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                                        )
                
                 #pose1 and pose3
                 if r_hand<60 and l_hand<60 and r_leg>150 and r_leg<180 and l_leg>150 and l_leg<180:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2) 
                                        )
                 elif r_hand>100 and r_hand<180 and l_hand<90 or l_hand>100 and l_hand<160 and r_hand<60 and r_leg>150 and r_leg<180 and l_leg>150 and l_leg<180:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2) 
                                        )
          #       pose2 https://www.youtube.com/clip/UgkxZJAvtpPYlD7P5t8-b6QoTbSALc0a_Va4
                 elif l_hand>70 and l_hand<90 and r_hand>40 and r_hand<60 and r_leg>150 and r_leg<180 and l_leg>150 and l_leg<180:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2) 
                                        )
                 elif r_leg>30 and r_leg<60 and l_leg<180:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2) 
                                        )
          #       pose4 https://www.youtube.com/clip/UgkxoI0yHWRziYrfK1xkLkwZ3m-LfepQm69v
                 elif r_leg>100 and r_leg<150 and l_leg>150 and l_leg<180:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,128,0), thickness=2, circle_radius=2) 
                                        ) 
                 else:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2) 
                                        )    
                   
            except:
                pass                      
            
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route("/")
def home():
     return render_template("index.html")

@app.route("/feed/")
def feed():
     return render_template("Feedback.html")

@app.route("/start/")
def start():
     return render_template("start.html")

@app.route("/start1/")
def start1():
     return render_template("start1.html")

@app.route("/start2/")
def start2():
     return render_template("start2.html")

@app.route("/start3/")
def start3():
     return render_template("start3.html")

@app.route("/vid1/")
def vid1():
     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/vid2/")
def vid2():
     return Response()

@app.route("/vid3/")
def vid3():
     return Response()

@app.route("/vid4/")
def vid4():
     return Response()


if __name__=="__main__":
    app.run(host = "127.0.0.1",debug=True)

