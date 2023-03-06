#
# utility to make height map for game
# - requires Pillow (python -m pip install Pillow)
# - view with http://procgenesis.com/SimpleHMV/simplehmv.html
#

from PIL import Image
import math
import random

height_map = []
material_map = []

#
# initialize
#
def level(material_name, height, sizex, sizey):
    print(f"level {height}")
    material = get_material_number(material_name)
    global height_map
    global material_map
    height_map = []
    materialt_map = []

    hrow = []
    mrow = []
    for i in range (0, sizex):
        for j in range (0, sizey):
            hrow.append(height)
            mrow.append(material)
        height_map.append(hrow)
        material_map.append(mrow)
        hrow = []
        mrow = []

#
# save to .png
#
def save_height_image(filename):

    min_height=300
    max_height=0
    for my in range(0,size_y()):
        for mx in range(0, size_x()):
            height = get_height(mx,my)
            if max_height < height:
               max_height = height
            if min_height > height:
               min_height = height

    rgbArray = []
    for my in range(0,size_y()):
        rgb_row=[]
        for mx in range(0, size_x()):
            val = get_height(mx,my)
            norm_val = int((val - min_height) / (max_height-min_height) *  255.0)
            if norm_val > 255:
                rgb_row.append([norm_val,150,150])
            else:
                rgb_row.append([norm_val,norm_val,norm_val])
        rgbArray.append(rgb_row)

    newimage = Image.new('RGB', (len(rgbArray[0]), len(rgbArray)))  # type, size
    newimage.putdata([tuple(p) for row in rgbArray for p in row])
    newimage.save(filename)  # takes type from filename extension

def save_material_image(filename):

    for my in range(0,size_y()):
        for mx in range(0, size_x()):
            height = get_material(mx,my)

    rgbArray = []
    for my in range(0,size_y()):
        rgb_row=[]
        for mx in range(0, size_x()):
            val = get_material(mx,my)
            rgb_color = get_material_color(val)
            rgb_row.append(rgb_color)
        rgbArray.append(rgb_row)

    newimage = Image.new('RGB', (len(rgbArray[0]), len(rgbArray)))  # type, size
    newimage.putdata([tuple(p) for row in rgbArray for p in row])
    newimage.save(filename)  # takes type from filename extension

material_names = {
    "Air": 1,
    "Asphalt": 2,
    "Basalt":	3,
    "Brick":	4,
    "Cobblestone":	5,
    "Concrete":	6,
    "CrackedLava":	7,
    "Glacier":	8,
    "Grass":	9,
    "Ground":	10,
    "Ice":	11,
    "LeafyGrass":	12,
    "Limestone":	13,
    "Mud":	14,
    "Pavement":	15,
    "Rock":	16,
    "Salt":	17,
    "Sand":	18,
    "Sandstone":	19,
    "Slate":	20,
    "Snow":	21,
    "WoodPlanks":	22,
    "Water":	23
    }

material_colors = {
    1: [255, 255, 255],
    2: [115, 123, 107],
    3:	[30, 30, 37],
    4:	[138, 86, 62],
    5:	[132, 123, 90],
    6:	[127, 102, 63],
    7:	[232, 156, 74],
    8:	[101, 176, 234],
    9:	[106, 127, 63],
    10:	[102, 92, 59],
    11:	[129, 194, 224],
    12:	[115, 132, 74],
    13:	[206, 173, 148],
    14:	[58, 46, 36],
    15:	[148, 148, 140],
    16:	[102, 108, 111],
    17:	[198, 189, 181],
    18:	[143, 126, 95],
    19:	[137, 90, 71],
    20:	[63, 127, 107],
    21:	[195, 199, 218],
    22:	[139, 109, 79],
    23:	[12, 84, 92]
    }


def get_material_number(material_name):
    global material_names
    global material_colors

    #if actually is a number.. just return it
    if material_name in material_colors:
        return material_name

    if material_name in material_names:
        return material_names[material_name]
    else:
        print(f"unknown material name: {material_name}")
        return material_names["Ground"]

def get_material_color(material_number):
    global material_colors
    if material_number in material_colors:
        return material_colors[material_number]
    else:
        print(f"unknown material number: {material_number}")
        return material_colors[11] #Ice


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

def get_material(x,y):
    global material_map
    try:
        return material_map[x][y]
    except IndexError:
        return 0

def set_material_height(x,y, material, height):
    global material_map
    global height_map
    try:
        material_map[x][y] = material
        height_map[x][y] = height
    except IndexError:
        pass


