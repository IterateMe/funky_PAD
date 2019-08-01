import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)
GPIO.setup([11,12,13,15,16,18], GPIO.OUT)
GPIO.setup([31,32], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mode = 1

pin_left = [11,12,13]
pin_right = [15,16,18]

def mode_1(choice):
    print("THIS IS MODE 1")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins, 1)
    time.sleep(1.5)
    GPIO.output(pins, 0)

def mode_2(choice):
    print("THIS IS MODE 2")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins[0], 1)
    time.sleep(0.5)
    GPIO.output(pins[0], 0)
    GPIO.output(pins[1], 1)
    time.sleep(0.5)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[2], 1)
    time.sleep(0.5)
    GPIO.output(pins[2], 0)

def mode_3(choice):
    print("THIS IS MODE 3")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins[2], 1)
    time.sleep(0.5)
    GPIO.output(pins[2], 0)
    GPIO.output(pins[1], 1)
    time.sleep(0.5)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[0], 1)
    time.sleep(0.5)
    GPIO.output(pins[0], 0)

def mode_4(choice):
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    p_1 = GPIO.PWM(pins[0], 50)
    p_2 = GPIO.PWM(pins[1], 50)
    p_3 = GPIO.PWM(pins[2], 50)
    p_1.start(0)
    p_2.start(0)
    p_3.start(0)
    for dc in range(0,101, 5):
        p_1.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_1.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_2.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_2.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_3.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_3.ChangeDutyCycle(0)

def mode_5(choice):
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    p_1 = GPIO.PWM(pins[2], 50)
    p_2 = GPIO.PWM(pins[1], 50)
    p_3 = GPIO.PWM(pins[0], 50)
    p_1.start(0)
    p_2.start(0)
    p_3.start(0)
    for dc in range(0,101, 5):
        p_1.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_1.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_2.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_2.ChangeDutyCycle(0)
    for dc in range(0,101, 5):
        p_3.ChangeDutyCycle(dc)
        time.sleep(0.1)
    p_3.ChangeDutyCycle(0)

def mode_6(choice):
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    count = 20
    while count != 0:
        D = random.choice([0,1,2])
        GPIO.output(pins[D], 1)
        time.sleep(0.05)
        GPIO.output(pins[D], 0)
        count -= 1

def callback_left(self):
    if mode == 1:
        mode_1(1)
    if mode == 2:
        mode_2(1)
    if mode == 3:
        mode_3(1)
    if mode == 4:
        mode_4(1)
    if mode == 5:
        mode_5(1)
    if mode == 6:
        mode_6(1)

def callback_right(self):
    if mode == 1:
        mode_1(0)
    if mode == 2:
        mode_2(0)
    if mode == 3:
        mode_3(0)
    if mode == 4:
        mode_4(0)
    if mode == 5:
        mode_5(0)
    if mode == 6:
        mode_6(0)

if __name__ == "__main__":
    try:
        GPIO.add_event_detect(31, GPIO.RISING, callback = callback_left, bouncetime = 700)
        GPIO.add_event_detect(32, GPIO.RISING, callback = callback_right, bouncetime = 700)
        while True:
            global mode
            print("Your actual mode:  ", mode)
            print("""Choose an option between those two:
           [1] For simultanous activation
           [2] For Sequential <logic> activation Back to front
           [3] For Sequential <logic> activation Front to back
           [4] For sequential <PWM> activation Back to front
           [5] For sequential <PWM> activation Front to back
           [6] For random activation
           """)
            mode = int(input())

    except KeyboardInterrupt:
        GPIO.cleanup()