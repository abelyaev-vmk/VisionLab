import numpy as np
# import cv2
from camera import Camera
from optparse import OptionParser


if __name__== '__main__':
    parser = OptionParser()
    parser.add_option("-o", "--out", dest="DST_FILE",
                      help="write matrix to FILE")
    parser.add_option("-f", "--file", dest="SRC_FILE",
                      help="get data from FILE")
    parser.add_option("-g", "--gl", action="store_true",
                      dest="useGL", help="use openGL coordinates")
    parser.add_option("-q", "--qorder", dest="QORDER",
                      help="set quaternion order, default: xyzw")
    parser.add_option("--full", action="store_true",
                      dest="full", help="write full info files")
    options, args = parser.parse_args()
    options_dict = vars(options)
    if options_dict.get("SRC_FILE"):
        with open(options_dict.get("SRC_FILE"), "r") as f:
            location = np.array(map(float, f.readline().split(' ')))
            quaternion = np.array(map(float, f.readline().split(' ')))
    else:
        location = np.array([0.49528, 0.69725 -0.4303])
        quaternion = np.array([0.28877, -0.059884, 3.8333, 12.3911])

    if options_dict.get("QORDER"):
        quaternionOrder = options_dict.get("QORDER")
    else:
        quaternionOrder = "xyzw"

    cam = Camera()
    cam.SetLocation(location)
    cam.SetQuaternion(in_quaternion=quaternion, order=quaternionOrder)

    if options_dict.get("useGL"):
        cam.isGL = True
    else:
        cam.isGL = False

    viewMatrix = cam.GetViewMatrix()
    location = cam.GetLocation()
    forward = cam.GetForward()
    up = cam.GetUp()
    right = cam.GetRight()

    if options_dict.get("DST_FILE"):
        path = options_dict.get("DST_FILE")
        help_path = path[0:len(path) - 4] + '_help' + path[len(path) - 4:len(path)]
        with open(path, "w") as f:
            if options_dict.get("full"):
                f.write(str(viewMatrix) + '\n')
                f.write(str(forward) + '\n')
                f.write(str(up) + '\n')
                f.write(str(right) + '\n')
                f.write(str(cam.GetRotationMatrix()) + '\n')
            f.write(str(location) + '\n')
            f.write(str(cam.GetQuaternion(order=quaternionOrder)) + '\n')
            cam.UseGL()
            f.write(str(cam.GetQuaternion(order=quaternionOrder)) + '\n')

        with open(help_path, "w") as f:
            if options_dict.get("full"):
                f.write("View matrix")
                f.write("forward direction")
                f.write("up direction")
                f.write("right direction")
                f.write("Used rotation vector")
            f.write("location")
            f.write("Used quaternion")
            f.write("Quaternion for rotation in openGL")
    else:
        print "View matrix:\n", viewMatrix, "\n"
        print "location: %s\n" % location
        print "forward direction: %s" % forward
        print "up direction: %s" % up
        print "right direction: %s\n" % right
        print "Used rotation vector: %s" % cam.GetRotationVector()
        print "Used quaternion: %s\n" % cam.GetQuaternion(order=quaternionOrder)

        cam.UseGL()
        print "Quaternion for rotation in openGL: %s" % cam.GetQuaternion(order=quaternionOrder)

