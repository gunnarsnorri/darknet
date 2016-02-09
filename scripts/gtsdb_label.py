#!/usr/bin/env python
import sys
from os import getcwd
import os.path
import shutil
from helper_functions import convert_txt, get_image_set

if __name__ == "__main__":
    if len(sys.argv) > 1:
        img_db_dir = os.path.abspath(sys.argv[1])
        if not os.path.exists(img_db_dir):
            print("Directory %s does not exist!" % img_db_dir)
            sys.exit(1)
    else:
        print("usage: python %s img_db_dir" % sys.argv[0])
        sys.exit(1)

    sets = [('train', 720), ('val', 810), ('test', 900)]

    # classes = [("0" + str(i))[-2:] for i in range(43)]

    """the generated text files has to be in format
    <object-class> <x> <y> <width> <height>
    where x,y,width,height is in percentages
    """

    wd = getcwd()
    labels_dir = '%s/FullIJCNN2013/labels' % img_db_dir
    if os.path.exists(labels_dir):
        shutil.rmtree(labels_dir)
    os.makedirs(labels_dir)
    for sub_dir, _ in sets:
        sub_txt_path = '%s/FullIJCNN2013/%s/%s_gt.txt' % (
            img_db_dir, sub_dir, sub_dir)
        if os.path.exists(sub_txt_path):
            os.remove(sub_txt_path)

    with open('%s/FullIJCNN2013/gt.txt' % img_db_dir) as read_f:
        for line in read_f:
            line = line.strip("\n")
            gt_row = line.split(";")
            for i in range(1, 5):
                gt_row[i] = int(gt_row[i])
            convert_txt(img_db_dir, gt_row)
            image_set = get_image_set(sets, int(gt_row[0].split(".")[0]))
            with open('%s/FullIJCNN2013/%s/%s_gt.txt' % (img_db_dir, image_set, image_set), 'a') as subset_gt:
                subset_gt.write(
                    '%s/FullIJCNN2013/%s\n' %
                    (img_db_dir, gt_row[0]))
