# Kushal Jaligama
import cv2
import numpy as np
import os

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

def houghLines(img, orig_image):
    """
    Uses the edge image and detects the lines of the lane using the Hough Trans.
    """

    lines = cv2.HoughLinesP(img, 100, 0.785, 50)
    # line_img = np.zeros((*img.shape, 3), dtype=np.uint8)
    print(img.shape)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(orig_image, (x1, y1), (x2, y2), [255, 255, 0], 5)
    return orig_image

def main():
    laneImage = cv2.imread(os.getcwd() + "/lane.jpeg")
    laneGray = grayscale(laneImage)
    laneEdges = canny(laneGray, 100, 255)
    cv2.imshow("Lane Edges ROI", roi(laneEdges))
    laneHough = houghLines(roi(laneEdges), laneImage)
    cv2.imshow("Hough Lines", laneHough)
    # Show the image for 10 seconds
    cv2.waitKey(10000)

if __name__ == '__main__':
    main()