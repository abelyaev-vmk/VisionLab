import subprocess
from GUI_consts import *
from PIL import Image


def generate_kv(file_path='GUI.kv', source_path='SOURCE-2.jpg', size=(896, 506)):
    with open(file_path, 'w') as f:
        f.write(GUI_header)
        f.write('\t\tRectangle:\n\t\t\tid: Rect\n\t\t\tpos: east, south'
                '\n\t\t\tsource: "%s"\n\t\t\tsize: %d, %d' %
                (source_path, size[0], size[1]))
        f.write(GUI_text_input + '"%s"' % source_path)
        f.write(GUI_objects)
        f.close()


if __name__ == '__main__':
    source_path = 'SOURCE-2.jpg'
    img = Image.open(source_path, 'r')
    print img.size
    width, height = max(img.size[0] + EW_border, 900), img.size[1] + NS_border
    newSize = str(width) + "x" + str(height)
    print "--size=" + newSize
    generate_kv(file_path='GUI.kv', source_path=source_path, size=img.size)
    subprocess.call(["python", "GUI.py", "--size=" + newSize])


