import cv2, os, urllib.request

import math
import numpy as np
import tensorflow as tf

from tensorflow import keras
from os.path import dirname, join
 

def draw_faces(img, faces):
    for x, y, x1, y1 in faces:
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 3)


def get_landmark_model(saved_model= join(dirname(__file__), 'pose_model')):
    model = keras.models.load_model(saved_model)
    return model


def get_square_box(box):
    left_x = box[0]
    top_y = box[1]
    right_x = box[2]
    bottom_y = box[3]

    box_width = right_x - left_x
    box_height = bottom_y - top_y

    # Check if box is already a square. If not, make it a square.
    diff = box_height - box_width
    delta = int(abs(diff) / 2)

    if diff == 0:  # Already a square.
        return box
    elif diff > 0:  # Height > width, a slim box.
        left_x -= delta
        right_x += delta
        if diff % 2 == 1:
            right_x += 1
    else:  # Width > height, a short box.
        top_y -= delta
        bottom_y += delta
        if diff % 2 == 1:
            bottom_y += 1

    # Make sure box is always square.
    assert ((right_x - left_x) == (bottom_y - top_y)), 'Box is not square.'

    return [left_x, top_y, right_x, bottom_y]


def move_box(box, offset):
    """Move the box to direction specified by vector offset"""
    left_x = box[0] + offset[0]
    top_y = box[1] + offset[1]
    right_x = box[2] + offset[0]
    bottom_y = box[3] + offset[1]
    return [left_x, top_y, right_x, bottom_y]


def detect_marks(img, model, face):
    offset_y = int(abs((face[3] - face[1]) * 0.1))
    box_moved = move_box(face, [0, offset_y])
    facebox = get_square_box(box_moved)

    h, w = img.shape[:2]
    if facebox[0] < 0:
        facebox[0] = 0
    if facebox[1] < 0:
        facebox[1] = 0
    if facebox[2] > w:
        facebox[2] = w
    if facebox[3] > h:
        facebox[3] = h

    face_img = img[facebox[1]: facebox[3],
               facebox[0]: facebox[2]]


    face_img = cv2.resize(face_img, (128, 128))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    # # Actual detection.
    predictions = model.signatures["predict"](
        tf.constant([face_img], dtype=tf.uint8))

    # Convert predictions to landmarks.
    marks = np.array(predictions['output']).flatten()[:136]
    marks = np.reshape(marks, (-1, 2))

    marks *= (facebox[2] - facebox[0])
    marks[:, 0] += facebox[0]
    marks[:, 1] += facebox[1]
    marks = marks.astype(np.uint)

    return marks


def draw_marks(image, marks, color=(0, 255, 0)):
    for mark in marks:
        cv2.circle(image, (mark[0], mark[1]), 2, color, -1, cv2.LINE_AA)


def get_face_detector(modelFile=None,
                      configFile=None,
                      quantized=False):
    if quantized:
        if modelFile == None:
            modelFile = "static/opencv_face_detector_uint8.pb"
        if configFile == None:
            configFile = "static/opencv_face_detector.pbtxt"
        model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    else:
        if modelFile == None:
            modelFile = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel") #join(dirname(__file__), )
        # = "res10_300x300_ssd_iter_140000.caffemodel"
        if configFile == None:
            configFile =join(dirname(__file__), "deploy.prototxt")    #join(dirname(__file__),)
        model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    return model


def find_faces(img, model):
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    res = model.forward()
    faces = []
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])
    return faces


# from face_detector import get_face_detector, find_faces
# from face_landmarks import get_landmark_model, detect_marks, draw_marks

face_model = get_face_detector()
landmark_model = get_landmark_model()
outer_points = [[49, 59], [50, 58], [51, 57], [52, 56], [53, 55]]
d_outer = [0] * 5
inner_points = [[61, 67], [62, 66], [63, 65]]
d_inner = [0] * 3
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)

ret, img = cap.read()
#print(ret,"################################################")
size = img.shape
#print(size,"##############################################")
# 3D model points.
model_points = np.array([
    (0.0, 0.0, 0.0),  # Nose tip
    (0.0, -330.0, -65.0),  # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),  # Right eye right corne
    (-150.0, -150.0, -125.0),  # Left Mouth corner
    (150.0, -150.0, -125.0)  # Right mouth corner
])

