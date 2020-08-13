import os
from PIL import Image
from PIL import ImageFilter

path_in = "../pigeon"
path_out = "../pigeon_augumented"


def augument_images(path_in, path_out, circles=2):
    '''
    Image augumentation. Changes blur and sharpnes of the image
    :param path_in: folder that contains images that should be augumented. Type: str
    :param path_out: output folder for the augumented images. Type: str
    :param circles: how many times to perform augumentation. Type: int
    :return:
    '''

    filelist = []
    for r, d, f in os.walk(path_in):
        for file in f:
            if '.jpg' in file:
                filelist.append(file)

    for count in range(circles-1):
        for imagefile in filelist:
            os.chdir(path)
            im = Image.open(imagefile)
            im = im.convert("RGB")
            im_blur = im.filter(ImageFilter.GaussianBlur)
            im_unsharp = im.filter(ImageFilter.UnsharpMask)
            os.chdir(path_out)
            im_blur.save(str(count) + 'blur_' + imagefile)
            im_unsharp.save(str(count) + 'unsharp_' + imagefile)
    return

augument_images(path_in, path_out, 2)