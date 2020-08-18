### Author Kiegan Lenihan
### Inputs = CenteredMesh
### Outputs = [out, JoinedMesh]
import Rhino
from Rhino.Geometry import *
from Rhino.Input import RhinoGet
from Rhino.Commands import Result
from Rhino.DocObjects import ObjectType
import rhinoscriptsyntax as rs
from scriptcontext import doc
import math

coerceMesh = rs.coercemesh(CenteredMesh)

# fix mesh
coerceMesh.ExtractNonManifoldEdges(coerceMesh)
coerceMesh.UnifyNormals()
coerceMesh.SplitDisjointPieces()

vertices = rs.MeshVertices(coerceMesh)
naked = rs.MeshNakedEdgePoints(coerceMesh)
for i, vertex in enumerate(vertices):
    if naked[i]: a = rs.AddPoint(vertex)

# Fill Holes
if coerceMesh.GetNakedEdges():
    FillMeshes= []
    for pl in coerceMesh.GetNakedEdges():
        fm = Rhino.Geometry.Mesh()
        fm.Vertices.AddVertices(pl)
        faces = pl.TriangulateClosedPolyline()
        fm.Faces.AddFaces(faces)
    FillMeshes.append(fm)
    print "Number of holes patched: " + str(len(FillMeshes))
    FillMeshes.append(coerceMesh)
    RepairedMesh = FillMeshes
    print len(RepairedMesh)
    JoinedMesh = Rhino.Geometry.Mesh()
    for j in range(len(RepairedMesh)):
        JoinedMesh.Append(RepairedMesh[j])
else:
    print "Number of holes patched: 0"
    JoinedMesh = coerceMesh
