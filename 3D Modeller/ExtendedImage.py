from PIL import Image
import pickle


class ExtendedImage:
    def __init__(self, image=None, offset=(0, 0), shape_reducing=1, key='ground'):
        self.image = image
        self.offset_x, self.offset_y = offset
        self.shape_reducing = shape_reducing
        self.key = key
        if self.image:
            self.pixels = self.image.load()

    def image_coordinates(self, point):
        return (point[0] / self.shape_reducing - self.offset_x,
                point[1] / self.shape_reducing - self.offset_y)

    def __getitem__(self, item):
        if not self.image:
            raise ValueError('There\'s no image here!')
        return self.image.getpixel((item[0] / self.shape_reducing - self.offset_x,
                                    item[0] / self.shape_reducing - self.offset_y))

    def __setitem__(self, key, value):
        if not self.image:
            raise ValueError('There\'s no image here!')
        self.pixels[key] = value

    def save(self, project='SOURCE'):
        source = project + '_' + self.key + '_world_image'
        self.image.save(source + '_' + self.key + '.jpg')
        with open(source + '.pick', 'wb') as f:
            pickle.dump([self.offset_x, self.offset_y, self.shape_reducing], f)

    @staticmethod
    def load(project='SOURCE', key='ground'):
        source = project + '_' + key + '_world_image'
        try:
            with open(source + '.pick', 'rb') as f:
                ox, oy, r = pickle.load(f)
            return ExtendedImage(image=Image.open(source + '_' + key + '.jpg'),
                                 offset=(ox, oy),
                                 shape_reducing=r)
        except IOError:
            return None

    def show(self):
        self.image.show()
