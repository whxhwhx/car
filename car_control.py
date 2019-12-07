import RPi.GPIO as GPIO
import time

# 设定速度，满电时速度太快，图像处理速度跟不上
# 直行快一点，转向慢一点
speed1 = 26        # 直行速度
speed2 = 45       # 拐弯速度
speed4 = 26 
speed3 = 8 
speed_slow = 25
# 轮子定义
leftMotorinput1 = 11   #后轮1
leftMotorinput2 = 7   #后轮2

rightMotorinput1 = 15    #前轮1
rightMotorinput2 = 13    #前轮2

leftMotorEn = 32    #使能端口1
rightMotorEn = 12    #使能端口2

GPIO.setmode(GPIO.BOARD)                         # 设置模式
GPIO.setup(leftMotorinput1,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(leftMotorinput2,GPIO.OUT)             # 此端口为输出模式
GPIO.setup(rightMotorinput1,GPIO.OUT)            # 此端口为输出模式
GPIO.setup(rightMotorinput2,GPIO.OUT)            # 此端口为输出模式
GPIO.setup(leftMotorEn,GPIO.OUT)
GPIO.setup(rightMotorEn,GPIO.OUT)
# 将控制小车运动封装为函数
leftMotorPwm = GPIO.PWM(leftMotorEn,100)         # 配置PWM
leftMotorPwm.start(0)                            # 开始输出PWM
rightMotorPwm = GPIO.PWM(rightMotorEn,100)         # 配置PWM
rightMotorPwm.start(0)                            # 开始输出PWM
# 当使能端口输入低电压时，电机驱动板将不对电机输出电流，电机将不工作。
# 当使能端口输入高电压时，让前轮转向电机正常工作。
# 向前走
def slow_backward():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed_slow)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed_slow)         # 改变PWM占空比，参数为占空比
    
def car_move_forward():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed1)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed1)         # 改变PWM占空比，参数为占空比
# 向后退
def car_move_backward():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed1)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed1)         # 改变PWM占空比，参数为占空比
# 左拐
def car_cycle_left():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed2)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed2)         # 改变PWM占空比，参数为占空比

def adapt_left():
    GPIO.output(leftMotorinput1,GPIO.HIGH)
    GPIO.output(leftMotorinput2,GPIO.LOW)
    GPIO.output(rightMotorinput2,GPIO.HIGH)
    GPIO.output(rightMotorinput1,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed3)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed4)         # 改变PWM占空比，参数为占空比

# 右拐	
def car_cycle_right():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed2)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed2)         # 改变PWM占空比，参数为占空比

def adapt_right():
    GPIO.output(leftMotorinput2,GPIO.HIGH)
    GPIO.output(leftMotorinput1,GPIO.LOW)
    GPIO.output(rightMotorinput1,GPIO.HIGH)
    GPIO.output(rightMotorinput2,GPIO.LOW)
    leftMotorPwm.ChangeDutyCycle(speed4)         # 改变PWM占空比，参数为占空比
    rightMotorPwm.ChangeDutyCycle(speed3)         # 改变PWM占空比，参数为占空比


# 清除
def clean_GPIO():
    GPIO.cleanup()
    leftMotorPwm.stop()                          # 停止输出PWM

# 停止
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

    #car_stop()
    #time.sleep(1)
    #move_right()
    #car_stop()
    clean_GPIO()
