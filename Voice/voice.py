import subprocess
import RPi.GPIO as gpio
def voice():
 gpio.setmode(gpio.BOARD)
 gpio.setwarnings(False)
 gpio.setup(13, gpio.OUT)
 gpio.setup(15, gpio.OUT)
 gpio.setup(18, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(32, gpio.OUT)
 gpio.setup(36, gpio.OUT)
 gpio.setup(38, gpio.OUT)
 gpio.setup(40, gpio.OUT)
 gpio.setup(7, gpio.OUT)
 gpio.setup(11, gpio.OUT)
 gpio.setup(12, gpio.OUT)
 gpio.setup(16, gpio.OUT)
 gpio.setup(33, gpio.OUT)
 gpio.setup(35, gpio.OUT)
 a=gpio.PWM(7, 50)
 b=gpio.PWM(11, 50)
 c=gpio.PWM(12, 50)
 d=gpio.PWM(16, 50)
 g=gpio.PWM(33, 100)
 s=gpio.PWM(35, 100)
 s.start(14)
 g.start(14)
 a.start(1)
 b.start(1)
 c.start(1)
 d.start(1)

def forward():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)
# Motor 1
 gpio.output(32, True)
 gpio.output(36, False)
# Motor 2
 gpio.output(38, False)
 gpio.output(40, True)
	
def backward():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)
# Motor 1
 gpio.output(32, False)
 gpio.output(36, True)
# Motor 2
 gpio.output(38, True)
 gpio.output(40, False)
def stop():
# Motor 1
 gpio.output(18, False)
 gpio.output(22, False)
# Motor 2
 gpio.output(13, False)
 gpio.output(15, False)
# Motor 1
 gpio.output(32, False)
 gpio.output(36, False)
# Motor 2
 gpio.output(38, False)
 gpio.output(40, False)

def right():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)
# Motor 1
 gpio.output(32, True)
 gpio.output(36, False)
# Motor 2
 gpio.output(38, True)
 gpio.output(40, False)


def left():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)
# Motor 1
 gpio.output(32, False)
 gpio.output(36, True)
# Motor 2
 gpio.output(38, False)
 gpio.output(40, True)
def up():
 voice()
 dutyCycle = ((float(180) * 0.01) + 0.5) * 10
 s.ChangeDutyCycle(dutyCycle)
def down():
 voice()
 dutyCycle = ((float(70) * 0.01) + 0.5) * 10
 s.ChangeDutyCycle(dutyCycle)

'''def open():
 dutyCycle = ((float(45) * 0.01) + 0.5) * 10
 g.ChangeDutyCycle(dutyCycle)'''
def close():
 voice()
 dutyCycle = ((float(180) * 0.01) + 0.5) * 10
 g.ChangeDutyCycle(dutyCycle)
def center():
 voice()
 dutyCycle = ((float(110) * 0.01) + 0.5) * 10
 s.ChangeDutyCycle(dutyCycle)

while True:
    subprocess.call(['./speech-rec.sh'])
    with open('MyText.txt', 'r') as f:
      lineArr=f.read().split()
    if 'left' in lineArr:
        print ("left")
        voice()
	subprocess.call(["espeak","-s140 -ven+18 -z","i will turn to left"])
        left()
    elif 'right' in lineArr :
        print ("right") 
	subprocess.call(["espeak","-s140 -ven+18 -z","i will turn to right"])
        voice()
        right()
    elif 'forward' in lineArr :
        print ("forward")
        voice()
	subprocess.call(["espeak","-s140 -ven+18 -z","i will go to forward"])
	forward()        
    elif 'back' in lineArr :
        print ("back")
        voice()
	subprocess.call(["espeak","-s140 -ven+18 -z","i will go to back"])
        backward()
    elif 'stop' in lineArr :
        print ("stop")
        voice()
	subprocess.call(["espeak","-s140 -ven+18 -z","i will stop now"])
        stop()
        gpio.cleanup()
    elif 'fast' in lineArr :
        subprocess.call(["espeak","-s140 -ven+18 -z","yes sir"])
    elif 'introduce' in lineArr :
        print ("introducing")
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","i'm a intelligent robot developed by "])
	subprocess.call(["espeak","-g15 -s140 -ven+18 -z"," computer and mechatronic department as a graduation project"])
	subprocess.call(["espeak","-g15 -s140 -ven+18 -z"," under supervised professor adel and engineer amr abdelfattah "])	
	subprocess.call(["espeak","-g15 -s140 -ven+18 -z"," work in two mode first automatic by computer vision"])
	subprocess.call(["espeak","-g15 -s140 -ven+18 -z"," other munual by internet of things and voice command "])
    elif 'time' in lineArr :
        print ("time")
	subprocess.Popen(['sh','time.sh'])
    elif 'automatic' in lineArr :
        print ("vision")
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","you select automatic mode"])
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","control by computer vision"])
        subprocess.Popen(['sh','img.sh'])
    elif 'things' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","you select manual mode"])
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","control by internet of things"])
        print ("internet mode")
        subprocess.Popen(['sh','iot.sh'])
    elif 'restart' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","system will restart in 30 sec"])
        print ("restart")
	subprocess.Popen(['sh','restart.sh'])
    elif 'shutdown' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","system will shutdown in 30 sec"])
        print ("shutdown")
	subprocess.Popen(['sh','shutdown.sh'])
    elif 'open' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","gripper will open"])
        open()
    elif 'close' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","gripper will close"])
        close()
    elif 'up' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","gripper will up"])
        up()
    elif 'down' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","gripper will down"])
        down()
    elif 'down' in lineArr :
        subprocess.call(["espeak","-g15 -s140 -ven+18 -z","gripper will center"])
        center()     
    f.close()
    with open('MyText.txt', 'w') as f:
        f.write(" ")
    f.close()
