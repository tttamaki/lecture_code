import cv2
import numpy as np
import sys

def myfunc(i):
    pass # do nothing now

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


    cv2.namedWindow('frame') # create win with win name
    cv2.createTrackbar('th1', # name of value
                       'frame', # win name
                       100, # value
                       255, # count
                       myfunc) # callback func
    cv2.createTrackbar('th2', 'frame', 200, 255, myfunc)
    cv2.createTrackbar('th', 'frame', 10, 50, myfunc)


    hough = '1'
    print('keys: 1 (detecting lines), 2 (detecting line segments)')

    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        # frame = cv2.flip(frame, 1)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        if k == ord('1'):
            hough = '1'
        if k == ord('2'):
            hough = '2'

        th1 = cv2.getTrackbarPos('th1', 'frame')
        th2 = cv2.getTrackbarPos('th2', 'frame')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, th1, th2, apertureSize=3)

        if hough == '1':
            ## Opencv hough
            th = cv2.getTrackbarPos('th', 'frame')
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=th*10)
            if lines is not None:
                for l in lines:
                    for rho, theta in l:
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + frame.shape[1]*(-b))
                        y1 = int(y0 + frame.shape[1]*(a))
                        x2 = int(x0 - frame.shape[1]*(-b))
                        y2 = int(y0 - frame.shape[1]*(a))
                        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

        if hough == '2':
            # Opencv Prob Hough
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=15, maxLineGap=3)
            if lines is not None:
              for l in lines:
                  for x1, y1, x2, y2 in l:
                      cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)



        cv2.imshow('frame', frame)
        cv2.imshow('edges', edges)


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()