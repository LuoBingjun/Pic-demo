import tensorflow as tf
import numpy as np
import os
import sys
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def classify(id,filename):
    with open(os.path.join(BASE_DIR, 'app/processors/classifier/node2human.txt'),'r') as f:
        node_id_to_name = eval(f.read())

    with tf.gfile.GFile(os.path.join(BASE_DIR, 'app/processors/classifier/classify_image_graph_def.pb'),'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        
        image_data = tf.gfile.GFile(os.path.join(BASE_DIR, 'media/%s'%(filename)), 'rb').read()
        predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        top_k = predictions.argsort()[-5:][::-1]
        res = []
        for node_id in top_k:
            res.append({
                'class':str(node_id_to_name[node_id]),
                'score': float(predictions[node_id])
            })
    return {
        'id': id,
        'res': res
    }