# 收集数据，赛道照片和对应的前、后、左、右、4停 # 对应图片和相应的标签值
import io
import w4_car_control 
import os
os.environ['SDL_VIDEODRIVE'] = 'x11'
import pygame     # 检测模块
from time import ctime,sleep,time
import threading
import numpy as np

is_capture_running = True

def my_car_control(): 
    global is_capture_running
    pygame.init()
    pygame.display.set_mode((1,1))            # 窗口
    w4_car_control.car_stop()
    sleep(0.1)
    print("Start control!")
 
    while is_capture_running:
        # get input from human driver
        # 
        for event in pygame.event.get():
            # 判断事件是不是按键按下的事件
            if event.type == pygame.KEYDOWN:  
                key_input = pygame.key.get_pressed()     # 可以同时检测多个按键

                print(key_input[pygame.K_w], key_input[pygame.K_a], key_input[pygame.K_d])

                if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d] and not key_input[pygame.K_s]:
                    print("Forward")
                    w4_car_control.car_move_forward()
                elif key_input[pygame.K_a] and not key_input[pygame.K_w] and not key_input[pygame.K_d] and not key_input[pygame.K_s]:
                    print("Left")
                    w4_car_control.car_go_left()
                    sleep(0.1)
                elif key_input[pygame.K_d] and not key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_s]:
                    print("Right")
                    w4_car_control.car_go_right()
                    sleep(0.1)
                elif key_input[pygame.K_w] and key_input[pygame.K_a] and not key_input[pygame.K_d] and not key_input[pygame.K_s]:
                    print('forward left')
                    w4_car_control.car_forward_left()
                    sleep(0.1)
                elif key_input[pygame.K_w] and key_input[pygame.K_d] and not key_input[pygame.K_a] and not key_input[pygame.K_s]:
                    print('forward right')
                    w4_car_control.car_forward_right()
                    sleep(0.1)
                elif key_input[pygame.K_s] and not key_input[pygame.K_d] and not key_input[pygame.K_a] and not key_input[pygame.K_w]:
                    print("Backward")
                    w4_car_control.car_move_backward()
                elif key_input[pygame.K_s] and key_input[pygame.K_a] and not key_input[pygame.K_d] and not key_input[pygame.K_w]:
                    print("Backward left")
                    w4_car_control.car_backward_left()
                    sleep(0.1)
                elif key_input[pygame.K_s] and key_input[pygame.K_d] and not key_input[pygame.K_a] and not key_input[pygame.K_w]:
                    print("Backward right")
                    w4_car_control.car_backward_right()
                    sleep(0.1)
                elif key_input[pygame.K_e]:
                    print("cycle right")
                    w4_car_control.car_cycle_right()
                    sleep(0.1)
                elif key_input[pygame.K_q]:
                    print("cycle left")
                    w4_car_control.car_cycle_left()
                    sleep(0.1)
                # 按下k停止键，停止
                elif key_input[pygame.K_k]:
                    w4_car_control.car_stop()
                    is_capture_running = False 
            # 检测按键是不是抬起
            elif event.type == pygame.KEYUP:
                #key_input = pygame.key.get_pressed()
                print("Stop")
                w4_car_control.car_stop()
                #car_control.cleanGPIO()
    #w4_car_control.clean_GPIO()

if __name__ == '__main__':
    my_car_control()

    while is_capture_running:
        pass

    print("Done!")
    w4_car_control.car_stop()
    w4_car_control.clean_GPIO()

