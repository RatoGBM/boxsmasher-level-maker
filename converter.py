from PIL import Image

def main(save_to_output=False):
    input_file = 'example-level.png'
    output_file = 'example-level.lua'

    author = "me"
    totalBalls = 2
    grid_constant = 40 # don't change
    # grid size is 1280/40 = 32 x 720/40=18 pixels (conf.lua)
    color_designations = [
        [(255,0,0,255),'boxclusters',''],
        [(0,255,0,255),'throwBoundary',''],
        [(0,0,255,255),'terrain','']
    ]

    level = build(input_file,output_file,author,totalBalls,grid_constant,color_designations)
    if (save_to_output):
        with open(output_file,'w') as f:
            f.write(level)
    return level

def load_image(filename):
    i = Image.open(filename)
    px = i.load() # this is not a list
    width, height = i.size
    pixels = [[px[x,y] for x in range(width)] for y in range(height)]
    return pixels, width, height

def grouping(pixels, width, height):
    groups = []
    id_map = [[0 for x in range(width)] for y in range(height)]
    group_i = 1
    def check_row(x,y,w,base) -> bool:
        for i in range(w):
            if not (id_map[y][x+i]==0 and pixels[y][x+i]==base):
                return False
        return True
    def mark_row(x,y,w,group_i):
        for i in range(w):
            id_map[y][x+i] = group_i
    for x in range(width):
        for y in range(height):

            if (id_map[y][x]==0 and pixels[y][x][3]!=0):
                base = pixels[y][x]
                xc = x
                yc = y
                h = 0
                w = 0
                # width
                while (xc+w<width and pixels[yc][xc+w]==base):
                    w+=1

                # height
                while (yc+h<height and check_row(xc,yc+h,w,base)):
                    mark_row(xc,yc+h,w,group_i)
                    h+=1

                groups.append([xc,yc,w,h,base])
    print("-- Groups",len(groups))
    return groups

def throwBoundaryFormatting(boundary,grid_constant):
    return f"""
        x = {grid_constant}*{boundary[0]}, y = {grid_constant}*{boundary[1]},
        w = {grid_constant}*{boundary[2]}, h = {grid_constant}*{boundary[3]},"""
def clustersFormatting(clusters,grid_constant):
    return ",".join([clusterFormatting(cluster,grid_constant) for cluster in clusters])
def clusterFormatting(cluster,grid_constant):
    return f"""
    \t{{
    \t    x = {grid_constant}*{cluster[0]}, y = {grid_constant}*{cluster[1]},
    \t    w = {grid_constant}, h = {grid_constant},
    \t    aX = {cluster[2]}, aY = {cluster[3]},
    \t    {cluster[5]}
    \t}}"""
def terrainsFormatting(clusters,grid_constant):
    return ",".join([terrainFormatting(cluster,grid_constant) for cluster in clusters])
def terrainFormatting(cluster,grid_constant):
    return f"""
    \t{{
    \t    x = {grid_constant}*{cluster[0]}, y = {grid_constant}*{cluster[1]},
    \t    w = {grid_constant}*{cluster[2]}, h = {grid_constant}*{cluster[3]},
    \t    {cluster[5]}
    \t}}"""

def build(input_file,output_file,author,totalBalls,grid_constant,color_designations):
    pixels, width, height = load_image(input_file)
    groups = grouping(pixels, width, height)
    
    boundaries = {
        'boxclusters' : [],
        'throwBoundary' : [],
        'terrain' : []
    }

    for group in groups:
        for c in color_designations:
            if c[0]==group[4]:
                group.append(c[2])
                boundaries[c[1]].append(group)
    
    level = f"""return {{
    author = "{author}",
    totalBalls = {totalBalls},
    throwBoundary = {{{throwBoundaryFormatting(boundaries['throwBoundary'][0],grid_constant)}
    }},
    boxclusters = {{{clustersFormatting(boundaries['boxclusters'],grid_constant)}
    }},
    terrain = {{{terrainsFormatting(boundaries['terrain'],grid_constant)}
    }},
}}
"""
    return level

print(main(True))