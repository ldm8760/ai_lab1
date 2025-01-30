import sys
from PIL import Image

open_land = "#F89412"  # (248, 148, 18)
rough_meadow = "#FFC000"  # (255, 192, 0)
easy_movement_forest = "#FFFFFF"  # (255, 255, 255)
slow_run_forest = "#02D03C"  # (2, 208, 60)
walk_forest = "#028828"  # (2, 136, 40)
impassible_vegetation = "#054918"  # (5, 73, 24)
lake_swamp_marsh = "#0000FF"  # (0, 0, 255)
paved_road = "#473303"  # (71, 51, 3)
footpath = "#000000"  # (0, 0, 0)
out_of_bounds = "#CD0065"  # (205, 0, 101)


terrain = sys.argv[1]
elevation = sys.argv[2]
points_to_visit = sys.argv[3]
output_file = sys.argv[4]


def main():
    with Image.open(f"{terrain}") as im:
        im.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    
    main()