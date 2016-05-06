import email
import smtplib
import RPi.GPIO as GPIO
import time
import Adafruit_DHT as dht
import picamera
import os
from time import sleep
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
Servo=GPIO.PWM(5,50)
Servo.start(6)
GPIO.setup(11, GPIO.IN)         
GPIO.setup(3, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.IN)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.OUT)

camera = picamera.PiCamera()
camera.hflip = True
camera.vlip = True
picNumber = 3

result = GPIO.input(31)

def send_email(address, subject, body):
    msg = email.message_from_string(body)
    msg['From'] = "rpi_loh@hotmail.com"
    msg['To'] = address
    msg['Subject'] = subject

    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo()
    s.starttls()
    s.login('rpi_loh@hotmail.com','loh321loh')

    s.sendmail("zeina.araby@gmail.com", address, msg.as_string())



def send_image(address, subject, body, image_path):
    img_data = open(image_path, 'rb').read()
    msg = MIMEMultipart()
    msg['From'] = "rpi_loh@hotmail.com"
    msg['To'] = address
    msg['Subject'] = subject

    text = MIMEText(body)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(image_path))
    msg.attach(image)

    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('rpi_loh@hotmail.com','loh321loh')

    s.sendmail("zeina.araby@gmail.com", address, msg.as_string())

    s.quit()

camera.capture('photos/test1.jpg')
    

while True:
    h,t = dht.read_retry(dht.DHT11, 4)
    i=GPIO.input(11)
    GPIO.output(8, False)
    time.sleep(0.1)
    GPIO.output(8, True)
    time.sleep(0.001)
    GPIO.output(8, False)
    while GPIO.input(10)==0:
        signalOff=time.time()

    while GPIO.input(10)==1:
        signalOn=time.time()



    timePassed=signalOn-signalOff
    distance=timePassed*17150

    
    if 0<distance<60:
        Servo.ChangeDutyCycle(12.5)
    else:
        Servo.ChangeDutyCycle(5.5)
        time.sleep(2)                                                                                           

    
        
    print "distance=",distance,"cm"
    print 'Temp={0:01f}*C Humidity={1:0.1f}%'.format(t, h)
    

    if result == 1:
        send_email('zeina.araby@gmail.com',
                'door',
                'someone is breaking your door')
       
    else:
        if result == 0:
            GPIO.output(15,GPIO.LOW)
            print("no vibration")
            sleep(1)
    
    if i == 0:
        print 'no intruder'
        GPIO.output(3, GPIO.LOW)
        sleep(2)
    else:
        print 'intruder alert'
        sleep(2)
        GPIO.output(3, GPIO.HIGH)
        camera.capture('photos/test%03d.jpg' %picNumber)
        picNumber = picNumber +1
        send_image('zeina.araby@gmail.com',
                    'Sending image',
                    'Ftemkewmrkj kejr kwer',
                    '/home/pi/photos/test1.jpg')                  

       
    
Servo.stop()
GPIO.stop()
GPIO.cleanup()
