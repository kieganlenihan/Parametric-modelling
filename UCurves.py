### Author Kiegan Lenihan
### Inputs = [JoinedMesh, pointSlide]
### Outputs = [out, silhouette]
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

### Get Outlines
meshBase = JoinedMesh
outlines = rs.MeshOutline(meshBase, view="Top")

### Fix Outline to make silhouette
segments = 50
points = rs.DivideCurve(outlines, segments)
interpolatedCurve = rs.AddInterpCurve(points, degree=3,
 knotstyle=0, start_tangent=None, end_tangent=None)
startPoint = rs.CurveStartPoint(interpolatedCurve)
startTangent = rs.CurveTangent(interpolatedCurve, 0)
endPoint = rs.CurveEndPoint(interpolatedCurve)
endTangent = rs.CurveTangent(interpolatedCurve, 1)
patchPoints = [startPoint, endPoint]
silhouettePatch = rs.AddInterpCurve(patchPoints, degree=3,
 knotstyle=0, start_tangent = startTangent, end_tangent = endTangent)
curvesList = [interpolatedCurve, silhouettePatch]
silhouette = rs.JoinCurves(curvesList, delete_input=False, tolerance=None)

### Bounding Box
box = rs.BoundingBox(silhouette)
a = box
boxPointX = list(); boxPointY = list(); boxPointZ = list()
for i in range(len(box)):
    boxPoint = box[i]
    boxPointX_indiv = boxPoint[0]
    boxPointY_indiv = boxPoint[1]
    boxPointZ_indiv = boxPoint[2]
    boxPointX.append(boxPointX_indiv)
    boxPointY.append(boxPointY_indiv)
    boxPointZ.append(boxPointZ_indiv)
boxCenterPoint = rs.AddPoint((sum(boxPointX)/len(boxPointX),
sum(boxPointY)/len(boxPointY), sum(boxPointZ)/len(boxPointZ)))
b = boxCenterPoint

### Get Defining Curvature
curveParam = rs.CurveParameter(silhouette, pointSlide)
evalCurve = rs.EvaluateCurve(silhouette, curveParam)
pointOnCurve = rs.AddPoint(evalCurve)
c = pointOnCurve
index = 100
lengths = list(); drawLines = list()
for j in range(index):
    curveParam_new = rs.CurveParameter(silhouette, pointSlide + 1/index*j)
    evalCurve_new = rs.EvaluateCurve(silhouette, curveParam_new)
    pointOnCurve_new = rs.AddPoint(evalCurve_new)
    drawLine = rs.AddLine(pointOnCurve, pointOnCurve_new)
    drawLines.append(drawLine)
    length = rs.CurveLength(drawLine)
    lengths.append(length)
