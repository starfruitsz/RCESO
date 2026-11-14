# -*- coding: utf-8 -*-
from pptx import Presentation
src = r"C:\Users\Administrator\Desktop\2026.10--2.pptx"
dst = r"C:\Users\Administrator\Desktop\2026.10--2_b0combined.pptx"
files = {5:"ppt_s5_combined.png", 6:"ppt_s6_combined.png", 8:"ppt_s8_combined.png",
         10:"ppt_s10_combined.png", 13:"ppt_s13_combined.png", 16:"fig_b0_adaptive_ppt.png"}
p = Presentation(src)
for idx, fn in files.items():
    s = p.slides[idx-1]
    old = None
    for sh in s.shapes:
        if sh.shape_type == 13 and sh.width > 5000000:
            old = sh; break
    assert old is not None, idx
    left, top, width, height = old.left, old.top, old.width, old.height
    pic = s.shapes.add_picture(fn, left, top, width, height)
    pic.name = "图片 3"
    s.shapes._spTree.remove(old._element)
p.save(dst)
q = Presentation(dst)
print("slides", len(q.slides))
for idx in files:
    pics = [sh for sh in q.slides[idx-1].shapes if sh.shape_type == 13]
    print(idx, [(round(sh.width/914400,2), round(sh.height/914400,2), len(sh.image.blob)) for sh in pics])
