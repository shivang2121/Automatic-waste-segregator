#!/usr/bin/env python
import os
import threading
import cv2
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int16
import time
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
count = 0

class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()

    def run(self):
        while not rospy.is_shutdown():
            ret, self.last_frame = self.camera.read()


DATA_DIR = os.path.join(os.getcwd(), 'data0')
MODELS_DIR = os.path.join(DATA_DIR, 'models0')
MODEL_NAME = 'rcnn_model'
PATH_TO_CKPT = os.path.join(MODELS_DIR, os.path.join(MODEL_NAME, 'checkpoint/'))
PATH_TO_CFG = os.path.join(MODELS_DIR, os.path.join(MODEL_NAME, 'pipeline.config'))
LABEL_FILENAME = 'labelmap.pbtxt'
PATH_TO_LABELS = os.path.join(MODELS_DIR, os.path.join(MODEL_NAME, LABEL_FILENAME))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging

tf.get_logger().setLevel('ERROR')
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
model_config = configs['model']
detection_model = model_builder.build(model_config=model_config, is_training=False)
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(PATH_TO_CKPT, 'ckpt-0')).expect_partial()
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

@tf.function
def detect_fn(image):
    """Detect objects in image."""

    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])



camera = cv2.VideoCapture(0)
cam_cleaner = CameraBufferCleanerThread(camera)
def callback(data):
    distance=data.data
    global count
    print("c5")
    if distance != 0:
        
            
        print("in")
        if cam_cleaner.last_frame is not None:
            image_np = cam_cleaner.last_frame
        else:
            ret, image_np = camera.read()
    
    
        start = time.time()
    
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
    

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        print("tensor")
        detections, predictions_dict, shapes = detect_fn(input_tensor)
    
    

        label_id_offset = 1
        image_np_with_detections = image_np.copy()
    

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'][0].numpy(),
            (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
            detections['detection_scores'][0].numpy(),
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.80,
            agnostic_mode=False)
    

    # Display output
        end = time.time()
        print(end-start)
        name = 'frame' + str(count) +'.jpg'
        cv2.imwrite(name,cv2.resize(image_np_with_detections, (800, 600)))
        count += 1
        pub = rospy.Publisher('rec', Int16, queue_size=10)
        pub.publish(1)
        print("saved")
        
        
            

        
            
        
  

def peak():
   
    rospy.init_node('oc', anonymous=True)

    rospy.Subscriber("oc", Int16, callback)
    
    print("check")

    rospy.spin()

if __name__ == '__main__':
    try:
        peak()
    except rospy.ROSInterruptException:
        cap.release()
        
        pass

