import paho.mqtt.client as mqtt
from Predict_Result import predict_img_result, init_vgg
import json
import paho.mqtt.publish as publish
import time
import tensorflow as tf

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
    client.subscribe("iot_data_pub")

# 接收到数据
def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))
    img_url = msg.payload.decode("utf-8")

    prob_list = predict_img_result(img_url, input_, sess, vgg, graph)
    prob_dict = {}
    prob_dict['bird'] = prob_list[0]
    prob_dict['cat'] = prob_list[1]
    prob_dict['dog'] = prob_list[2]
    prob_dict['fish'] = prob_list[3]
    prob_dict['tiger'] = prob_list[4]

    show_list = prob_dict

    prob_json = json.dumps(prob_dict)
    print('prob_json: ' + str(prob_json))

    # 调用Publisher发送
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    publish.single("iot_data", prob_json, qos=1, hostname=HOST, port=PORT,
                   client_id=client_id, auth={'username': "admin", 'password': "123456"})

    # 发送到安卓端和上面的有所不同
    show_list['img_url'] = img_url
    show_list = json.dumps(show_list)
    print('show_list长得什么样呢?? '+str(show_list))
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    publish.single("android_show_data", show_list, qos=1, hostname=HOST, port=PORT,
                   client_id=client_id, auth={'username': "admin", 'password': "123456"})


if __name__ == '__main__':
    input_ = tf.placeholder(tf.float32, [None, 224, 224, 3])
    vgg = init_vgg(input_)

    sess = tf.Session()
    # First let's load meta graph and restore weights
    saver = tf.train.import_meta_graph('checkpoints/animals.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint('checkpoints/'))

    graph = tf.get_default_graph()

    client_loop()