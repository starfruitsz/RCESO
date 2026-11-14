# -*- coding: utf-8 -*-
from pptx import Presentation
path = r"C:\Users\Administrator\Desktop\2026.10--2_b0combined.pptx"
p = Presentation(path)
s = p.slides[4]
old = None
for sh in s.shapes:
    if sh.shape_type == 13 and sh.width > 5000000:
        old = sh; break
assert old is not None
left, top, width, height = old.left, old.top, old.width, old.height
pic = s.shapes.add_picture("ppt_s5_combined.png", left, top, width, height)
pic.name = "图片 3"
s.shapes._spTree.remove(old._element)
p.save(path)
print("replaced s5")
