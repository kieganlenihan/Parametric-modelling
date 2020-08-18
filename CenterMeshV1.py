### Author Kiegan Lenihan
### Inputs = mesh
### Outputs = [out, CenteredMesh]
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import math
 # move mesh to origin
centerPoint = rs.AddPoint(rs.MeshAreaCentroid(mesh))
origin = (0,0,0)
vectorMove = rs.VectorCreate(origin,centerPoint)
moved = rs.MoveObject(mesh,vectorMove)
print moved

# rotate so longest dimension is in x
vertices = rs.MeshVertices(moved)
vertCount = rs.MeshVertexCount(moved)
step = int(math.floor(vertCount/100))
lines = list() # initialize lines
lengths = list() # initialize lengths
for i in range(0,step):
    vertQuery = i*100
    edgePntQuery = vertices[vertQuery]
    lineEdgePntQuery = rs.AddLine(origin,edgePntQuery)
    lengthLineEdgePntQuery = rs.CurveLength(lineEdgePntQuery)
    lines.append(lineEdgePntQuery)
    lengths.append(lengthLineEdgePntQuery)
longestLine = lines[lengths.index(max(lengths))]
vectorRot = rs.VectorCreate(origin,rs.CurveEndPoint(longestLine))
vectorRotLength = rs.VectorLength(vectorRot)
pointXaxis = (vectorRotLength,0,0)
vectorXaxis = rs.VectorCreate(origin,pointXaxis)
axis = rs.VectorCrossProduct(vectorRot,vectorXaxis)
angle = rs.VectorAngle(vectorRot,vectorXaxis)
rotated = rs.RotateObject(moved,origin,angle, axis,copy=True)

# rotate so second longest dimension is in y
angleSteps = 100
xAxis = rs.VectorCreate(origin,(100,0,0))
lengthsY = list()
yCoords = list()
for j in range(0,angleSteps+1):
    meshAngle = 360/angleSteps*j
    rotated2 = rs.RotateObject(rotated,origin,meshAngle,xAxis,copy=True)
    box = rs.BoundingBox(rotated2)
    yCoords.append(rs.VectorCreate(origin,box[3])[1])
rotAngle = 360/angleSteps*yCoords.index(min(yCoords))
rotatedFinal = rs.RotateObject(rotated,origin,rotAngle,xAxis,copy=True)

# move so that no part of mesh is beneath z = 0
lowestPoint = rs.MeshClosestPoint(rotatedFinal,(0,0,-1000),maximum_distance=None)
lowestPoint = lowestPoint[0]
newLowestPoint = (lowestPoint[0],lowestPoint[1],5)
vectorMove2 = rs.VectorCreate(newLowestPoint,lowestPoint)
moved2 = rs.MoveObject(rotatedFinal,vectorMove2)
CenteredMesh = moved2
print CenteredMesh
