import cv2
import threading
import playsound
import smtplib
import os

current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'alarm-sound.mp3')

if os.path.exists(file_path):
    print("File exists at path:", file_path)
else:
    print("File does not exist at path:", file_path)

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')
vid = cv2.VideoCapture(0)
runOnce = False
isAlarmPlaying = False  # Flag variable to track alarm status

def play_alarm_sound_function():
    global isAlarmPlaying  # Access the global flag variable
    isAlarmPlaying = True  # Set the flag to indicate alarm is playing
    playsound.playsound('alarm-sound.mp3')
    isAlarmPlaying = False  # Reset the flag after alarm sound finishes

def send_mail_function():
    recipientmail = "add recipients mail"  # Recipient's mail
    recipientmail = recipientmail.lower()  # Convert to lowercase

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("add senders mail", 'add senders password')  # Sender's mail ID and password
        server.sendmail('add senders mail', recipientmail, "Warning fire accident has been reported")  # Sender's mail with mail message
        print("Alert mail sent successfully to {}".format(recipientmail))  # Print to console to whom mail is sent
        server.close()  # Close the server

    except Exception as e:
        print(e)  # Print error if any

while True:
    Alarm_Status = False
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        if not isAlarmPlaying:  # Check if alarm is already playing
            print("Fire alarm initiated")
            threading.Thread(target=play_alarm_sound_function).start()

        if not runOnce:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start()  # Start email thread
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
