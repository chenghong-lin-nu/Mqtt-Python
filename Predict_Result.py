import os
import csv
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from scipy.ndimage import imread
from sklearn.preprocessing import LabelBinarizer

import tensorflow as tf

from tensorflow_vgg import vgg16
from tensorflow_vgg import utils


img_src = 'https://tf-img-classifier.oss-cn-shanghai.aliyuncs.com/camera_img.jpg'

# 展示图片
#image = io.imread(img_src)
#io.imshow(image)
#io.show()

## 读取模型并返回预测结果

def predict_img_result(img_src):
    print('img_src: '+str(img_src))
    img = utils.load_image(img_src)
    print(''+str(img.shape))

    img = img.reshape((1, 224, 224, 3))

    ####################
    try:
        input_ = tf.placeholder(tf.float32, [None, 224, 224, 3])

        feed_dict = {input_: img}
        code = sess.run(vgg.relu6, feed_dict=feed_dict)

        inputs_ = graph.get_tensor_by_name('inputs:0')
        predicted = graph.get_tensor_by_name('op_predicted:0')
    except:
        tf.reset_default_graph()

        sess = tf.Session()
        # First let's load meta graph and restore weights
        saver = tf.train.import_meta_graph('checkpoints/animals.ckpt.meta')
        saver.restore(sess, tf.train.latest_checkpoint('checkpoints/'))

        # Now, let's access and create placeholders variables and
        # create feed-dict to feed new data

        graph = tf.get_default_graph()

        input_ = tf.placeholder(tf.float32, [None, 224, 224, 3])
        vgg = vgg16.Vgg16()
        vgg.build(input_)

        feed_dict = {input_: img}
        code = sess.run(vgg.relu6, feed_dict=feed_dict)

        inputs_ = graph.get_tensor_by_name('inputs:0')
        predicted = graph.get_tensor_by_name('op_predicted:0')

    feed = {inputs_: code}
    # 预测结果分别表示为['bird' 'cat' 'dog' 'fish' 'tiger']
    # prediction是一个list
    prediction = sess.run(predicted, feed_dict=feed).squeeze()
    print(prediction)
    sess.close()
    return prediction.tolist()
