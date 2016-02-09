from PIL import Image


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
    return (x, y, w, h)


def get_image_size(img_db_dir, image_number):
    im = Image.open('%s/FullIJCNN2013/%s' % (img_db_dir, image_number))
    return im.size


def convert_txt(img_db_dir, gt_row):
    out_file_name = gt_row[0].split(".")[0]+".txt"
    with open('%s/FullIJCNN2013/labels/%s' % (img_db_dir, out_file_name), 'a') as f:
        b = gt_row[1:5]
        size = get_image_size(img_db_dir, gt_row[0])
        bb = convert(size, b)
        new_description = "%s %s\n" % (
            str(gt_row[5]),
            " ".join([str(a) for a in bb]))
        f.write(new_description)


def get_image_set(sets, pic_number):
    for image_set, n in sets:
        if int(pic_number) < n:
            return(image_set)
