import numpy as np
import camera

cam = camera.Camera()
# c.SetLocation(np.array([-0.05988363921642303467, 3.83331298828125000000, 12.39112186431884765625]))
# c.SetQuaternion(np.array([0.69724917918208628720, -0.43029624469563848566, 0.28876888503799524877, 0.49527896681027261394]))

cam.SetLocation(np.array([-0.059884, 3.8333, 12.3911]))
cam.SetQuaternion(np.array([0.69725, -0.4303, 0.28877, 0.49528]))

# use non-openGL coordinates
cam.UseNonGL()
# # use openGL coordinates
# c.UseGL()

viewMatrix = cam.GetViewMatrix()
location = cam.GetLocation()
forward = cam.GetForward()
up = cam.GetUp()
right = cam.GetRight()
quaternionOrder = "xyzw"

print "View matrix:\n", viewMatrix, "\n"
print "location: %s\n" % location
print "forward direction: %s" % forward
print "up direction: %s" % up
print "right direction: %s\n" % right
print "Used rotation vector: %s" % cam.GetRotationVector()
print "Used quaternion: %s\n" % cam.GetQuaternion(order=quaternionOrder)

cam.UseGL()
print "Quaternion for rotation in openGL: %s" % cam.GetQuaternion(order=quaternionOrder)