# Camera internals
focal_length = size[1]
center = (size[1] / 2, size[0] / 2)
camera_matrix = np.array(
    [[focal_length, 0, center[0]],
     [0, focal_length, center[1]],
     [0, 0, 1]], dtype="double"
)

cap.release()


#######################head pose################
def get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val):
    """Return the 3D points present as 2D for making annotation box"""
    point_3d = []
    dist_coeffs = np.zeros((4, 1))
    rear_size = val[0]
    rear_depth = val[1]
    point_3d.append((-rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, -rear_size, rear_depth))

    front_size = val[2]
    front_depth = val[3]
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d.append((-front_size, front_size, front_depth))
    point_3d.append((front_size, front_size, front_depth))
    point_3d.append((front_size, -front_size, front_depth))
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d = np.array(point_3d, dtype=np.float).reshape(-1, 3)

    # Map to 2d img points
    (point_2d, _) = cv2.projectPoints(point_3d,
                                      rotation_vector,
                                      translation_vector,
                                      camera_matrix,
                                      dist_coeffs)
    point_2d = np.int32(point_2d.reshape(-1, 2))
    return point_2d


def draw_annotation_box(img, rotation_vector, translation_vector, camera_matrix,
                        rear_size=300, rear_depth=0, front_size=500, front_depth=400,
                        color=(255, 255, 0), line_width=2):
    rear_size = 1
    rear_depth = 0
    front_size = img.shape[1]
    front_depth = front_size * 2
    val = [rear_size, rear_depth, front_size, front_depth]
    point_2d = get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val)
    # # Draw all the lines
    cv2.polylines(img, [point_2d], True, color, line_width, cv2.LINE_AA)
    cv2.line(img, tuple(point_2d[1]), tuple(
        point_2d[6]), color, line_width, cv2.LINE_AA)
    cv2.line(img, tuple(point_2d[2]), tuple(
        point_2d[7]), color, line_width, cv2.LINE_AA)
    cv2.line(img, tuple(point_2d[3]), tuple(
        point_2d[8]), color, line_width, cv2.LINE_AA)


def head_pose_points(img, rotation_vector, translation_vector, camera_matrix):
    rear_size = 1
    rear_depth = 0
    front_size = img.shape[1]
    front_depth = front_size * 2
    val = [rear_size, rear_depth, front_size, front_depth]
    point_2d = get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val)
    y = (point_2d[5] + point_2d[8]) // 2
    x = point_2d[2]

    return (x, y)


#ret, img = cap.read()
#print(ret,"11111111")
"""
rects = find_faces(img, face_model)
shape = detect_marks(img, landmark_model, rects[0])
for i in range(100):
    for i, (p1, p2) in enumerate(outer_points):
        d_outer[i] += shape[p2][1] - shape[p1][1]
    for i, (p1, p2) in enumerate(inner_points):
        d_inner[i] += shape[p2][1] - shape[p1][1]

d_outer[:] = [x / 100 for x in d_outer]
d_inner[:] = [x / 100 for x in d_inner]
"""
#
hu = 0
hd = 0
hl = 0
hr = 0
M= 0
O=0
#array
hul = []
hdl = []
hll = []
hrl = []
Ml = []
out=[]
toll = 100
cmt=0

