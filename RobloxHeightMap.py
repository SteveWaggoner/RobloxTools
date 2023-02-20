#
# utility to make height map for game
# - requires Pillow (python -m pip install Pillow)
# - view with http://procgenesis.com/SimpleHMV/simplehmv.html
#

from PIL import Image
import math
import random

height_map = []
max_height=150

#
# initialize
#
def level(height,sizex, sizey):
    global height_map
    height_map = []

    row = []
    for i in range (0, sizex):
        for j in range (0, sizey):
            row.append(height)
        height_map.append(row)
        row = []

#
# save to .png
#
def save_image(filename):
    global height_map
    global max_height

    rgbArray = []
    for my in range(0,size_y()):
        rgb_row=[]
        for mx in range(0, size_x()):
            val = get_height(mx,my)
            norm_val = int(val / max_height *  255.0)
            if norm_val > 255:
                rgb_row.append([norm_val,150,150])
            else:
                rgb_row.append([norm_val,norm_val,norm_val])
        rgbArray.append(rgb_row)

    newimage = Image.new('RGB', (len(rgbArray[0]), len(rgbArray)))  # type, size
    newimage.putdata([tuple(p) for row in rgbArray for p in row])
    newimage.save(filename)  # takes type from filename extension


def size_x():
    return len(height_map[0])

def size_y():
    return len(height_map)

def get_height(x,y):
    global height_map
    try:
        return height_map[x][y]
    except IndexError:
        return 0

def set_height(x,y, height):
    global height_map
    try:
        height_map[x][y] = height
    except IndexError:
        pass

def get_noise(noise):
    return (random.random()-0.5) * noise

def adjust_height(x,y, height, noise, mode):
    cur_height = get_height(x,y)
    new_height = height + get_noise(noise)

    if mode=='set':
        set_height(x,y, new_height)
    elif mode=='inc':
        set_height(x,y, get_height(x,y) + new_height)
    elif mode=='and':
        if cur_height < height:
            set_height(x,y, height)
    else:
        print("unknown mode")


def rect(height, x1, y1, x2, y2, noise, mode):
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            adjust_height(x,y, height, noise, mode)

def circle(height, cenx, ceny, size, noise, mode):
    global height_map
    for mx in range(0,size_x()):
        for my in range(0, size_y()):
            distance = math.hypot(cenx-mx,ceny-my)
            if distance < size:
                adjust_height(mx, my, height, noise, mode)

def dist(x1,y1,x2,y2):
    return math.hypot(x2-x1,y2-y1)

def get_line(x1, y1, x2, y2):
    # (x- p1X) / (p2X - p1X) = (y - p1Y) / (p2Y - p1Y)
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return [a,b,c]

def point_to_line_dist(px, py, lx1, ly1, lx2, ly2):
    [a,b,c] = get_line(lx1,ly1,lx2,ly2)
    return abs(a * px + b * py + c) / math.sqrt(a * a + b * b) #assumes line is infinite

def mound(base_height, top_height, cenx, ceny, base_size, top_size, noise, mode):
    print("mound")
    global height_map
    for mx in range(0,size_x()):
        for my in range(0, size_y()):
            distance = dist(cenx,ceny, mx, my)
            if distance < base_size:
                    if distance < top_size:
                        adjust_height(mx, my, top_height, noise/2.0, mode)
                    else:
                        pos = distance - top_size
                        max_pos = base_size - top_size
                        opp_pos = max_pos - pos
                        pct_inc = opp_pos / max_pos
                        adjust_height(mx, my, base_height + ((top_height-base_height) * pct_inc), noise, mode)

