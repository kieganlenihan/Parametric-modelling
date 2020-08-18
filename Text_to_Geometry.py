### Author Hyungsoo Kim
### Obtained from https://www.grasshopper3d.com/forum/topics/
###extruding-text-normal-to-the-surface?commentId=2985220%3AComment%3A1364746
import Rhino as rc

def flattenList(l):
    return [item for sublist in l for item in sublist]

def text2crv(text, font, textHeight):
    textCrvs = []

    for n in range(len(text)):
        textPt = rc.Geometry.Point3d(0,-(1.2 * n * textHeight),0)
        plane = rc.Geometry.Plane(textPt, rc.Geometry.Vector3d(0,0,1))

        if type(text[n]) is not str:
            preText = rc.RhinoDoc.ActiveDoc.Objects.AddText(`text[n]`, plane,
            ...textHeight, font, True, False)
        else:
            preText = rc.RhinoDoc.ActiveDoc.Objects.AddText(text[n], plane,
            ...textHeight, font, True, False)

        postText = rc.RhinoDoc.ActiveDoc.Objects.Find(preText)
        TG = postText.Geometry
        crv = TG.Explode()
        textCrvs.append(crv)

        rc.RhinoDoc.ActiveDoc.Objects.Delete(postText, True)

    return flattenList(textCrvs)

if not font: font = 'Arial'
if not height: textHeight = 20
else: textHeight = float(height)

if text and text[0]!=None:
    crvs = text2crv(text, font, textHeight)
