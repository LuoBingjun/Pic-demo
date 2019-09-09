import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

os.path.join()

with open('node2human.txt','r') as f:
    node_id_to_name = eval(f.read())

with tf.gfile.GFile('/Users/liuyunrui/PycharmProjects/tensor/model/classify_image_graph_def.pb','rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')



with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    
    image_data = tf.gfile.GFile('/Users/liuyunrui/PycharmProjects/tensor/model/image/tiger.jpg', 'rb').read()
    predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)
    top_k = predictions.argsort()[-5:][::-1]
    for node_id in top_k:
        human_string = node_id_to_name[node_id]
        score = predictions[node_id]
        print('%s (score = %.5f)' % (human_string, score))
