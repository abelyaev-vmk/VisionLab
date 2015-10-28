from ImageProperties import ImageProperties
import pickle


def save_image_data(ip, out_path):
    assert ip.__class__.__name__ == ImageProperties.__name__
    if '.' not in out_path:
        out_path += '.pick'
    with open(out_path, 'wb') as f:
        pickle.dump(ip, f)


def load_image_data(in_path):
    if '.' not in in_path:
        in_path += '.pick'
    with open(in_path, 'rb') as f:
        ip = pickle.load(f)
    return ip
