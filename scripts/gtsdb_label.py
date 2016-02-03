import sys
from os import getcwd
import os.path
from PIL import Image

if len(sys.argv) > 1:
    img_db_dir = os.path.abspath(sys.argv[1])
    if not os.path.exists(img_db_dir):
        print("Directory %s does not exist!" % img_db_dir)
        sys.exit(1)
else:
    print("usage: python %s img_db_dir" % sys.argv[0])
    sys.exit(1)

sets=[('train', 720), ('val', 90),('test', 90)]

classes = [("0" + str(i))[-2:] for i in range(43)]

"""
the generated text files has to be in <object-class> <x> <y> <width> <height>
where x,y,width,height is in percentages
"""
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
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
    with open('%s/FullIJCNN2013/labels/%s'%(img_db_dir, out_file_name),'w') as f:
        b=gt_row[1:5]
        size=get_image_size(gt_row[0])
        bb=convert(size,b)
        f.write(gt_row[5] + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

with open('%s/FullIJCNN2013/gt.txt' % img_db_dir) as read_f:
    for image_set, n in sets:
        with open('%s/FullIJCNN2013/%s/%s_gt.txt' %(img_db_dir, image_set, image_set), 'w') as subset_gt:
            for i in xrange(n):
                line = read_f.next()
                gt_row=line.split(";")
                for i in range (1,4):
                    gt_row[i]=int(gt_row[i])
                convert_txt(gt_row)
                subset_gt.write('%s/FullIJCNN2013/%s' % (img_db_dir, gt_row[0]))
