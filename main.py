import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup([11,12,13,15,16,18], GPIO.OUT)
GPIO.setup([31,32], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mode = 1
delay = 2

pin_left = [11,12,13]
pin_right = [15,16,18]

def mode_1(choice):
    print("THIS IS MODE 1")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins, 1)
    time.sleep(delay)
    GPIO.output(pins, 0)

def mode_2(choice):
    print("THIS IS MODE 2")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins[0], 1)
    time.sleep(delay/3)
    GPIO.output(pins[0], 0)
    GPIO.output(pins[1], 1)
    time.sleep(delay/3)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[2], 1)
    time.sleep(delay/3)
    GPIO.output(pins[2], 0)

def mode_3(choice):
    print("THIS IS MODE 3")
    if choice:
        pins = pin_left
    else:
        pins = pin_right
    GPIO.output(pins[2], 1)
    time.sleep(delay/3)
    GPIO.output(pins[2], 0)
    GPIO.output(pins[1], 1)
    time.sleep(delay/3)
    GPIO.output(pins[1], 0)
    GPIO.output(pins[0], 1)
    time.sleep(delay/3)
    GPIO.output(pins[0], 0)

def callback_left(self):
    if mode == 1:
        mode_1(1)
    if mode == 2:
        mode_2(1)
    if mode == 3:
        mode_3(1)

def callback_right(self):
    if mode == 1:
        mode_1(0)
    if mode == 2:
        mode_2(0)
    if mode == 3:
        mode_3(0)


if __name__ == "__main__":
    try:
        GPIO.add_event_detect(31, GPIO.RISING, callback = callback_left, bouncetime = 200)
        GPIO.add_event_detect(32, GPIO.RISING, callback = callback_right, bouncetime = 200)
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
        GPIO.cleanup