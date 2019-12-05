import serial
import time
import threading
import w4_car_control
 
ACCData=[0.0]*8
GYROData=[0.0]*8
AngleData=[0.0]*8         #定义三个数组，分别存储加速度角速度与角度的值
 
FrameState = 0            #通过0x后面的值判断属于哪一种情况
Bytenum = 0               #读取到这一段的第几位
CheckSum = 0              #求和校验位         
angle = [] 

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
    while(1):
        #datahex = (ser.read(33).hex()) #之前转换成了字符串，一位变成了两位
        datahex = ser.read(33)       #不用hex()转化，直接用read读取的即是16进制
        DueData(datahex)            #调用程序进行处理


def get_turn_right_angle(angle):
    angle = angle-90
    if angle<(-180):
        angle = -(-180-(angle+180))
    return angle
 
if __name__=='__main__':  #主函数

    ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.5)  # 打开端口，改到循环外
    print(ser.is_open)
    ang_thread = threading.Thread(target=get_thread, args=())
    ang_thread.setDaemon(True)
    ang_thread.start()
    time.sleep(1)

    try:
        '''
        old_angle = start_angle
        start_angle = get_turn_right_angle(start_angle) 
        print('old', old_angle)
        print('new_start', start_angle)
        input('enter')
        while abs(angle[2]-start_angle) > 20:   
            w4_car_control.car_cycle_right()

        w4_car_control.car_stop()
        print(angle[2])
        time.sleep(4)
        print(angle[2])
        '''
        dire_angle = 0.0
        print('dire_angle',dire_angle)
        input()
        while(1):
            print(angle[2])
            time.sleep(0.2)
            '''now_angle = angle[2]
            if abs(abs(now_angle)-abs(dire_angle))<2.5:
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
                    '''
    finally:
        ser.close()
        w4_car_control.clean_GPIO()


