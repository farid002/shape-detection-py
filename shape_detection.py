import cv2
import math
import numpy as np


class Rect:

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def ratio(self):
        return self.width / self.height

    @property
    def max_x(self):
        return self.x + self.width

    @property
    def max_y(self):
        return self.y + self.height


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def angle(pt1, pt2, pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return (dx1 * dx2 + dy1 * dy2) / math.sqrt((dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2) + 1e-10)


def setLabel(im, label, contour):
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    thickness = 1
    # baseline = 0

    text = cv2.getTextSize(label, fontface, scale, thickness)
    r = Rect()
    r.x, r.y, r.height, r.width = cv2.boundingRect(contour)

    pt = Point(r.x + ((r.width - text.width) / 2), r.y + ((r.height + text.height) / 2))
    cv2.putText(im, label, fontface, scale, (0, 0, 0), thickness, 8)


src = cv2.imread("box.jpg")

blurred = cv2.GaussianBlur(src, (3, 3), 0)

gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

bw = cv2.Canny(gray, 80, 120)

bw, contours, hierarchy = cv2.findContours(bw.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.findContours(bw.clone(), contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE)

dst = src.copy()

for cnt in contours:

    perimeter = cv2.arcLength(cnt, True)
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    vtc = len(approx)

    if abs(cv2.contourArea(cnt)) > 100 and cv2.isContourConvex(approx):

        if len(approx) == 3:
            print("Triangle")
        elif 4 <= len(approx) <= 12:
            cos = []
            for j in range(2, vtc + 1):
                print(approx[2])
                cos.append(angle(approx[j % vtc], approx[j - 2], approx[j - 1]))
            cos.sort()
            # sort(cos.begin(), cos.end())

            mincos = cos[0]
            maxcos = cos[-1]
            rect = cv2.minAreaRect(cnt)
            rect = Rect(width=rect[1][0], height=rect[1][1])
            print(rect)
            print(type(rect))

            if vtc == 4 and mincos >= -0.15 and maxcos <= 0.15 and 0.8 < rect.ratio < 1.2:
                print("SQR")

            elif vtc == 4 and mincos >= -0.15 and maxcos <= 0.15:
                print("RECT")

            elif vtc == 4 and mincos <= -0.2:
                print("TRAPEZOID")

            elif vtc == 5 and mincos >= -0.5 and maxcos <= -0.05:
                print("PENTA")

            elif vtc == 5 and mincos >= -0.85 and maxcos <= 0.6:
                print("SEMI-CIRCLE")

            elif vtc == 5 and mincos >= -1 and maxcos <= 0.6:
                print("QUARTER_CIRCLE")

            elif vtc == 6 and mincos >= -0.7 and maxcos <= -0.3:
                print("HEXA")

            elif vtc == 6 and mincos >= -0.85 and maxcos <= 0.6:
                print("SEMI-CIRCLE")

            elif vtc == 6 and mincos >= -1 and maxcos <= 0.6:
                print("QUARTER-CIRCLE")

            elif vtc == 7:
                print("HEPTA")

            elif vtc == 8:
                area = cv2.contourArea(cnt)
                r = Rect()
                r.x, r.y, r.height, r.width = cv2.boundingRect(cnt)
                radius = r.width / 2

                if abs(1 - (r.width / r.height)) <= 0.2 and abs(1 - (area / (np.pi * math.pow(radius, 2)))) <= 0.2:
                    print("CIR")

                else:
                    print("OCTA")

    elif abs(cv2.contourArea(cnt)) > 100:
        if vtc == 4:
            print("QUAD")
        if vtc == 5:
            print("PENTA")
        if vtc == 6:
            print("HEXA")
        if vtc == 7:
            print("HEPTA")
        if vtc == 10:
            print("STAR")
        elif vtc == 12:
            print("CROSS")
        else:
            print("UNKNOWN")

cv2.namedWindow("src", cv2.WINDOW_FREERATIO)
cv2.namedWindow("dst", cv2.WINDOW_FREERATIO)
cv2.imshow("src", src)
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
