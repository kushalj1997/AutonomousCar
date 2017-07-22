"""@author Kushal Jaligama"""

import os

import cv2

import numpy as np


def canny(img, low_threshold, high_threshold):
    """
    Applies the Canny transform to the input image, allowing for edges to be
    detected.
    """
    return cv2.Canny(img, low_threshold, high_threshold)


def grayscale(img):
    """
    Applies the Grayscale transform to the input image. This means that the
    output image will be a black and white image, with only one channel for
    colors as opposed to 3.
    NOTE: to see the returned image as grayscale, call:
    plt.imshow(gray, cmap='gray')
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def roi(img):
    """
    Removes all items in the image that are outside of the target region
    described by vertices.
    """
    vertices = np.array([[460, 320], [130, 540], [870, 540], [520, 320]])
    # Create a blank image that has the same shape as the original image
    blank = np.zeros_like(img)
    # Fill the mask with black over the area we want to maintain
    cv2.fillPoly(blank, [vertices], 255)
    # Bitwise AND the original image and the mask we created to get only the
    # part of the image that contains the lane
    return cv2.bitwise_and(img, blank)


def drawLine(img, line, color):
    if color is "blue":
        for x1, y1, x2, y2 in line:
            # print(type(x1))
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0),
                     5)
    elif color is "red":
        for x1, y1, x2, y2 in line:
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255),
                     5)


def houghLines(img, orig_image):
    """
    Uses the edge image and detects the lines of the lane using the Hough Trans.
    """

    lines = cv2.HoughLinesP(img, 100, 0.785, 50)
    # line_img = np.zeros((*img.shape, 3), dtype=np.uint8)
    print(img.shape)
    (left_line, right_line) = getConnectedHoughLines(img, lines)
    # print("Connected: " + str(type(leftSideLine)))
    for line in lines:
        # print("Hough: " + str(line))
        drawLine(orig_image, line, "blue")
    drawLine(orig_image, left_line, "red")
    drawLine(orig_image, right_line, "red")
    return orig_image


def getLineFromPoint(img, point, slope):
    # Get second point
    y2 = point[0]
    y1 = img.shape[0]
    x2 = point[1]
    x1 = -1 * ((y2 - y1) / slope + x2)

    return [[int(x1), int(y1), int(x2), int(y2)]]


def getConnectedHoughLines(img, lines):
    """
    This looks for the most extreme pixels in an image, calculates the slope of
    all of the Hough Lines and creates a line going down to the bottom of the
    screen to show two single lines for each painted line of the lane.
    """
    right_line = [[img.shape[0], 0, 0, 0]]
    left_line = [[img.shape[0], 0, 0, 0]]

    left_max_y = right_max_y = 0
    left_min_y = right_min_y = img.shape[0]

    print(type(lines))
    # Find out the most extreme pixels for both the left and right side
    for line in lines:
        for x1, y1, x2, y2 in line:
            x1f = float(x1)
            x2f = float(x2)
            y1f = float(y1)
            y2f = float(y2)
            if x1f != x2f:
                # Only lines that are not NAN
                if ((y2f - y1f) / (x2f - x1f)) < 0:
                    # Left Sided line
                    if y1 > left_max_y:
                        left_max_y = y1
                        left_line[0][0] = x1
                        left_line[0][1] = y1
                    if y2 > left_max_y:
                        left_max_y = y2
                        left_line[0][0] = x2
                        left_line[0][1] = y2
                    if y1 < left_min_y:
                        left_min_y = y1
                        left_line[0][2] = x1
                        left_line[0][3] = y1
                    if y2 < left_min_y:
                        left_min_y = y2
                        left_line[0][2] = x2
                        left_line[0][3] = y2

                elif ((y2f - y1f) / (x2f - x1f)) > 0:
                    # Right Sided line
                    if y1 > right_max_y:
                        right_max_y = y1
                        right_line[0][0] = x1
                        right_line[0][1] = y1
                    if y2 > right_max_y:
                        right_max_y = y2
                        right_line[0][0] = x2
                        right_line[0][1] = y2
                    if y1 < right_min_y:
                        right_min_y = y1
                        right_line[0][2] = x1
                        right_line[0][3] = y1
                    if y2 < right_min_y:
                        right_min_y = y2
                        right_line[0][2] = x2
                        right_line[0][3] = y2

    print("Left: {}, Right: {}".format(left_line, right_line))
    return (left_line, right_line)


def main():
    """
    Read in the image.
    Convert it to Grayscale.
    Generate the edge image using Canny.
    Apply the Hough Transform to detect lines.
    Display the result.
    """
    lane_image = cv2.imread(os.getcwd() + "/lane.jpeg")
    lane_gray = grayscale(lane_image)
    cv2.imshow("Lane Grayscale:", lane_gray)
    lane_edges = canny(lane_gray, 100, 255)
    cv2.imshow("Lane Edges ROI", roi(lane_edges))
    lane_hough = houghLines(roi(lane_edges), lane_image)
    cv2.imshow("Hough Lines", lane_hough)
    # Show the image for 10 seconds
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
