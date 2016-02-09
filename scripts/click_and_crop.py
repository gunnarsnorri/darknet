#!/usr/bin/env python
# import the necessary packages
import os
import csv
import argparse
import cv2

from helper_functions import convert

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPts = []
refStart = (-1, -1)
cropping = False


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPts, refStart, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refStart = (x, y)
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPts.append((refStart, (x, y)))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(
            image, refPts[-1][0], refPts[-1][1], (0, 255, 0), 2)
        cv2.imshow("image", image)


def get_images(source_dir):
    filetypes = ["ppm", "jpg", "jpeg", "png", "bmp"]
    return [filename for filename in os.listdir(source_dir) if
            filename.split(".")[-1] in filetypes]

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--indir", required=True,
                    help="Path to the source directory")
    args = vars(ap.parse_args())

    # load the image, clone it, and setup the mouse callback function
    images = get_images(args["indir"])
    gt_filename = os.path.join(args["indir"], "gt.txt")
    with open(gt_filename, 'w') as gt_file:
        gt_writer = csv.writer(gt_file, delimiter=";")
        for image_filename in images:
            image_fullname = os.path.join(args["indir"], image_filename)
            image = cv2.imread(image_fullname)
            clone = image.copy()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", click_and_crop)

            # keep looping until the 'c' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    image = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif key == ord(" "):
                    break

            # if there are two reference points, then crop the region of interest
            # from the image and display it
            gt_info = []
            for refPt in refPts:
                if len(refPt) == 2:
                    x1 = min(refPt[0][0], refPt[1][0])
                    x2 = max(refPt[0][0], refPt[1][0])
                    y1 = min(refPt[0][1], refPt[1][1])
                    y2 = max(refPt[0][1], refPt[1][1])
                    gt_info.append((image_filename, x1, y1, x2, y2, "category"))
            gt_writer.writerows(gt_info)

            # close all open windows
            refPts = []
            cv2.destroyAllWindows()
