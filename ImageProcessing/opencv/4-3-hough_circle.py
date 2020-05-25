import numpy as np
import cv2
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
# from skimage.draw import circle_perimeter
import sys




def main():

    if len(sys.argv) == 1: # pass the device number
        cap = cv2.VideoCapture(0)
    else:
        try:
            cap = cv2.VideoCapture(int(sys.argv[1]))
        except:
            cap = cv2.VideoCapture(sys.argv[1])

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        # frame = cv2.flip(frame, 1)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        hough_radii = np.arange(50, 100, 10)
        hough_res = hough_circle(edges, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                                   total_num_peaks=6)
        for center_y, center_x, radius in zip(cy, cx, radii):
            cv2.circle(frame, (center_x, center_y), radius, (255, 0, 0), 2)
        
        
        cv2.imshow('frame', frame)
        cv2.imshow('edges', edges)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()