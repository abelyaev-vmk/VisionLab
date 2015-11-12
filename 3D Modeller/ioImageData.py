from ImageProperties import ImageProperties
import pickle
from GUI_consts import *


def save_image_data(ip, out_path):
    assert ip.__class__.__name__ == ImageProperties.__name__
    if '.' not in out_path:
        out_path += '.pick'
    print 'Saved image path: ', ip.image_path
    with open(out_path, 'wb') as f:
        pickle.dump(ip, f)


def load_image_data(in_path):
    if '.' not in in_path:
        in_path += '.pick'
    with open(in_path, 'rb') as f:
        ip = pickle.load(f)
    if ip.image_path:
        print 'Loaded image path', ip.image_path
    else:
        print 'Wrong image path. Loading %s' % imgTownCenterPath
        ip.image_path = imgTownCenterPath
    return ip
