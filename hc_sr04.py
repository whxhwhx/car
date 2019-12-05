import time
import car_control
import RPi.GPIO as GPIO
 
trigger_pin = 7 
echo_pin = 22 
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin,GPIO.OUT)
GPIO.setup(echo_pin,GPIO.IN)
 
def wait_for_echo(value,timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count>0:
        count = count-1
 
def get_distance():

    GPIO.output(trigger_pin,True)
    time.sleep(0.00015)
    GPIO.output(trigger_pin,False)

    wait_for_echo(True,10000)
    start = time.time()
    wait_for_echo(False,10000)
    finish = time.time()
    pulse_len = finish-start
    distance_cm = pulse_len/0.000058
    return distance_cm

def main():
    try:
        while True:
            print("距离 = %f cm"%get_distance())
            time.sleep(0.1)
    except:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
