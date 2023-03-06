import sys
import os

from RobloxHeightMap import *

#base
level("Grass", 40, 1000, 1000)

#river
path(10, 10, 220, -60, [[0,600],[200,550],[300,500],[500,500],[550,500]],0,0,0,'set',['norm','sym'], "Rock", "Water")

#border
path(85, 85, 10, -5, [[0,0],[0,1000],[1000,1000],[1000,0],[0,0]],1,15,6,'set',['norm'], "Grass", "Rock")

#castle mound
mound(40,80, 200,180, 100,35, 0, 'and', ['norm','sym'],"Grass","Ground")

#spawn mound
mound(40,65, 765,115, 180,35, 0, 'and', ['norm','sym'],"Grass","Ground")

#little hills
mound(40,65, 572,314, 50, 5, 1, 'and',['norm','sym'],"Grass","Grass")
mound(40,65, 662,339, 50, 5, 1, 'and',['norm','sym'],"Grass","Grass")
mound(40,60, 314,320, 40, 2, 1, 'and',['norm','sym'],"Grass","Grass")
mound(40,60, 212,333, 40, 2, 1, 'and',['norm','sym'],"Grass","Grass")
mound(40,60, 302,212, 40, 2, 1, 'and',['norm','sym'],"Grass","Grass")
mound(40,65, 273,154, 60,15, 1, 'and',['norm','sym'],"Grass","Grass")

#path to castle
path(10, 80, 20,-10, [[750,383],
                      [717,379],
                      [696,388],
                      [633,392],
                      [613,382],
                      [606,369],
                      [609,341],
                      [606,302],
                      [590,276],
                      [561,271],
                      [539,286],
                      [526,305],
                      [540,352],
                      [508,384],
                      [416,380],
                      [394,374],
                      [313,370],
                      [266,343],
                      [265,294],
                      [285,284],
                      [316,283],
                      [355,264],
                      [363,246],
                      [361,144],
                      [350,122],
                      [311,104],
                      [230,91],
                      [191,105],
                      [193,177]],
                      0,0,0,'set',['norm','sym'], 'Grass', 'Concrete')


hmap_filename = os.path.splitext(__file__)[0] + "_hmap.png"
save_height_image(hmap_filename)

material_filename = os.path.splitext(__file__)[0] + "_material.png"
save_material_image(material_filename)

print("done.")

