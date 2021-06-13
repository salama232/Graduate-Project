# author Ingmar Stapel
# version 0.1 BETA
# date 20140810 04:36 AM

import webiopi

# Enable debug output
# webiopi.setDebug()
GPIO = webiopi.GPIO
	
# set variables Motor speed.
acceleration = 0
spotturn = "false"
# Here we configure the PWM settings for
# the four DC motors. It defines the two GPIO
# pins used for the input on the L298 H-Bridge,
# starts the PWM and sets the
# motors' speed initial to 0
motor1_in1_pin = 27
motor1_in2_pin = 22
motor1_in11_pin = 12
motor1_in22_pin = 16
GPIO.setFunction(motor1_in1_pin, GPIO.OUT)
GPIO.setFunction(motor1_in2_pin, GPIO.OUT)
GPIO.setFunction(motor1_in11_pin, GPIO.OUT)
GPIO.setFunction(motor1_in22_pin, GPIO.OUT)
motor2_in1_pin = 24
motor2_in2_pin = 25
motor2_in11_pin = 20
motor2_in22_pin = 21
GPIO.setFunction(motor2_in1_pin, GPIO.OUT)
GPIO.setFunction(motor2_in2_pin, GPIO.OUT)
GPIO.setFunction(motor2_in11_pin, GPIO.OUT)
GPIO.setFunction(motor2_in22_pin, GPIO.OUT)
# set PWM for motor1 to 0
motorpwm1_in1_pin = 4
motorpwm1_in2_pin = 17
GPIO.setFunction(motorpwm1_in1_pin, GPIO.PWM)
GPIO.setFunction(motorpwm1_in2_pin, GPIO.PWM)
pwm1 = 13
pwm2 = 19
GPIO.setFunction(pwm1, GPIO.PWM)
GPIO.setFunction(pwm2, GPIO.PWM)
# set PWM for motor2 to 0
motorpwm2_in1_pin = 18
motorpwm2_in2_pin = 23
GPIO.setFunction(motorpwm2_in1_pin, GPIO.PWM)
GPIO.setFunction(motorpwm2_in2_pin, GPIO.PWM)

def initiate():
	global spotturn
	global acceleration
	global motorLspeed
	global motorRspeed
	global speedstep
	global maxspeed
	global minspeed
	global angle
	spotturn = "false"
	acceleration = 0
	motorLspeed = 0
	motorRspeed = 0
	speedstep = 5
	maxspeed = 40
	minspeed = 0
	angle=0

# def getvalues():
	# global spotturn
	# global acceleration
	# global motorLspeed
	# global motorRspeed
	# global speedstep
	# global maxspeed
	# global minspeed
	
	# speedstep = 5
	# maxspeed = 40
	# minspeed = 0
	# return spotturn, acceleration, motorLspeed, motorRspeed, speedstep, maxspeed, minspeed
	
# Here we define the methods used to determine
# whether a motor needs to spin forward or backwards.
# both pins match, the motor will not turn.

def reverse():
    GPIO.digitalWrite(motor1_in1_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor1_in2_pin, GPIO.LOW)
    GPIO.digitalWrite(motor2_in1_pin, GPIO.LOW)
    GPIO.digitalWrite(motor2_in2_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor1_in11_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor1_in22_pin, GPIO.LOW)
    GPIO.digitalWrite(motor2_in11_pin, GPIO.LOW)
    GPIO.digitalWrite(motor2_in22_pin, GPIO.HIGH)	
	
def forward():
    GPIO.digitalWrite(motor1_in1_pin, GPIO.LOW)
    GPIO.digitalWrite(motor1_in2_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor2_in1_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor2_in2_pin, GPIO.LOW)
    GPIO.digitalWrite(motor1_in11_pin, GPIO.LOW)
    GPIO.digitalWrite(motor1_in22_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor2_in11_pin, GPIO.HIGH)
    GPIO.digitalWrite(motor2_in22_pin, GPIO.LOW)
	
