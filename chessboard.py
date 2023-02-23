import numpy as np
import cv2 as cv

with np.load('calibration.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    imgpts0 = tuple(imgpts[0].ravel())
    imgpts1 = tuple(imgpts[1].ravel())
    imgpts2 = tuple(imgpts[2].ravel())
    tuplecorner = (int(corner[0]), int(corner[1]))
    img = cv.line(img, tuplecorner,
                  (int(imgpts0[0]), int(imgpts0[1])), (255, 0, 0), 5)
    img = cv.line(img, tuplecorner,
                  (int(imgpts1[0]), int(imgpts1[1])), (0, 255, 0), 5)
    img = cv.line(img, tuplecorner,
                  (int(imgpts2[0]), int(imgpts2[1])), (0, 0, 255), 5)
    return img


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.1)

objp = np.zeros((6 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()
    # frame = cv.resize(frame, None, fx=0.7, fy=0.7, interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    frame = gray

    ret, corners = cv.findChessboardCorners(frame, (7, 6), None)
    if ret:
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
        imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
        frame = draw(frame, corners2, imgpts)
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
