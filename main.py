import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)
GPIO.setup([11,12,13,15,16,18], GPIO.OUT)
GPIO.setup([31,32], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

global mode
global auto
global s
mode = 1
auto = 0
s = 1

pin_left = [11,12,13]
pin_right = [15,16,18]

def mode_1(pins):
    d = s
    GPIO.output(pins, 1)
    time.sleep(d)
    GPIO.output(pins, 0)

def mode_2(pins):
    d = s * 0.3
    GPIO.output(pins[0], 1)
    time.sleep(d)
    GPIO.output(pins[0], 0)
    GPIO.output(pins[1], 1)
    time.sleep(d)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[2], 1)
    time.sleep(d)
    GPIO.output(pins[2], 0)

def mode_3(pins):
    d = s * 0.3
    GPIO.output(pins[2], 1)
    time.sleep(d)
    GPIO.output(pins[2], 0)
    GPIO.output(pins[1], 1)
    time.sleep(d)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[0], 1)
    time.sleep(d)
    GPIO.output(pins[0], 0)

def mode_4(pins):
    p_1 = GPIO.PWM(pins[0], 50)
    p_2 = GPIO.PWM(pins[1], 50)
    p_3 = GPIO.PWM(pins[2], 50)
    p_1.start(0)
    p_2.start(0)
    p_3.start(0)
    d = s * 0.017
    for dc in range(0,101, 5):
        p_1.ChangeDutyCycle(dc)
        time.sleep(d)
    p_1.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_2.ChangeDutyCycle(dc)
        time.sleep(d)
    p_2.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_3.ChangeDutyCycle(dc)
        time.sleep(d)
    p_3.ChangeDutyCycle(0)

def mode_5(pins):
    f = 50
    d = s * 0.017
    p_1 = GPIO.PWM(pins[2], f)
    p_2 = GPIO.PWM(pins[1], f)
    p_3 = GPIO.PWM(pins[0], f)
    p_1.start(0)
    p_2.start(0)
    p_3.start(0)
    for dc in range(0,101, 5):
        p_1.ChangeDutyCycle(dc)
        time.sleep(d)
    p_1.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_2.ChangeDutyCycle(dc)
        time.sleep(d)
    p_2.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_3.ChangeDutyCycle(dc)
        time.sleep(d)
    p_3.ChangeDutyCycle(0)

def mode_6(pins):
    count = 20
    d = s/count
    while count != 0:
        D = random.choice([0,1,2])
        GPIO.output(pins[D], 1)
        time.sleep(d)
        GPIO.output(pins[D], 0)
        count -= 1

def mode_7(pins):
    d = s * 0.05
    p_1 = GPIO.PWM(pins[0], 50)
    p_2 = GPIO.PWM(pins[1], 50)
    p_3 = GPIO.PWM(pins[2], 50)
    p_1.start(0)
    p_2.start(0)
    p_3.start(0)
    for dc in range(0,101,10):
        p_1.ChangeDutyCycle(dc)
        p_2.ChangeDutyCycle(dc)
        p_3.ChangeDutyCycle(dc)
        time.sleep(d)
    for dc in range(100, -1, -10):
        p_1.ChangeDutyCycle(dc)
        p_2.ChangeDutyCycle(dc)
        p_3.ChangeDutyCycle(dc)
        time.sleep(d)

def mode_8(pins):
    count = 50
    d = s * 0.5
    while count != 0:
        D = random.choice([0,1,2,3,4,5])
        GPIO.output(pins[D], 1)
        time.sleep(d)
        GPIO.output(pins[D], 0)
        count -= 1

def mode_9(pins):
    p_1 = GPIO.PWM(pins[0], 50)
    p_2 = GPIO.PWM(pins[1], 50)
    p_3 = GPIO.PWM(pins[2], 50)
    p_1.start(100)
    p_2.start(100)
    p_3.start(100)
    d =  s * 0.017
    for dc in range(100,-1, -5):
        p_1.ChangeDutyCycle(dc)
        time.sleep(d)
    for dc in range(100,-1, -5):
        p_2.ChangeDutyCycle(dc)
        time.sleep(d)
    for dc in range(100,-1, -5):
        p_3.ChangeDutyCycle(dc)
        time.sleep(d)

def callback_left(self):
    print("LEFT DETECTED")
    if mode == 1:
        mode_1(pin_left)
    if mode == 2:
        mode_2(pin_left)
    if mode == 3:
        mode_3(pin_left)
    if mode == 4:
        mode_4(pin_left)
    if mode == 5:
        mode_5(pin_left)
    if mode == 6:
        mode_6(pin_left)
    if mode == 7:
        mode_7(pin_left)
    if mode == 8:
        pin_left.extend(pin_right)
        mode_8(pin_left)
    if mode == 9:
        mode_9(pin_left)

def callback_right(self):
    print("RIGHT DETECTED")
    if mode == 1:
        mode_1(pin_right)
    if mode == 2:
        mode_2(pin_right)
    if mode == 3:
        mode_3(pin_right)
    if mode == 4:
        mode_4(pin_right)
    if mode == 5:
        mode_5(pin_right)
    if mode == 6:
        mode_6(pin_right)
    if mode == 7:
        mode_7(pin_right)
    if mode == 8:
        pin_left.extend(pin_right)
        mode_8(pin_left)
    if mode == 9:
        mode_9(pin_right)

def auto_run(auto):
    while auto:
        if GPIO.input(31, 1) or GPIO.input(32, 1):
            auto = 0
        else:
            callback_left(self)
            callback_right(self)

if __name__ == "__main__":
    try:
        GPIO.add_event_detect(31, GPIO.RISING, callback = callback_left, bouncetime = 1000)
        GPIO.add_event_detect(32, GPIO.RISING, callback = callback_right, bouncetime = 1000)
        while True:
            print("""MODE {} IS IN USE
            With a timespan of {} seconds""".format(mode, s))
            print("""OPTIONS  :
           [1] For L/R simultanous activation
           [2] For L/R Sequential <logic> activation Back to Front
           [3] For L/R Sequential <logic> activation Front to Back
           [4] For L/R sequential <PWM> activation Back to Front
           [5] For L/R sequential <PWM> activation Front to Back
           [6] For L/R random activation
           [7] For L/R Simultanous <PWM> activation
           [8] For ALL OUTPUT RANDOM
           [9] For L/R Sequential <PWM> DESactivation Back to Front
           """)
            mode = int(input("Enter your mode:   "))
            s = int(input("Enter your activation time frame:  "))
            auto = (int(input("Automatic [1] OR manual [0]")))
            if auto:
                auto_run(auto)
    except KeyboardInterrupt:
        GPIO.cleanup()