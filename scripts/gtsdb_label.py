import os
from os import listdir, getcwd
from os.path import join
from PIL import Image
sets=[('train'), ('val'),('test')]

classes=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42"]

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
    im=Image.open('Imgdb/FullIJCNN2013/%s'%image_number)
    return im.size    

def convert_txt(gt_row):
    out_file_name=gt_row[0].split(".")[0]+".txt"
    with open('Imgdb/FullIJCNN2013/labels/%s'%(out_file_name),'w') as f:
        b=gt_row[1:5]
        size=get_image_size(gt_row[0])
        bb=convert(size,b)
        f.write(gt_row[5] + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
    with open('Imgdb/%s/gt.txt'%(image_set)) as read_f:
        for line in read_f:
            gt_row=line.split(";")
            for i in range (1,4):
                gt_row[i]=int(gt_row[i])
            convert_txt(gt_row)
        