#cap.release()

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        print("videocap started")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global hu
        global toll
        global hd
        global hl
        global hr
        global M
        global hul
        global hdl
        global hll
        global hrl
        global Ml
        global out
        global O
        global cmt
        """"
		success, image = self.video.read()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image, 1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		"""
        ret, img = self.video.read()
        ############################################

        rects = find_faces(img, face_model)
        if rects!=[] and cmt == 0:
            cmt=1

            while True:
                try:
                    shape = detect_marks(img, landmark_model, rects[0])
                except:
                    continue
                break

            for i in range(100):
                for i, (p1, p2) in enumerate(outer_points):
                    d_outer[i] += shape[p2][1] - shape[p1][1]
                for i, (p1, p2) in enumerate(inner_points):
                    d_inner[i] += shape[p2][1] - shape[p1][1]

            d_outer[:] = [x / 100 for x in d_outer]
            d_inner[:] = [x / 100 for x in d_inner]
        elif rects==[] and cmt==0:
            cv2.putText(img, 'face not found', (30, 30), font,
                        1, (0, 255, 255), 2)

        #############################

        if ret == True:
            faces = find_faces(img, face_model)
            if len(faces)==0:
                cv2.putText(img, "Please return to test", (30, 30), font,
                        1, (0, 255, 255), 2)
                O = O + 1
                if O >= 10:
                    toll = toll - 1
                    O=0
                    out.append("1")

            for face in faces:

                while True:
                    try:
                        marks = detect_marks(img, landmark_model, face)
                    except:
                        continue
                    break

                #######################

                shape = marks
                cnt_outer = 0
                cnt_inner = 0
                draw_marks(img, shape[48:])
                for i, (p1, p2) in enumerate(outer_points):
                    if d_outer[i] + 3 < shape[p2][1] - shape[p1][1]:
                        cnt_outer += 1
                for i, (p1, p2) in enumerate(inner_points):
                    if d_inner[i] + 2 < shape[p2][1] - shape[p1][1]:
                        cnt_inner += 1
                if cnt_outer > 3 and cnt_inner > 2:
                    M = M + 1
                    if M >= 8:
                        toll = toll - 1
                        M = 0
                        Ml.append("MOUTH OPEN")

                    # print(toll)

                    cv2.putText(img, 'Mouth open', (30, 30), font,
                                1, (0, 255, 255), 2)

                ###################################
                # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
                image_points = np.array([
                    marks[30],  # Nose tip
                    marks[8],  # Chin
                    marks[36],  # Left eye left corner
                    marks[45],  # Right eye right corne
                    marks[48],  # Left Mouth corner
                    marks[54]  # Right mouth corner
                ], dtype="double")
                dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
                (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                              dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

                # Project a 3D point (0, 0, 1000.0) onto the image plane.
                # We use this to draw a line sticking out of the nose

                (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                                 translation_vector, camera_matrix, dist_coeffs)

                for p in image_points:
                    cv2.circle(img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

                p1 = (int(image_points[0][0]), int(image_points[0][1]))
                p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
                x1, x2 = head_pose_points(img, rotation_vector, translation_vector, camera_matrix)

                cv2.line(img, p1, p2, (0, 255, 255), 2)
                cv2.line(img, tuple(x1), tuple(x2), (255, 255, 0), 2)
                # for (x, y) in marks:
                #     cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
                # cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
                try:
                    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
                    ang1 = int(math.degrees(math.atan(m)))
                except:
                    ang1 = 90

                try:
                    m = (x2[1] - x1[1]) / (x2[0] - x1[0])
                    ang2 = int(math.degrees(math.atan(-1 / m)))
                except:
                    ang2 = 90

                # print('div by zero error')
                if ang1 >= 40:

                    hd = hd + 1
                    if hd >= 5:
                        toll = toll - 1
                        hd = 0
                        hdl.append("Head down")

                    # print(toll)

                    cv2.putText(img, 'Head down', (30, 30), font, 2, (255, 255, 128), 3)

                elif ang1 <= -35:

                    hu = hu + 1
                    if hu >= 5:
                        toll = toll - 1
                        hu = 0
                        hul.append("Head Up")

                    # print(toll)

                    cv2.putText(img, 'Head up', (30, 30), font, 2, (255, 255, 128), 3)

                if ang2 >= 40:
                    hr = hr + 1
                    if hr >= 5:
                        toll = toll - 1
                        hr = 0
                        hrl.append("Head Right")
                    cv2.putText(img, 'Head right', (90, 30), font, 2, (255, 255, 128), 3)
                elif ang2 <= -40:
                    hl = hl + 1
                    if hl >= 5:
                        toll = toll - 1
                        hl = 0
                        hll.append("Head left")
                    cv2.putText(img, 'Head left', (90, 30), font, 2, (255, 255, 128), 3)
                cv2.putText(img, str(ang1), tuple(p1), font, 2, (128, 255, 255), 3)
                cv2.putText(img, str(ang2), tuple(x1), font, 2, (255, 255, 128), 3)
            ret, jpeg = cv2.imencode('.jpg', img)
            a=str(len(Ml))+" "+str(len(hul))+" "+str(len(hdl))+" "+str(len(hll))+" "+str(len(hrl))+" "+str(len(out))+" "+str(toll)
            return jpeg.tobytes(),a
