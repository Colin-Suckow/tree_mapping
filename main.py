import cv2
from light import *
import time
from detector import *
import math
from patterns import *
import json
import os.path


def main(capture=False):
    #capture_points("left_side")
    if os.path.isfile('light_pos.json'):
        print("Loading light positions from disk...")
        with open('light_pos.json', 'r') as f:
            points = json.load(f)
        print("Done!")
    else:
        print("No light data found. Calculating...")
        points = combine_points(calculate_points("front"), calculate_points("right_side"), calculate_points("back_side"), calculate_points("left_side"))
        print("Done! Saving calculated data...")
        with open('light_pos.json', 'w') as f:
            json.dump(points, f)
        print("Done!")
    t = 0

    print("Starting animation!")
    while True:
        send_pattern(vertical_rg_rot(points, t))
        t += 0.01
        time.sleep(0.016)



        
if __name__ == "__main__":
    main()