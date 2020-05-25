import cv2
import numpy as np
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


    is_track = False
    is_forward = False
    alpha = 2

    while True:

        ret, frame = cap.read()
        if not ret: continue

        frame_g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        if k == ord('t'):
            is_track = True
            points_pre = cv2.goodFeaturesToTrack(frame_g,
                                                 maxCorners = 60,
                                                 qualityLevel = 0.01,
                                                 minDistance = 5,
                                                 blockSize = 10 )
            points_pre = np.squeeze(points_pre)

        if k == ord('s'):
            is_track = False

        if k == ord('f'):
            is_forward = not is_forward


        if is_track:

            points_now, found, _ = cv2.calcOpticalFlowPyrLK(frame_g_pre, frame_g, points_pre, None, 
                                                            winSize  = (20, 20),
                                                            maxLevel = 4,
                                                            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.01)
                                                            )
            points_pre = np.squeeze(points_pre)
            found = np.squeeze(found)

            if (found == None).all():
                is_track = False
                continue
            
            points_now = points_now[found == 1]
            points_pre = points_pre[found == 1]

            for s, e in zip(points_now, points_pre):
                cv2.circle(frame, tuple(s), 3, (0, 0, 255), -1)
                if is_forward:                
                    cv2.line(frame, tuple(s), tuple(s + alpha * (s - e)), (255, 0, 0), 2)
                else:
                    cv2.line(frame, tuple(s), tuple(e), (255, 255, 255), 2)

            points_pre = points_now


        cv2.imshow('frame', frame)
        frame_g_pre = frame_g


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()





