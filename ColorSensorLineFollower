import RPi.GPIO as GPIO
import time
from simple_pid import PID

# Assign GPIO pin numbers to variables
s2 = 16
s3 = 18
sig = 22 #labeled "out" on your board
cycles = 10

s21 = 35
s31 = 33
sig2 = 31
# Motor Pins
in1 = 40
in3 = 38
in2 = 36
in4 = 32
ena = 29
enb = 15

cc = 1
ccw = 0

# PID Constants
kp = 1.0
ki = 0.05
kd = 1.0
setpoint = (25500,26000,24500)
# PID Control
prev_error = 0

pid = PID(kp,ki,kd,setpoint=0)


# Setup GPIO and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(s2, GPIO.OUT)
GPIO.setup(s3, GPIO.OUT)
GPIO.setup(s21, GPIO.OUT)
GPIO.setup(s31, GPIO.OUT)
GPIO.setup(sig, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sig2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.setup(ena, GPIO.LOW)
GPIO.setup(enb, GPIO.LOW)


frequency = 50
pwm1 = GPIO.PWM(ena, frequency)
pwm2 = GPIO.PWM(enb, frequency)

def DetectColor(lsp1, lsp2, lsig):
    # Detect red values
    GPIO.output(lsp1, GPIO.LOW)
    GPIO.output(lsp2, GPIO.LOW)
    time.sleep(0.01)

    start_time = time.time()
    for count in range(cycles):
        GPIO.wait_for_edge(lsig, GPIO.FALLING)
    duration = time.time() - start_time
    red = cycles / duration
    #print("red1 value - ", red1)

    # Detect blue values
    GPIO.output(lsp1, GPIO.LOW)
    GPIO.output(lsp2, GPIO.HIGH)
    time.sleep(0.01)

    start_time = time.time()
    for count in range(cycles):
        GPIO.wait_for_edge(lsig, GPIO.FALLING)
    duration = time.time() - start_time
    blue = cycles / duration
    #print("blue1 value - ", blue1)

    # Detect green values
    GPIO.output(lsp1, GPIO.HIGH)
    GPIO.output(lsp2, GPIO.HIGH)
    time.sleep(0.01)
    start_time = time.time()
    for count in range(cycles):
        GPIO.wait_for_edge(lsig, GPIO.FALLING)
    duration = time.time() - start_time
    green = cycles / duration
    #print("green1 value - ", green1)

    return red, blue, green

def print_color(red, blue, green):
    if max(red, blue, green) == red:
        print("red")
    elif max(red, blue, green) == blue:
        print("blue")
    else:
        print("green")

def move_forward():
    # print("forwards")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.ChangeDutyCycle(20)
    pwm2.ChangeDutyCycle(20)
    pwm1.start(20)
    pwm2.start(20)
    time.sleep(0.1)
    # GPIO.output(in1, GPIO.LOW)
    # GPIO.output(in2, GPIO.LOW)
    # GPIO.output(in3, GPIO.LOW)
    # GPIO.output(in4, GPIO.LOW)
    # time.sleep(0.2)

def turn_right():
    # print("right")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(22)
    pwm1.start(0)
    pwm2.start(22)
    time.sleep(0.1)
    # GPIO.output(in1, GPIO.LOW)
    # GPIO.output(in2, GPIO.LOW)
    # GPIO.output(in3, GPIO.LOW)
    # GPIO.output(in4, GPIO.LOW)
    # time.sleep(0.1)

def turn_left():
    # print("left")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(22)
    pwm2.ChangeDutyCycle(0)
    pwm1.start(22)
    pwm2.start(0)
    time.sleep(0.1)
    # GPIO.output(in1, GPIO.LOW)
    # GPIO.output(in2, GPIO.LOW)
    # GPIO.output(in3, GPIO.LOW)
    # GPIO.output(in4, GPIO.LOW)
    # time.sleep(0.1)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.start(0)
    pwm2.start(0)
    

def get_pid(currentvalue, setpoint):
    global prev_error

    error = setpoint - currentvalue
    average_error = mean(error)
    proportional = average_error*kp
    prev_error += proportional
    return proportional

def get_color(red, blue, green):
    if red >= 22000 and red <= 39000 and blue >= 21000 and blue <= 26000 and green >= 18000 and green <= 38000:
        return "white"
    
    elif max(red,blue,green) == red:
        return "red"
    elif red >= 19000 and red <= 22000 and blue >= 24000 and blue <= 27000 and green >= 16500 and green <= 20000:
        return "purple"
    else: 
        return "not either"
    

def line_follower():
    try:
        while True:
            # obtain all color info
            # do line following

            # do some PID thing here

            red1, blue1, green1 = DetectColor(s2, s3, sig)
            red2, blue2, green2 = DetectColor(s21, s31, sig2)
            #print("right",red1, blue1, green1)
            print("left",red2, blue2, green2)

            left_sensor_color = get_color(red2, blue2, green2)
            right_sensor_color = get_color(red1, blue1, green1)
            # print("right",right_sensor_color)
            print("left",left_sensor_color)



            if left_sensor_color == "white":
                turn_left()
                print("turning left")
            
            elif left_sensor_color == "red":
                turn_right()
                print("turning right)")
            
            elif left_sensor_color == "purple":
                turn_left()
                print("purple idc")

            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
time.sleep(1)
try:
    line_follower()
    time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
