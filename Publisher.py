import paho.mqtt.publish as publish
import time

HOST = "47.106.81.90"
PORT = 1883

# 发送数据端

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("iot_data")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    publish.single("iot_data", "你好 MQTT", qos = 1,hostname=HOST, port=PORT,
                   client_id=client_id,auth = {'username':"admin", 'password':"123456"})