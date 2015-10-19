import numpy as np
import camera

c = camera.Camera()
# c.SetLocation(np.array([-0.05988363921642303467, 3.83331298828125000000, 12.39112186431884765625]))
# c.SetQuaternion(np.array([0.69724917918208628720, -0.43029624469563848566, 0.28876888503799524877, 0.49527896681027261394]))

c.SetLocation(np.array([-0.059884, 3.8333, 12.3911]))
c.SetQuaternion(np.array([0.49528, 0.69725, -0.4303, 0.18877]))

# use non-openGL coordinates
c.UseNonGL()
# # use openGL coordinates
# c.UseGL()
viewMatrix = c.GetViewMatrix()
print("View matrix:")
print(viewMatrix)

print("")

location = c.GetLocation()
print("location: %s" % location)

print("")

forward = c.GetForward()
up = c.GetUp()
right = c.GetRight()
print("forward direction: %s" % forward)
print("up direction: %s" % up)
print("right direction: %s" % right)

print("")

print("Used rotation vector: %s" % c.GetRotationVector())
print("Used quaternion: %s" % c.GetQuaternion())

print("")

c.UseGL()
print("Quaternion for rotation in openGL: %s" % c.GetQuaternion())