# stop the motors
def stop():
	GPIO.digitalWrite(motor1_in1_pin, GPIO.LOW)
	GPIO.digitalWrite(motor1_in2_pin, GPIO.LOW)
	GPIO.digitalWrite(motor2_in1_pin, GPIO.LOW)
	GPIO.digitalWrite(motor2_in2_pin, GPIO.LOW)
	GPIO.digitalWrite(motor1_in11_pin, GPIO.LOW)
	GPIO.digitalWrite(motor1_in22_pin, GPIO.LOW)
	GPIO.digitalWrite(motor2_in11_pin, GPIO.LOW)
	GPIO.digitalWrite(motor2_in22_pin, GPIO.LOW)
	# motorLspeed, motorRspeed, acceleration
	initiate()
	return 0, 0, 0
def open():
        GPIO.pwmWriteAngle(pwm2,-100)     
def close():
        GPIO.pwmWriteAngle(pwm2,30)	

def center():
        GPIO.pwmWriteAngle(pwm1,0)

# This functions sets the motor speed.
def up():
        GPIO.pwmWriteAngle(pwm1,180)
def down():
        GPIO.pwmWriteAngle(pwm1,-30)
def setacceleration(value):

	global motorLspeed
	global motorRspeed
	global acceleration
	global minspeed
	global maxspeed
	
	acceleration = acceleration + value
	
	minspeed, maxspeed = getMinMaxSpeed()
	
	#Set Min and Max values for acceleration
	if(acceleration < -40):
		acceleration = -40
	
	if(acceleration > 40):
		acceleration = 40	
	
	if(acceleration > 0):
		# drive forward
		forward()
		motorLspeed = acceleration
		motorRspeed = acceleration
		#print("forward: ", motorLspeed, motorRspeed)
	elif(acceleration == 0):
		# stopp motors
		motorLspeed = acceleration
		motorRspeed = acceleration
		motorLspeed, motorRspeed, acceleration = stop()
		#print("stop: ", motorLspeed, motorRspeed)
	else:
		# drive backward
		reverse()
		motorLspeed = (acceleration * -1)
		motorRspeed = (acceleration * -1)
		#print("backward: ", motorLspeed, motorRspeed)
	
	motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)
	#print("check: ", motorLspeed, motorRspeed)

# check the motorspeed if it is correct and in max/min range
def check_motorpseed(motorLspeed, motorRspeed):
	if (motorLspeed < minspeed):
		motorLspeed = minspeed

	if (motorLspeed > maxspeed):
		motorLspeed = maxspeed
		
	if (motorRspeed < minspeed):
		motorRspeed = minspeed

	if (motorRspeed > maxspeed):
		motorRspeed = maxspeed	
		
	return motorLspeed, motorRspeed

# Set Min Max Speed
def getMinMaxSpeed():
	minspeed = 0
	maxspeed = 40
	return minspeed, maxspeed
	
# Get the motor speed
def getMotorSpeed():
	global motorLspeed
	global motorRspeed
	
	return motorLspeed, motorRspeed

def getMotorSpeedStep():
	return 5	
	
@webiopi.macro
def ButtonForward():
	fowardAcc = 0
	fowardAcc = getMotorSpeedStep()

	setacceleration(fowardAcc)
	
	motorLspeed, motorRspeed = getMotorSpeed()
	
	# percent calculation	
	valueL = float(motorLspeed)/100
	valueR =  float(motorRspeed)/100
		
	GPIO.pulseRatio(motorpwm1_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm11_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm12_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm21_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm22_in2_pin, valueR)
@webiopi.macro
def ButtonReverse():
	backwardAcc = 0
	backwardAcc = getMotorSpeedStep()

	setacceleration((backwardAcc*-1))
	
	motorLspeed, motorRspeed = getMotorSpeed()
	
	# percent calculation
	valueL = float(motorLspeed)/100
	valueR =  float(motorRspeed)/100
		
	GPIO.pulseRatio(motorpwm1_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm1_in11_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in22_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in11_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in22_pin, valueR)
	
