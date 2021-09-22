import threading
import cv2
import os

# Define the thread that will continuously pull frames from the camera
class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()

# Start the camera
camera = cv2.VideoCapture(0)
camera.set(3,800)
camera.set(4,600)
# Start the cleaning thread
cam_cleaner = CameraBufferCleanerThread(camera)
count = 0

# Use the frame whenever you want
while True:
    if cam_cleaner.last_frame is not None:
        cv2.imshow('The last frame', cam_cleaner.last_frame)
    
    if cv2.waitKey(30) == ord('s'):
        if cam_cleaner.last_frame is not None:
            image_np = cam_cleaner.last_frame
        else:
            ret, image_np = camera.read()
        
        name = 'measure' + str(count) +'.jpg'
        path = '/home/tan/objectTrackingpic/measure/'
        cv2.imwrite(os.path.join(path,name),image_np)
        count += 1
        print('save')

    if cv2.waitKey(25) == ord('a'):
        break


cv2.destroyAllWindows()
camera.release()

