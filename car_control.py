import RPi.GPIO as GPIO
import time

speed1 = 26        
speed2 = 45       
speed4 = 26 
speed3 = 8 
speed_slow = 25

leftMotorinput1 = 11   
leftMotorinput2 = 7   

rightMotorinput1 = 15    
rightMotorinput2 = 13    

leftMotorEn = 32    
rightMotorEn = 12   

GPIO.setmode(GPIO.BOARD)                      
GPIO.setup(leftMotorinput1,GPIO.OUT)         
GPIO.setup(leftMotorinput2,GPIO.OUT)        
GPIO.setup(rightMotorinput1,GPIO.OUT)      
GPIO.setup(rightMotorinput2,GPIO.OUT)     
GPIO.setup(leftMotorEn,GPIO.OUT)
GPIO.setup(rightMotorEn,GPIO.OUT)

leftMotorPwm = GPIO.PWM(leftMotorEn,100) 
leftMotorPwm.start(0)                   
rightMotorPwm = GPIO.PWM(rightMotorEn,100)   
rightMotorPwm.start(0)                      


def slow_backward():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed_slow)   
    rightMotorPwm.ChangeDutyCycle(speed_slow)   
    

def car_move_forward():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed1)     


def car_move_backward():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed1)      
    rightMotorPwm.ChangeDutyCycle(speed1)      


def car_cycle_left():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed2)   
    rightMotorPwm.ChangeDutyCycle(speed2)   


def adapt_left():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed3)     
    rightMotorPwm.ChangeDutyCycle(speed4)     


def car_cycle_right():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed2)       
    rightMotorPwm.ChangeDutyCycle(speed2)       


def adapt_right():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed4)        
    rightMotorPwm.ChangeDutyCycle(speed3)        


def clean_GPIO():
    GPIO.cleanup()
    leftMotorPwm.stop()                        

def car_stop():
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    GPIO.output(leftMotorEn,GPIO.LOW)
    GPIO.output(rightMotorEn,GPIO.LOW)


if __name__ == '__main__':
    adapt_right()
    time.sleep(1)
    adapt_left()
    time.sleep(1)
    clean_GPIO()
