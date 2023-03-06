import sys
import os

from RobloxHeightMap import *

max_height=250


#base
level("Grass", 91, 1000, 1000)


#border
path(120, 120, 10, -5, [[0,0],[0,1000],[1000,1000],[1000,0],[0,0]],1,15,6,'set',['norm'],"Grass","Rock")

def ring (off,ring_height, width, drop, ramp_off, mode, mat1, mat2, mat3):

    rect(ring_height, 0+off, 0+off, 1000-off, 0+off+width, 0, 'set', ['norm','rot','rot_mx','my'],mat1)

    flat_start_x = off
    ramp_start_x = off + ramp_off
    ramp_end_x   = 500 - ramp_off
    flat_end_x   = 500

    start_y = off
    end_y = off+width
    middle_y = off+(width/2)


    all_moves = ['norm','mx','my','sym','rot','rot_mx','rot_my','rot_sym']

    if mode == "inner_ramp":
            rect(ring_height,      flat_start_x, start_y, ramp_start_x, end_y, 0, 'set', all_moves, mat1)
            rect(ring_height+drop, ramp_end_x,   start_y, flat_end_x,   end_y, 0, 'set', all_moves, mat1)
            ramp(ring_height, ring_height+drop, ramp_start_x, middle_y, ramp_end_x, middle_y, width, 0, 0, 0, 0, 'set', all_moves, False, mat2, mat3)
    elif mode == "outer_ramp":
            rect(ring_height+drop, flat_start_x, start_y, ramp_start_x, end_y, 0, 'set', all_moves, mat1)
            rect(ring_height,      ramp_end_x,   start_y, flat_end_x,   end_y, 0, 'set', all_moves, mat1)
            ramp(ring_height+drop, ring_height, ramp_start_x, middle_y, ramp_end_x, middle_y, width, 0, 0, 0, 0, 'set', all_moves, False, mat2, mat3)




ring ( 40,90,20,10,90,"","Grass","","")
ring ( 60,80,20,10,90,"inner_ramp","Grass","Grass","Grass")
ring ( 80,80,20,10,90,"","Grass","","")
ring (100,70,20,10,90,"outer_ramp","Grass","Grass","Grass")

ring (120,70,20,10,90,"","Grass","Grass","Ground")
ring (140,60,20,10,90,"inner_ramp","Grass","Grass","Ground")
ring (160,60,20,10,90,"","Grass","Grass","Ground")
ring (180,50,20,10,90,"outer_ramp","Grass","Grass","Ground")

ring (200,50,20,10,90,"","Ground","Ground","Ground")
ring (220,40,20,10,90,"inner_ramp","Ground","Ground","Ground")
ring (240,40,20,10,90,"","Ground","Ground","Ground")
ring (260,30,20,10,90,"outer_ramp","Ground","Ground","Ground")

ring (280,30,20,10,50,"","Rock","Rock","Ground")
ring (300,20,20,10,50,"inner_ramp","Rock","Rock","Ground")
ring (320,20,20,10,50,"","Rock","Rock","Ground")
ring (340,10,20,10,50,"outer_ramp","Rock","Rock","Ground")

ring (360,10,20,10,10,"","Basalt","","")
ring (380,0,20,10,10,"inner_ramp","Basalt","Basalt","Rock")
ring (400,0,20,10,10,"outer_ramp","Basalt","Basalt","Rock")
ring (420,2,20,10,10,"","Basalt","","")
ring (440,2,20,10,10,"","Basalt","","")

circle(0,500,500,50,2,'set',['norm'],"CrackedLava")
circle(0,460,460,25,2,'set',['norm','mx','my','sym'],"CrackedLava")

hmap_filename = os.path.splitext(__file__)[0] + "_hmap.png"
save_height_image(hmap_filename)

material_filename = os.path.splitext(__file__)[0] + "_material.png"
save_material_image(material_filename)

print("done.")

