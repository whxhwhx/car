import RPi.GPIO as GPIO
import time

speed1 = 40 
speed2 = 38

front_left_En = 32
front_right_En = 33 

back_left_En = 15
back_right_En = 12 

front_left_input1 = 37 
front_left_input2 = 36 
front_right_input1 = 31 
front_right_input2 = 29
   
back_left_input1 = 16
back_left_input2 = 18 
back_right_input1 = 11
back_right_input2 = 13

GPIO.setmode(GPIO.BOARD)                         # 设置模式

GPIO.setup(front_left_input1,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(front_left_input2,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(front_right_input1,GPIO.OUT)            # 此端口为输出模式
GPIO.setup(front_right_input2,GPIO.OUT)            # 此端口为输出模式

GPIO.setup(back_left_input1,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(back_left_input2,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(back_right_input1,GPIO.OUT)            # 此端口为输出模式
GPIO.setup(back_right_input2,GPIO.OUT)            # 此端口为输出模式

GPIO.setup(front_left_En,GPIO.OUT)
GPIO.setup(front_right_En,GPIO.OUT)
GPIO.setup(back_left_En,GPIO.OUT)
GPIO.setup(back_right_En,GPIO.OUT)

front_leftPwm = GPIO.PWM(front_left_En,100)         # 配置PWM
front_leftPwm.start(0)                            # 开始输出PWM
front_rightPwm = GPIO.PWM(front_right_En,100)         # 配置PWM
front_rightPwm.start(0)

back_leftPwm = GPIO.PWM(back_left_En,100)         # 配置PWM
back_leftPwm.start(0)                            # 开始输出PWM
back_rightPwm = GPIO.PWM(back_right_En,100)         # 配置PWM
back_rightPwm.start(0)

def car_move_forward():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.HIGH)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    front_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比


def car_move_backward():
    GPIO.output(front_left_input2,GPIO.HIGH)
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.HIGH)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.HIGH)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.HIGH)
    GPIO.output(back_right_input1,GPIO.LOW)

    front_rightPwm.ChangeDutyCycle(24)         # 改变PWM占空比，参数为占空比
    front_leftPwm.ChangeDutyCycle(24)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(24)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(24)         # 改变PWM占空比，参数为占空比
    

def car_go_right():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.HIGH)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.HIGH)
    GPIO.output(back_right_input1,GPIO.HIGH)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_leftPwm.ChangeDutyCycle(35)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(36)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(35)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(37)         # 改变PWM占空比，参数为占空比

def car_go_left():
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_left_input2,GPIO.HIGH)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.HIGH)

    front_rightPwm.ChangeDutyCycle(35)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(36)         # 改变PWM占空比，参数为占空比
    front_leftPwm.ChangeDutyCycle(35)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(37)         # 改变PWM占空比，参数为占空比
    
def car_forward_left():
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_leftPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(23)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(23)         # 改变PWM占空比，参数为占空比

def car_forward_right():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.HIGH)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_leftPwm.ChangeDutyCycle(23)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(23)         # 改变PWM占空比，参数为占空比
    
def car_backward_left():
    GPIO.output(front_left_input2,GPIO.HIGH)
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.HIGH)
    GPIO.output(back_right_input1,GPIO.LOW)

    front_leftPwm.ChangeDutyCycle(20)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(20)         # 改变PWM占空比，参数为占空比
    
def car_backward_right():
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.HIGH)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.HIGH)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.LOW)

    front_leftPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(20)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(20)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(0)         # 改变PWM占空比，参数为占空比
 

def car_stop():
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.LOW)

    GPIO.output(front_left_En,GPIO.LOW)
    GPIO.output(front_right_En,GPIO.LOW)
    GPIO.output(back_right_En,GPIO.LOW)
    GPIO.output(back_left_En,GPIO.LOW)

def car_cycle_right():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.HIGH)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.HIGH)

    front_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比


def car_cycle_left():
    GPIO.output(front_left_input2,GPIO.HIGH)
    GPIO.output(front_left_input1,GPIO.LOW)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.HIGH)
    GPIO.output(back_left_input1,GPIO.LOW)
    GPIO.output(back_right_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.HIGH)

    front_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    front_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比

    back_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比

def adapt_left():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.HIGH)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    front_leftPwm.ChangeDutyCycle(13)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(13)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比

def adapt_right():
    GPIO.output(front_left_input1,GPIO.HIGH)
    GPIO.output(front_left_input2,GPIO.LOW)
    GPIO.output(front_right_input1,GPIO.HIGH)
    GPIO.output(front_right_input2,GPIO.LOW)
    GPIO.output(back_left_input1,GPIO.HIGH)
    GPIO.output(back_left_input2,GPIO.LOW)
    GPIO.output(back_right_input1,GPIO.HIGH)
    GPIO.output(back_right_input2,GPIO.LOW)

    front_rightPwm.ChangeDutyCycle(13)         # 改变PWM占空比，参数为占空比
    back_rightPwm.ChangeDutyCycle(13)         # 改变PWM占空比，参数为占空比
    front_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比
    back_leftPwm.ChangeDutyCycle(25)         # 改变PWM占空比，参数为占空比



def clean_GPIO():
    GPIO.cleanup()
    

if __name__ == '__main__':
    car_move_forward()
    time.sleep(1)

    clean_GPIO()
