### Author Kiegan Lenihan
### Inputs = input
### Outputs = [out, box]

import rhinoscriptsyntax as rs
import math
import Rhino

# initial Volume
def vol(bound):
    len = rs.Distance(bound[0], bound[1])
    wid = rs.Distance(bound[0], bound[3])
    hgt = rs.Distance(bound[0], bound[4])
    vol = len*wid*hgt
    return vol

# initiate
vol_x = []
vol_y = []
vol_z = []

foot_mesh = input
worldXY = rs.WorldXYPlane()
bound_1 = rs.BoundingBox(foot_mesh, worldXY)
vol_1 = vol(bound_1)

precision = 1 # degrees
# x-rotation
for i in range(0,int(180/precision)):
    plane_2 = rs.RotatePlane(worldXY, i*precision, [1,0,0])
    bound_2 = rs.BoundingBox(foot_mesh, plane_2)
    vol_x.append(int(vol(bound_2)))
rot_x = vol_x.index(min(vol_x))
plane_x = rs.RotatePlane(worldXY, rot_x, [1,0,0])

# y-rotation
for j in range(0,int(180/precision)):
    plane_3 = rs.RotatePlane(plane_x, j*precision, [0,1,0])
    bound_3 = rs.BoundingBox(foot_mesh, plane_3)
    vol_y.append(int(vol(bound_3)))
rot_y = vol_y.index(min(vol_y))
plane_y = rs.RotatePlane(plane_x, rot_y, [0,1,0])

# z-rotation
for k in range(0,int(180/precision)):
    plane_4 = rs.RotatePlane(plane_y, k*precision, [0,0,1])
    bound_4 = rs.BoundingBox(foot_mesh, plane_4)
    vol_z.append(int(vol(bound_4)))
rot_z = vol_z.index(min(vol_z))
plane_z = rs.RotatePlane(plane_y, rot_z, [0,0,1])

corners = rs.BoundingBox(foot_mesh, plane_z)

# mapped axes
axis_u = rs.VectorCreate(corners[0], corners[1])
axis_v = rs.VectorCreate(corners[0], corners[3])
axis_w = rs.VectorCreate(corners[0], corners[4])

# initiate mapped volumes
vol_u = []
vol_v = []
vol_w = []

for a in range(0,int(180/precision)):
    plane_5 = rs.RotatePlane(plane_z, a*precision, axis_u)
    bound_5 = rs.BoundingBox(foot_mesh, plane_5)
    vol_u.append(int(vol(bound_5)))
axis_u_new = vol_u.index(min(vol_u))
plane_axis_u = rs.RotatePlane(plane_z, axis_u_new, axis_u)

for b in range(0,int(180/precision)):
    plane_6 = rs.RotatePlane(plane_axis_u, b*precision, axis_v)
    bound_6 = rs.BoundingBox(foot_mesh, plane_6)
    vol_v.append(int(vol(bound_6)))
axis_v_new = vol_v.index(min(vol_v))
plane_axis_v = rs.RotatePlane(plane_axis_u, axis_v_new, axis_v)

for c in range(0,int(180/precision)):
    plane_7 = rs.RotatePlane(plane_axis_v, c*precision, axis_w)
    bound_7 = rs.BoundingBox(foot_mesh, plane_7)
    vol_w.append(int(vol(bound_7)))
axis_w_new = vol_w.index(min(vol_w))
plane_axis_w = rs.RotatePlane(plane_axis_v, axis_w_new, axis_w)

# generate box
box = rs.AddBox(rs.AddPoints(rs.BoundingBox(foot_mesh, plane_axis_w)))
