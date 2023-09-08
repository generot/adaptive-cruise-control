#!/usr/bin/python

import cv2
import numpy as np

FPS = 30

video = cv2.VideoCapture("../samples/sample_florida1.mp4")
classifier = cv2.CascadeClassifier("../models/cars.xml")

kernel = np.ones((3, 3), np.uint8)
closing_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

avg_bbox = np.zeros(4)

no_matches_threshold = 20
no_matches_cnt = 0

while video.isOpened():
    retcode, frame = video.read()

    if retcode != True:
        print("An error occured.")

    augmented = frame[200:600, 300:600]

    gray = cv2.cvtColor(augmented, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    dilated = cv2.dilate(blurred, kernel)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, closing_kernel)
   
    result = classifier.detectMultiScale(augmented, 1.0006, 3, 0, (150,150))

    if len(result) == 0:
        no_matches_cnt += 1

    if no_matches_cnt > no_matches_threshold:
        avg_bbox = np.zeros(4, dtype=np.uint8)
        no_matches_cnt = 0

    for rect in result:
        x, y, width, height = rect

        y_frame = y + 200
        x_frame = x + 300

        rect_arrlike = np.array([x_frame, y_frame, width, height])

        if np.array_equal(avg_bbox, np.zeros(4)):
            avg_bbox = np.array(rect_arrlike)
        else:
            avg_bbox = (avg_bbox + rect_arrlike) // 2

        # 10% Tolerance
        x += x // 10
        y += y // 10

        #cv2.rectangle(augmented, (x, y), (x + width, y + height), (0, 255, 0))
        #cv2.rectangle(frame, (x_frame, y_frame), (x_frame + width, y_frame + height), (0, 255, 0))

    cv2.rectangle(frame, (avg_bbox[0], avg_bbox[1]), (avg_bbox[0] + avg_bbox[2], avg_bbox[1] + avg_bbox[3]), (0, 255, 0))
    cv2.imshow("Sample Video", frame)

    if cv2.waitKey(int(1000 / FPS)) == ord('e'):
        break

video.release()
cv2.destroyAllWindows()

def main():
    pass

if __name__ == "__main__":
    main()