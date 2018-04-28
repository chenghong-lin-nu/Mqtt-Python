import paho.mqtt.publish as publish
import time
import json

HOST = "47.106.81.90"
PORT = 1883

# 发送数据端

#def on_connect(client, userdata, flags, rc):
#    print("Connected with result code "+str(rc))
#    client.subscribe("iot_data")

#def on_message(client, userdata, msg):
#    print(msg.topic+" "+msg.payload.decode("utf-8"))

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    img_src = "https://tf-img-classifier.oss-cn-shanghai.aliyuncs.com/camera_img.jpg"
    prob_dict = {}
    prob_dict['bird'] = 0.00011512912169564515
    prob_dict['cat'] = 0.45457378029823303
    prob_dict['dog'] = 0.18857626616954803
    prob_dict['fish'] = 0.35237210988998413
    prob_dict['tiger'] = 0.004362653475254774
    prob_dict['img_url'] = img_src
    prob_dict = json.dumps(prob_dict)
    publish.single("android_show_data", prob_dict, qos = 1,hostname=HOST, port=PORT,
                   client_id=client_id,auth = {'username':"admin", 'password':"123456"})