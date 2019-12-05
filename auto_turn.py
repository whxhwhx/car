import threading
import io
import time
import RPi.GPIO as GPIO
import w4_car_control
import picamera
import glob
import serial
#from keras.models import load_model
#import tensorflow as tf
#from PIL import Image
#import picamera.array
#import numpy as np

# serial 
ACCData=[0.0]*8
GYROData=[0.0]*8
AngleData=[0.0]*8         #定义三个数组，分别存储加速度角速度与角度的值

FrameState = 0            #通过0x后面的值判断属于哪一种情况
Bytenum = 0               #读取到这一段的第几位
CheckSum = 0              #求和校验位         
angle = []
dire_angle=0.0

#hc_sr04
trigger_pin3 = 7 
echo_pin3 = 22 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin3,GPIO.OUT)
GPIO.setup(echo_pin3,GPIO.IN)
 
event1 = threading.Event()

def DueData(inputdata):   #新增的核心程序，对读取的数据进行划分，各自读到对应的数组里
    global  FrameState    #在局部修改全局变量，要进行global的定义
    global  Bytenum
    global  CheckSum
    global angle
    for data in inputdata:  #在输入的数据进行遍历
        if FrameState==0:   #当未确定状态的时候，进入以下判断
            if data==0x55 and Bytenum==0: #0x55位于第一位时候，开始读取数据，增大bytenum
                CheckSum=data
                Bytenum=1
                continue
            elif data==0x51 and Bytenum==1:#在byte不为0 且 识别到 0x51 的时候，改变frame
                CheckSum+=data
                FrameState=1
                Bytenum=2
            elif data==0x52 and Bytenum==1: #同理
                CheckSum+=data
                FrameState=2
                Bytenum=2
            elif data==0x53 and Bytenum==1:
                CheckSum+=data
                FrameState=3
                Bytenum=2
        elif FrameState==1: # acc    #已确定数据代表加速度
            if Bytenum<10:            # 读取8个数据
                ACCData[Bytenum-2]=data # 从0开始
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):  #假如校验位正确
                    pass
                    #print(get_acc(ACCData))
                CheckSum=0                  #各数据归零，进行新的循环判断
                Bytenum=0
                FrameState=0
        elif FrameState==2: # gyro
            if Bytenum<10:
                GYROData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):
                    pass
                    #print(get_gyro(GYROData))
                CheckSum=0
                Bytenum=0
                FrameState=0
        elif FrameState==3: # angle
            if Bytenum<10:
                AngleData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):
                    angle = list(get_angle(AngleData))
                CheckSum=0
                Bytenum=0
                FrameState=0


def get_acc(datahex):  #加速度
    axl = datahex[0]
    axh = datahex[1]
    ayl = datahex[2]
    ayh = datahex[3]
    azl = datahex[4]
    azh = datahex[5]

    k_acc = 16

    acc_x = (axh << 8 | axl) / 32768 * k_acc
    acc_y = (ayh << 8 | ayl) / 32768 * k_acc
    acc_z = (azh << 8 | azl) / 32768 * k_acc
    if acc_x >= k_acc:
        acc_x -= 2 * k_acc
    if acc_y >= k_acc:
        acc_y -= 2 * k_acc
    if acc_z >= k_acc:
        acc_z-= 2 * k_acc

    return acc_x,acc_y,acc_z


def get_gyro(datahex):                                          #陀螺仪
    wxl = datahex[0]
    wxh = datahex[1]
    wyl = datahex[2]
    wyh = datahex[3]
    wzl = datahex[4]
    wzh = datahex[5]
    k_gyro = 2000

    gyro_x = (wxh << 8 | wxl) / 32768 * k_gyro
    gyro_y = (wyh << 8 | wyl) / 32768 * k_gyro
    gyro_z = (wzh << 8 | wzl) / 32768 * k_gyro
    if gyro_x >= k_gyro:
        gyro_x -= 2 * k_gyro
    if gyro_y >= k_gyro:
        gyro_y -= 2 * k_gyro
    if gyro_z >=k_gyro:
        gyro_z-= 2 * k_gyro
    return gyro_x,gyro_y,gyro_z


def get_angle(datahex):                                 #角度
    rxl = datahex[0]
    rxh = datahex[1]
    ryl = datahex[2]
    ryh = datahex[3]
    rzl = datahex[4]
    rzh = datahex[5]
    k_angle = 180

    angle_x = (rxh << 8 | rxl) / 32768 * k_angle
    angle_y = (ryh << 8 | ryl) / 32768 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >=k_angle:
        angle_z-= 2 * k_angle

    return angle_x,angle_y,angle_z


def get_thread():
    global ser
    while(1):
        #datahex = (ser.read(33).hex()) #之前转换成了字符串，一位变成了两位
        datahex = ser.read(33)       #不用hex()转化，直接用read读取的即是16进制
        DueData(datahex)            #调用程序进行处理