def ramp(start_height, end_height, x1,y1, x2,y2, width, end_buf, xy_noise, road_noise, edge_noise, mode):
    print(f"ramp start_height={start_height}, end_height={end_height}, x1={x1}, y1={y1}")
    global height_map
    line_len = dist(x1,y1, x2,y2)
    inc_height = end_height - start_height

    mound(start_height*0.8, start_height, x1, y1, width*1.3, width*1.0, road_noise, "and")
    mound(end_height*0.8,   end_height,   x2, y2, width*1.3, width*1.0, road_noise, "and")

    for mx in range(0,size_x()):
        for my in range(0, size_y()):
            dist_from_line = point_to_line_dist(mx,my, x1,y1, x2,y2) + ((math.sin((mx+my)/10)-0.5)*xy_noise) + get_noise(xy_noise/3)
            if dist_from_line < width*1.2:
                dist_from_start = dist(mx,my, x1,y1)
                dist_from_end   = dist(mx,my, x2,y2)

                if dist_from_start < line_len-end_buf and dist_from_end < line_len-end_buf:
                    pct_step = max(min((dist_from_start-end_buf) / (line_len-(end_buf*2)),1.0),0.0)
                    height = start_height + (inc_height * pct_step)
                    edge_height = start_height + (inc_height * (pct_step*0.5))

                    if dist_from_line < width:
                        adjust_height(mx,my, height, road_noise, mode)
                    else:
                        adjust_height(mx,my, edge_height, edge_noise, 'and')


def path(start_height, end_height, width, end_buf, coords, xy_noise, road_noise, edge_noise, mode):
    print("path")
    total_distance = 0
    prev_x = None
    prev_y = None
    for (x,y) in coords:
        if prev_x == None:
            prev_x = x
            prev_y = y
        else:
            d = dist(prev_x, prev_y, x, y)
            total_distance = total_distance + d
            prev_x = x
            prev_y = y

    prev_x = None
    prev_y = None
    cur_distance = 0.0
    for (x,y) in coords:
        if prev_x == None:
            prev_x = x
            prev_y = y
        else:
            d = dist(prev_x, prev_y, x, y)

            start_pct = (1.0*   cur_distance /total_distance)
            end_pct   = (1.0*(d+cur_distance)/total_distance)

            ramp_start_height = start_height + ((end_height - start_height) * start_pct)
            ramp_end_height   = start_height + ((end_height - start_height) * end_pct)

            ramp(ramp_start_height, ramp_end_height, prev_x, prev_y, x, y, width, end_buf, xy_noise, road_noise, edge_noise, mode)

            cur_distance = cur_distance + d
            prev_x = x
            prev_y = y


def sym_rect(height, x1, y1, x2, y2, noise, mode):
    rect(height, x1, y1, x2, y2, noise, mode)
    rect(height, size_x()-x2, size_y()-y2, size_x()-x1, size_y()-y1, noise, mode)

def sym_circle(height, x, y, width, noise, mode):
    circle(height, x, y, width, noise, mode)
    circle(height, size_x()-x, size_y()-y, width, noise, mode)

def sym_mound(base_height, top_height, cenx, ceny, base_size, top_size, noise, mode):
    mound(base_height, top_height, cenx, ceny, base_size, top_size, noise, mode)
    mound(base_height, top_height, size_x()-cenx, size_y()-ceny, base_size, top_size, noise, mode)

def sym_coords(coords):
    new_coords=[]
    for (x,y) in coords:
        new_coords.append([size_x()-x,size_y()-y])
    return new_coords

def sym_path(start_height, end_height, width, end_buf, coords, xy_noise, road_noise, edge_noise, mode):
    path(start_height, end_height, width, end_buf, coords, xy_noise, road_noise, edge_noise, mode)
    path(start_height, end_height, width, end_buf, sym_coords(coords), xy_noise, road_noise, edge_noise, mode)

#base
level(40, 1000, 1000)

#river
sym_path(10, 10, 120, -60, [[0,600],[200,550],[300,500],[500,500],[550,500]],0,0,0,'set')

#border
path(85, 85, 10, -5, [[0,0],[0,1000],[1000,1000],[1000,0],[0,0]],1,15,6,'set')

#castle mound
sym_mound(40,80, 200,180, 100,35, 1, 'and')

#spawn mound
sym_mound(40,65, 765,115, 180,35, 1, 'and')

#little hills
sym_mound(40,65, 572,314, 50,5, 1, 'and')
sym_mound(40,65, 662,339, 50,5, 1, 'and')
sym_mound(40,60, 314,320, 40,2, 1, 'and')
sym_mound(40,60, 212,333, 40,2, 1, 'and')
sym_mound(40,60, 302,212, 40,2, 1, 'and')
sym_mound(40,65, 273,154, 60,15, 1, 'and')

#path to castle
sym_path(10, 80, 10,-10, [[750,383],
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
                      0,0,0,'set')

save_image("hmap.png")
print("done.")

