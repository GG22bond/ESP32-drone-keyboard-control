import pygame
import sys
import socket

host = '192.168.1.11'  # drone IP
port = 2390  # drone port

# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))
    return win

def getKey(keyName):
    ans = False
    for event in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    if keyInput[myKey]:
        ans = True
    return ans

def send_data(data):
    s.sendto(data.encode(), (host, port))

def main():
    global text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if getKey("LEFT"):
        text[0][0] = max(text[0][0] - 1, 0)
        print("Left")
    elif getKey("RIGHT"):
        text[0][0] = min(text[0][0] + 1, 255)
        print("Right")
    elif getKey("UP"):
        text[1][0] = min(text[1][0] + 1, 255)
        print("Forward")
    elif getKey("DOWN"):
        text[1][0] = max(text[1][0] - 1, 0)
        print("Back")
    elif getKey("a"):
        text[2][0] = max(text[2][0] - 1, 0)
        print("Counterclockwise")
    elif getKey("d"):
        text[2][0] = min(text[2][0] + 1, 255)
        print("Clockwise")
    elif getKey("w"):
        text[3][0] = min(text[3][0] + 1,255)
        print("Lift")
    elif getKey("s"):
        text[3][0] = max(text[3][0] - 1, 0)
        print("Drop")

    elif getKey("TAB"):
        text[4][0] = 24
        print("take off")

    elif getKey("SPACE"):
        text[4][0] = 72
        print("landing")

    elif getKey("b"):
        text[4][0] = 136
        print("stop")

    else:
        text = ([128], [128], [128], [128],[8])  # 初始化

  #  print(text)
    send_data(str(text))

if __name__ == "__main__":
    win = init()
    text = ([128], [128], [128], [128],[8])
    while True:
        main()
