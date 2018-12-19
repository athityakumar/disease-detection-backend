import tensorflow as tf, sys
from operator import itemgetter


IMAGES_PATH = "./images"
MODELS_PATH = "./models"

def main(folder,img) :
    # change this as you see fit
    print folder
    print img
    image_path = "{}/{}".format(IMAGES_PATH, img)

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Loads label file, strips off carriage return
    labelFile = "{}/{}/retrained_labels.txt".format(MODELS_PATH, folder)
    print ("The label file is {}".format(labelFile))
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile(labelFile)]

    # Unpersists graph from file
    graphFile = "{}/{}/retrained_graph.pb".format(MODELS_PATH, folder)
    print ("The graph file is {}".format(graphFile))
    with tf.gfile.FastGFile(graphFile, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        sess.close()
        # Sort to show labels of first prediction in order of confidence
        top_k2 = predictions[0].argsort()[-len(predictions[0]):][::-1]
        print top_k2
        results = list()
        print(label_lines)
        for node_id in top_k2:
            try:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                results.append({"score":str(float("{0:.2f}".format(score*100))) , "disease" : human_string})
                # print('%s (score = %.5f)' % (human_string, score))
            except:
                human_string = ""
        results_sorted = sorted(results, key=lambda x: float(x["score"]))[::-1]
        print (results_sorted)
        crop_name = results_sorted[0]["disease"]
        # print results_sorted
        return results_sorted
    tf.reset_default_graph()
