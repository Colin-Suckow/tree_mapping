# Standard imports
import cv2
import numpy as np;
from light import *
import time

def detect_light(path):

    # Read image
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    inv_im = cv2.bitwise_not(im)
    
    # Set up the detector with default parameters.
    params = cv2.SimpleBlobDetector_Params()
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Detect blobs.
    keypoints = detector.detect(inv_im)
    if len(keypoints) > 0:
        return (keypoints[0].pt[0], keypoints[0].pt[1])
    else:
        return None

def capture_points(side):
    print("Place camera to capture {} images".format(side))
    input("Press any key when ready")
    for i in range(150):
            frame = capture_led_image(i)
            cv2.imwrite("{}_images/{}.jpg".format(side, str(i)), frame)


def calculate_points(side):
    points = []
    for i in range(150):
        points.append(detect_light("{}_images/{}.jpg".format(side, str(i))))
    return normalized_points(points)

def combine_points(front_points, right_points, back_points, left_points):
    result_points = []
    unknown_lights = 0
    single_view_lights = 0

    for i in range(150):
        fp = front_points[i]
        rp = right_points[i]
        bp = back_points[i]
        lp = left_points[i]

        # At least 2 angles known
        if fp is not None and rp is not None:
            # We found the point in both angles, cool! Calculate a full 3D point
            rx = fp[0]
            ry = (fp[1] + rp[1]) / 2
            rz = rp[0]
            result_points.append((rx, ry, rz))
        elif rp is not None and bp is not None:
            rz = rp[0]
            rx = (1 - bp[0])
            ry = (rp[1] + bp[1]) / 2
            result_points.append((rx, ry, rz))
        elif bp is not None and lp is not None:
            rz = 1 - lp[0]
            rx = 1 - bp[0]
            ry = (lp[1] + bp[1]) / 2
            result_points.append((rx, ry, rz))
        elif lp is not None and fp is not None:
            rz = 1 - lp[0]
            rx = fp[0]
            ry = (lp[1] + fp[1]) / 2
            result_points.append((rx, ry, rz))

        # One angle known
        elif fp is not None:
            single_view_lights += 1
            result_points.append("known_f")
        elif rp is not None:
            single_view_lights += 1
            result_points.append("known_r")
        elif bp is not None:
            single_view_lights += 1
            result_points.append("known_b")
        elif lp is not None:
            single_view_lights += 1
            result_points.append("known_l")

        # No angles known
        else:
            # Default case, if we get here then there is no way to find the point, so return None
            unknown_lights += 1
            result_points.append(None)


    # Now that we have found some definite points, go back and try to make a good estimate of where the single view points are
    for i in range(150):
        fp = front_points[i]
        rp = right_points[i]
        bp = back_points[i]
        lp = left_points[i]

        if result_points[i] == "known_f":
            rx = fp[0]
            ry = fp[1]
            # Use the Z of the closest light on the strand
            rz = find_closest_strand(result_points, i)[2]
            result_points[i] = (rx, ry, rz)

        if result_points[i] == "known_r":
            rz = rp[0]
            ry = rp[1]
            # Use the X of the closest light on the strand
            rx = find_closest_strand(result_points, i)[0]
            result_points[i] = (rx, ry, rz)

        if result_points[i] == "known_b":
            rx = 1 - bp[0]
            ry = bp[1]
            # Use the Z of the closest light on the strand
            rz = find_closest_strand(result_points, i)[2]
            result_points[i] = (rx, ry, rz)

        if result_points[i] == "known_l":
            rz = 1 - lp[0]
            ry = lp[1]
            # Use the X of the closest light on the strand
            rx = find_closest_strand(result_points, i)[0]
            result_points[i] = (rx, ry, rz)

    print("Done combining lights. Estimated {} positions for single view lights. Could not find positions for {} lights.".format(single_view_lights, unknown_lights))
    return result_points

def find_closest_strand(calculated_points, i):
    dist = 0
    while True:
        pos_light = calculated_points[i + dist]
        neg_light = calculated_points[i - dist]
        if pos_light is not None and not isinstance(pos_light, str):
            return pos_light
        if neg_light is not None and not isinstance(neg_light, str):
            return neg_light

        dist += 1
        if i + dist >= 150 or i - dist < 0:
            return None

def capture_led_image(light):
    show_single_light(light)
    cam = cv2.VideoCapture(0)
    time.sleep(3)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        print("Failed to grab frame")
    return frame

def normalized_points(points):
    maxX = 0
    maxY = 0
    minX = 10000000000
    minY = 10000000000

    for p in points:
        if p is not None:
            if p[0] > maxX:
                maxX = p[0]
            if p[1] > maxY:
                maxY = p[1]
            if p[0] < minX:
                minX = p[0]
            if p[1] < minY:
                minY = p[1]

    maxX -= minX
    maxY -= minY

    norm_points = []
    for p in points:
        if p is not None:
            normX = (p[0] - minX) / maxX
            normY = (p[1] - minY) / maxY
            norm_points.append((normX, normY))
        else:
            norm_points.append(None)
    return norm_points