def set_point(x,y, material, height, moves):
    for move in moves:
        if move=='norm':
            set_material_height(x,y, material, height)
        if move=='sym':
            set_material_height(size_x()-x,size_y()-y, material, height)
        if move=='mx':
            set_material_height(size_x()-x,y, material, height)
        if move=='my':
            set_material_height(x,size_y()-y, material, height)
        if move=='rot':
            set_material_height(y,x, material, height)
        if move=='rot_sym':
            set_material_height(size_y()-y,size_x()-x, material, height)
        if move=='rot_mx':
            set_material_height(size_y()-y,x, material, height)
        if move=='rot_my':
            set_material_height(y,size_x()-x, material, height)


def get_noise(noise):
    return (random.random()-0.5) * noise

def adjust_height(x,y, height, noise, mode, moves, material):
    cur_height = get_height(x,y)
    new_height = height + get_noise(noise)

    if mode=='set':
        set_point(x,y, material, new_height, moves)
    elif mode=='inc':
        set_point(x,y, material, get_height(x,y) + new_height, moves)
    elif mode=='and':
        if cur_height < height:
            set_point(x,y, material, height, moves)
    else:
        print("unknown mode")


def rect(height, x1, y1, x2, y2, noise, mode, moves, material_name):
    print(f"rect ({x1},{y1}) ({x2}, {y2}) height={height}")
    material = get_material_number(material_name)
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            adjust_height(x,y, height, noise, mode, moves, material)

def circle(height, cenx, ceny, size, noise, mode, moves, material_name):
    material = get_material_number(material_name)
    for mx in range(0,size_x()):
        for my in range(0, size_y()):
            distance = math.hypot(cenx-mx,ceny-my)
            if distance < size:
                adjust_height(mx, my, height, noise, mode, moves,material)

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

def mound(base_height, top_height, cenx, ceny, base_size, top_size, noise, mode, moves, material,top_material):
    print("mound")
    material = get_material_number(material)
    top_material = get_material_number(top_material)
    for mx in range(max(int(cenx-base_size),0),min(int(cenx+base_size),size_x())):
        for my in range(max(int(ceny-base_size),0),min(int(ceny+base_size),size_y())):
            distance = dist(cenx,ceny, mx, my)
            if distance < base_size:
                    if distance < top_size:
                        adjust_height(mx, my, top_height, noise/2.0, mode, moves, top_material)
                    else:
                        pos = distance - top_size
                        max_pos = base_size - top_size
                        opp_pos = max_pos - pos
                        pct_inc = opp_pos / max_pos
                        adjust_height(mx, my, base_height + ((top_height-base_height) * pct_inc), noise, mode, moves, material)

def ramp(start_height, end_height, x1,y1, x2,y2, width, end_buf, xy_noise, road_noise, edge_noise, mode, moves, end_mounds, material, top_material):

    width = width / 2 # since its radius
    material = get_material_number(material)
    top_material = get_material_number(top_material)

    print(f"ramp start_height={start_height}, end_height={end_height}, x1={x1}, y1={y1}")
    line_len = dist(x1,y1, x2,y2)
    inc_height = end_height - start_height

    if end_mounds:
        mound(start_height*0.8, start_height, x1, y1, width*1.3, width*1.0, road_noise, "and", moves,material,top_material)
        mound(end_height*0.8,   end_height,   x2, y2, width*1.3, width*1.0, road_noise, "and", moves,material,top_material)

    cenx = (x1+x2) / 2
    ceny = (y1+y2) / 2
    base_size = max(width + abs(x2 - x1), width + abs(y2-y1) )

    for mx in range(max(int(cenx-base_size),0),min(int(cenx+base_size),size_x())):
        for my in range(max(int(ceny-base_size),0),min(int(ceny+base_size),size_y())):
            dist_from_line = point_to_line_dist(mx,my, x1,y1, x2,y2) + ((math.sin((mx+my)/10)-0.5)*xy_noise) + get_noise(xy_noise/3)
            if dist_from_line < width*1.2:
                dist_from_start = dist(mx,my, x1,y1)
                dist_from_end   = dist(mx,my, x2,y2)

                if dist_from_start < line_len-end_buf and dist_from_end < line_len-end_buf:
                    pct_step = max(min((dist_from_start-end_buf) / (line_len-(end_buf*2)),1.0),0.0)
                    height = start_height + (inc_height * pct_step)
                    edge_height = start_height + (inc_height * (pct_step*0.5))

                    if dist_from_line < width:
                        adjust_height(mx,my, height, road_noise, mode, moves, top_material)
                    else:
                        adjust_height(mx,my, edge_height, edge_noise, 'and', moves, material)


def path(start_height, end_height, width, end_buf, coords, xy_noise, road_noise, edge_noise, mode, moves, material, top_material):
    print("path")
    material = get_material_number(material)
    top_material = get_material_number(top_material)

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

            ramp(ramp_start_height, ramp_end_height, prev_x, prev_y, x, y, width, end_buf, xy_noise, road_noise, edge_noise, mode, moves, True, material, top_material)

            cur_distance = cur_distance + d
            prev_x = x
            prev_y = y

