__author__ = 'Andrew'

import os
from skimage import data
from skimage.io import imsave
from skimage.transform import resize


def get_video():
    tvideo, tmask = [], []
    for v in os.listdir(mainPath + videoPath):
        if v[len(v) - 3:len(v)] != 'jpg':
            continue
        tvideo.append(data.imread(mainPath + videoPath + v))
    for m in os.listdir(mainPath + videoMaskPath):
        if m[len(m) - 3:len(m)] != 'jpg':
            continue
        tmask.append(data.imread(mainPath + videoMaskPath + m))
    length = max(len(tvideo), len(tmask))
    return tvideo[0:length], tmask[0:length]


def get_image():
    #used for inverted mask
    def invert(i):
        for x in range(i.shape[0]):
            for y in range(i.shape[1]):
                i[x, y] = 1 - i[x, y]
        return i
    img = data.imread(mainPath + imagePath + imageName + '.jpg')
    msk = data.imread(mainPath + imagePath + imageName + 'map.jpg')
    size = video[0].shape
    img = resize(img, size)
    msk = resize(msk, size)
    #return img, invert(msk)
    return img, msk


def make_union():
    def number(n):
        k = 1
        string = ''
        while k < len(video):
            k *= 10
            if n == 0:
                string += '0'
        if n == 0:
            return string
        while k / 10 > n:
            string += '0'
            k /= 10
        string += str(n)
        return string
    size = image.shape
    for z in range(len(video)):
        nowImage = image.copy()
        for i in range(size[0]):
            for j in range(size[1]):
               # if (video[z][i, j] != background).any() and videoMask[z][i, j][0] / 255.0 < imageMask[i, j][0]:
                if videoMask[z][i, j][0] / 255.0 < imageMask[i, j][0]:
                    for c in range(3):
                        nowImage[i, j][c] = video[z][i, j][c] / 255.0
        imsave(mainPath + unionPath + imageName + number(z) + '.jpg', nowImage)
        print(z, 'done')




if __name__ == '__main__':
    mainPath = 'C:\\Users\\Andrew\\Desktop\\VisionLab\\Python_Mask&Image\\'
    unionPath = 'Union\\'
    videoPath = 'Video\\'
    videoMaskPath = 'Mask\\'
    imagePath = 'Image\\'
    imageName = 'TownCenter'
    video, videoMask = get_video()
    image, imageMask = get_image()
   # background = video[0][0, 0]
    make_union()
    print(imageMask)
    print(videoMask[0])
    print(image)
