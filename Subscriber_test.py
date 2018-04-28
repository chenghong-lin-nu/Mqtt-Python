import paho.mqtt.client as mqtt
import time
from Predict_Result import predict_img_result
import json
from Publisher import *

HOST = "47.106.81.90"
PORT = 1883

# 接收数据端

def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("control_camera_iot")
    print('subscribed!')

# 接收到数据
def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))
    img_url = msg.payload.decode("utf-8")


if __name__ == '__main__':
    client_loop()