def wait_for_echo(value,timeout, echo_pin):
    count = timeout
    while GPIO.input(echo_pin) != value and count>0:
        count = count-1
 
def get_distance(trigger_pin, echo_pin):
    global distance_cm, distance1,distance2
    GPIO.output(trigger_pin,True)
    time.sleep(0.00015)
    GPIO.output(trigger_pin,False)

    wait_for_echo(True,10000, echo_pin)
    start = time.time()
    wait_for_echo(False,10000, echo_pin)
    finish = time.time()
    pulse_len = finish-start
    distance_cm = pulse_len/0.000058
    time.sleep(0.01)

def hc_1():
    while True:
        event1.wait()
        get_distance(trigger_pin3, echo_pin3)
        #print('distance_front = ', distance_cm)


def get_max_prob_num(predictions_array):
    prediction_edit = np.zeros([1, 3])
    for i in range(0, 3):
        if predictions_array[0][i] == predictions_array.max():
            prediction_edit[0][i] = 1
            return i
    return 2

def control_car(action_num):
    global distance_cm
    if action_num == 0:
        event1.clear()
        time.sleep(0.2)
        w4_car_control.car_go_left()
        time.sleep(0.5)
        w4_car_control.car_stop()
        distance_cm = 50
        event1.set()
    elif action_num == 1:
        event1.clear()
        time.sleep(0.2)
        w4_car_control.car_go_right()
        time.sleep(0.5)
        w4_car_control.car_stop()
        distance_cm = 50
        event1.set()
    elif action_num == 2:
        w4_car_control.car_stop()
        time.sleep(1)
    else:
        w4_car_control.car_move_backward()
        #w4_car_control.car_stop()

def judge(stream):
    global model, graph
    try:
        stream.seek(0)
        image = Image.open(stream)
        image_np = np.array(image)
        camera_data_array = np.expand_dims(image_np, axis=0)
        current_time = time.time()
        with graph.as_default():
            prediction_array = model.predict(camera_data_array, batch_size=20)
            # 输出的是概率，比如[0.1,0.1,0.8,0.05,0.04]
        #print(prediction_array)
        action_num = get_max_prob_num(prediction_array)
        control_car(action_num)
    finally:
        stream.seek(0)
        stream.truncate()
    
def smart_forward():
    global angle,dire_angle
    now_angle = angle[2]
    if abs(abs(now_angle)-abs(dire_angle))<1.8:
        w4_car_control.car_move_forward()
        time.sleep(0.1)
    elif dire_angle == 180 or dire_angle== -180:
        if now_angle>0:
            w4_car_control.adapt_left()
        else:
            w4_car_control.adapt_right()
    else:
        if now_angle<dire_angle:
            w4_car_control.adapt_left()
        else:
            w4_car_control.adapt_right()


def smart_go_right():
    global dire_angle,distance_cm,event1
    event1.clear()
    dire_angle = dire_angle-90 
    if dire_angle == -270.0:
        dire_angle = 90.0
    while abs(angle[2]-dire_angle) > 18:   
        w4_car_control.car_cycle_right()
    w4_car_control.car_cycle_left()
    time.sleep(0.05)
    w4_car_control.car_stop()
    distance_cm = 40
    event1.set()

def smart_go_left():
    global dire_angle,distance_cm,event1
    event1.clear()
    dire_angle = dire_angle+90 
    if dire_angle == 270.0:
        dire_angle = -90.0
    while abs(angle[2]-dire_angle) > 18:   
        w4_car_control.car_cycle_left()
    w4_car_control.car_cycle_right()
    time.sleep(0.05)
    w4_car_control.car_stop()
    distance_cm = 40
    event1.set()

def main():
    global ser ,distance_cm, model, graph, angle
    stream = io.BytesIO()

    #model_loaded = glob.glob('model/*.h5') 
    #for single_mod in model_loaded:
    #    model = load_model(single_mod)
    #graph = tf.get_default_graph()
    print('ok')

    # open camera
    #camera = picamera.PiCamera(resolution=(160, 120))
    #camera.brightness = 72

    ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.5)  # 打开端口，改到循环外

    dis_thread1 = threading.Thread(target=hc_1, args=())
    dis_thread1.setDaemon(True)

    ang_thread = threading.Thread(target=get_thread, args=())
    ang_thread.setDaemon(True)

    ang_thread.start()
    dis_thread1.start()

    print('set')
    event1.set()

    time.sleep(2)
    print(angle[2])

    try:
        while True:
            if distance_cm<20:
                w4_car_control.car_move_backward()
                time.sleep(0.2)
                w4_car_control.car_stop()
                time.sleep(0.2)
                while distance_cm<14:
                    w4_car_control.car_move_backward()
                w4_car_control.car_move_forward()
                time.sleep(0.1)
                w4_car_control.car_stop()
                time.sleep(0.1)
                #camera.capture(stream, format='jpeg')
                #judge(stream)
                smart_go_right()
            else:
                smart_forward()
    finally:
        #camera.close()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
