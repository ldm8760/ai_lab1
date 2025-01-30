import sys
from PIL import Image

open_land = {"#F89412": 3}  # (248, 148, 18)
rough_meadow = {"#FFC000": 2.2}  # (255, 192, 0)
easy_movement_forest = {"#FFFFFF": 2.7}  # (255, 255, 255)
slow_run_forest = {"#02D03C": 2.3}  # (2, 208, 60)
walk_forest = {"#028828": 1.6}  # (2, 136, 40)
impassible_vegetation = {"#054918": 0}  # (5, 73, 24)
lake_swamp_marsh = {"#0000FF": 1}  # (0, 0, 255)
paved_road = {"#473303": 3}  # (71, 51, 3)
footpath = {"#000000": 3}  # (0, 0, 0)
out_of_bounds = {"#CD0065": 0}  # (205, 0, 101)

# speed in meters per second
# open_speed = 3
# rough_speed = 2.2
# easy_forest_speed = 2.7
# slow_forest_speed = 2
# walk_forest_speed = 


terrain = sys.argv[1]
elevation = sys.argv[2]
points_to_visit = sys.argv[3]
output_file = sys.argv[4]

coords = [
    (230, 327), (276, 279), (303, 240), (322, 242), (306, 286), 
    (319, 320), (325, 339), (312, 366), (275, 353), (253, 372), 
    (246, 355), (259, 330), (288, 338), (304, 331), (290, 310), 
    (269, 313), (282, 321), (243, 327), (230, 327)
]



def main():
    im = Image.open("terrain.png")
    pixels = im.load()
    for x, y in coords:
        pixels[x, y] = (0, 0, 0)  
        pixels[x+1, y] = (0, 0, 0)  
        pixels[x-1, y] = (0, 0, 0)  
        pixels[x, y+1] = (0, 0, 0)  
        pixels[x, y-1] = (0, 0, 0)  
        pixels[x+1, y+1] = (0, 0, 0)  
        pixels[x-1, y-1] = (0, 0, 0)  
        pixels[x+1, y-1] = (0, 0, 0)  
        pixels[x-1, y+1] = (0, 0, 0)

    im.save("modified.png")
    im.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    
    main()