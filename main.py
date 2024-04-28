import socket
import time
from machine import Timer
import drone
import network

# 构建四轴对象，无头方式
d = drone.DRONE(flightmode=0)

# 水平放置四轴，等待校准通过后蓝灯常亮
while True:
    # 打印校准信息
    print(d.read_cal_data())
    # 校准通过
    if d.read_calibrated():
        print(d.read_cal_data())
        break
    time.sleep_ms(100)

# 连接WiFi
def connect_to_wifi(ssid, password):
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    if not wlan_sta.isconnected():
        print('connecting to network...')
        wlan_sta.connect(ssid, password)
        while not wlan_sta.isconnected():
            pass
    print('网络配置:', wlan_sta.ifconfig())

# WiFi
wifi_ssid = "ChinaNet-re3T" # ssid
wifi_password = "19970305" # password
connect_to_wifi(wifi_ssid, wifi_password)

# socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 2390))

data, addr = s.recvfrom(128)
print(addr)

s.connect(addr)
s.setblocking(False)

# Socket接收数据
def Socket_rece(tim):
    try:
        data = s.recv(128)  # 128

        text = eval(data.decode())

        control_data = text[:4]
        button_states = text[4]

        # 打印控制数据和按键状态
        print('control:', control_data)
        print('button states:', button_states)

        # 将摇杆值转化为飞控控制值。
        for i in range(4):
            if 100 < control_data[i][0] < 155:
                control_data[i][0] = 0
            elif control_data[i][0] <= 100:
                control_data[i][0] -= 100
            else:
                control_data[i][0] -= 155

        print('control:', control_data)

        # 控制飞行器
        d.control(rol=control_data[0][0], pit=control_data[1][0], yaw=control_data[2][0], thr=control_data[3][0])

        # 检测X/Y/A/B按键
        if button_states[0] == 24:  # Y键按下
            print('TAB')
            # 起飞，起飞后120cm位置悬停。distance范围:30~2000 cm
            d.take_off(distance=40)
        elif button_states[0] == 72:  # A键按下
            print('SPACE')
            # 降落，允许control
            d.landing()
        elif button_states[0] == 136:  # X键按下,紧急停止
            print('b')
            # 降落，不允许control
            d.stop()

    except OSError:
        pass

tim = Timer(1)
tim.init(period=5, mode=Timer.PERIODIC, callback=Socket_rece)