@webiopi.macro
def ButtonTurnLeft():

	global motorLspeed
	global motorRspeed
	global acceleration
	global speedstep
	global spotturn

	#print("inital spotturn: ",spotturn)
	if(spotturn == "right" and acceleration == 0):
		motorLspeed, motorRspeed, acceleration = stop()
	
	if(acceleration == 0):
		spotturn = "left"
			
	if(motorRspeed < motorLspeed):
		motorRspeed = motorRspeed + speedstep	
	elif(acceleration == 0):
		GPIO.digitalWrite(motor1_in1_pin, GPIO.LOW)
		GPIO.digitalWrite(motor1_in2_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor2_in1_pin, GPIO.LOW)
		GPIO.digitalWrite(motor2_in2_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor1_in11_pin, GPIO.LOW)
		GPIO.digitalWrite(motor1_in22_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor2_in11_pin, GPIO.LOW)
		GPIO.digitalWrite(motor2_in22_pin, GPIO.HIGH)
		motorLspeed = motorLspeed + speedstep
		motorRspeed = motorRspeed + speedstep
	else:
		motorLspeed = motorLspeed - speedstep

	motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)		
	valueL = float(motorLspeed)
	valueR = float(motorRspeed)
		
	valueL = valueL/100
	valueR = valueR/100

	GPIO.pulseRatio(motorpwm1_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in2_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in1_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm1_in11_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in22_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in11_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in22_pin, valueR)
	
	#print("LEFT: ",valueL,valueR,spotturn)	
@webiopi.macro
def ButtonTurnRight():
	global motorLspeed
	global motorRspeed
	global acceleration
	global speedstep
	global spotturn

	#print("inital spotturn: ",spotturn)
	if(spotturn == "left" and acceleration == 0):
		motorLspeed, motorRspeed, acceleration = stop()
	if(acceleration == 0):
		spotturn = "right"
	
	if(motorLspeed < motorRspeed):
		motorLspeed = motorLspeed + speedstep	
	elif(acceleration == 0):
		GPIO.digitalWrite(motor1_in1_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor1_in2_pin, GPIO.LOW)
		GPIO.digitalWrite(motor2_in1_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor2_in2_pin, GPIO.LOW)
		GPIO.digitalWrite(motor1_in11_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor1_in22_pin, GPIO.LOW)
		GPIO.digitalWrite(motor2_in11_pin, GPIO.HIGH)
		GPIO.digitalWrite(motor2_in22_pin, GPIO.LOW)

		motorLspeed = motorLspeed + speedstep
		motorRspeed = motorRspeed + speedstep
	else:
		motorRspeed = motorRspeed - speedstep

	motorLspeed, motorRspeed = check_motorpseed(motorLspeed, motorRspeed)		
	valueL = float(motorLspeed)
	valueR = float(motorRspeed)
		
	valueL = valueL/100
	valueR = valueR/100

	GPIO.pulseRatio(motorpwm1_in1_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in2_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in1_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in2_pin, valueR)
	GPIO.pulseRatio(motorpwm1_in11_pin, valueL)
	GPIO.pulseRatio(motorpwm1_in22_pin, valueL)
	GPIO.pulseRatio(motorpwm2_in11_pin, valueR)
	GPIO.pulseRatio(motorpwm2_in22_pin, valueR)
	#print("RIGHT: ",valueL,valueR, spotturn)		
@webiopi.macro
def ButtonStop():	
	stop()
@webiopi.macro
def Buttonopen():
        open()
@webiopi.macro
def Buttonclose():
        close()
def Buttonup():
        up()
@webiopi.macro
def Buttondown():
        down()
def Buttoncenter():
        center()

initiate()

server = webiopi.Server(port=8000, login="robot", password="robot")

server.addMacro(ButtonForward)
server.addMacro(ButtonStop)
server.addMacro(ButtonReverse)
server.addMacro(ButtonTurnRight)
server.addMacro(ButtonTurnLeft)
server.addMacro(Buttonopen)
server.addMacro(Buttonclose)
server.addMacro(Buttonup)
server.addMacro(Buttondown)
server.addMacro(Buttoncenter)
webiopi.runLoop()
server.stop()
