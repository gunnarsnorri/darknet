import sys
from os import getcwd
import os.path
from PIL import Image
import shutil

if len(sys.argv) > 1:
    img_db_dir = os.path.abspath(sys.argv[1])
    if not os.path.exists(img_db_dir):
        print("Directory %s does not exist!" % img_db_dir)
        sys.exit(1)
else:
    print("usage: python %s img_db_dir" % sys.argv[0])
    sys.exit(1)

sets=[('train', 720), ('val', 810),('test', 900)]

classes = [("0" + str(i))[-2:] for i in range(43)]

"""
the generated text files has to be in <object-class> <x> <y> <width> <height>
where x,y,width,height is in percentages
"""
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def get_image_size(image_number):
    im=Image.open('%s/FullIJCNN2013/%s' %(img_db_dir, image_number))
    return im.size

def convert_txt(gt_row):
    out_file_name=gt_row[0].split(".")[0]+".txt"
    with open('%s/FullIJCNN2013/labels/%s'%(img_db_dir, out_file_name),'a') as f:
        b=gt_row[1:5]
        size=get_image_size(gt_row[0])
        bb=convert(size,b)
        new_description = "%s %s\n" %(str(gt_row[5]), " ".join([str(a) for a in bb]))
        f.write(new_description)

def get_image_set(pic_number):
    for image_set, n in sets:
        if int(pic_number) < n:
	    return(image_set)

wd = getcwd()
labels_dir = '%s/FullIJCNN2013/labels' %img_db_dir
if os.path.exists(labels_dir):
    shutil.rmtree(labels_dir)
os.mkdir(labels_dir)
for sub_dir, _ in sets:
    sub_txt_path='%s/FullIJCNN2013/%s/%s_gt.txt'%(img_db_dir, sub_dir, sub_dir)
    if os.path.exists(sub_txt_path):
        os.remove(sub_txt_path)

with open('%s/FullIJCNN2013/gt.txt' % img_db_dir) as read_f:
    for line in read_f:
        line = line.strip("\n")
        gt_row=line.split(";")
        for i in range (1,5):
            gt_row[i]=int(gt_row[i])
        convert_txt(gt_row)
        image_set=get_image_set(int(gt_row[0].split(".")[0]))
        with open('%s/FullIJCNN2013/%s/%s_gt.txt' %(img_db_dir, image_set, image_set), 'a') as subset_gt:
            subset_gt.write('%s/FullIJCNN2013/%s\n' % (img_db_dir, gt_row[0]))
