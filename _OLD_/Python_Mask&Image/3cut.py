import os
import numpy as np
from skimage import data
from skimage.io import imsave



def makeAndSave(image, path, number):
    size = image.shape
    img1 = np.zeros([size[0] / 3, size[1], size[2]])
    img2 = np.zeros([size[0] / 3, size[1], size[2]])
    img3 = np.zeros([size[0] / 3, size[1], size[2]])
    img1[:, :, :] = image[0: size[0] / 3, :, :] / 255.0
    img2[:, :, :] = image[size[0] / 3 + 1: 2 * size[0] / 3, :, :] / 255.0
    img3[:, :, :] = image[2 * size[0] / 3 + 1: size[0], :, :] / 255.0
    end_path = path
    for _ in range(4 - len(str(number))):
        end_path += '0'
    end_path += str(number)
    imsave(end_path + '1.jpg', img1)
    imsave(end_path + '2.jpg', img2)
    imsave(end_path + '3.jpg', img3)
    print(number)

def cut(img):
    p = [529, 429]
    size = [2525, 1669, 3]
    return img[p[0]:p[0] + size[0], p[1]:p[1]+size[1], :]

if __name__ == '__main__':
    path = 'C:\\Users\\Andrew\\Downloads\\Lektsiii_Kapustina_2014_g\\'
    i = 0
    for v in os.listdir(path):
        if v[len(v) - 3:len(v)] != 'jpg':
            continue
        image = cut(data.imread(path + v))
        makeAndSave(image, path + 'New\\', int(v[9:len(v) - 4]))
        i += 1
