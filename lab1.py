from random import Random
import sys
from PIL import Image
from queue import PriorityQueue

def test_image():
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

pixel_long = 10.29 # meters, east/west
pixel_lat = 7.55 # meters, north/south
pixel_area = pixel_long * pixel_lat

def calculate_traversal_score(color: str) -> int: # less is more
    pixel_speed = land_types[color]
    if pixel_speed != 0:
        score = pixel_area / pixel_speed
    else:
        score = float("inf")
    return round(score, 2)

# format of hard coded colors is in {color: estimated meters per second}
land_types: dict[str, float] = {
    "#F89412": 3,    # open_land
    "#FFC000": 2.2,  # rough_meadow
    "#FFFFFF": 2.7,  # easy_movement_forest
    "#02D03C": 2.3,  # slow_run_forest
    "#028828": 1.6,  # walk_forest
    "#054918": 0,    # impassible_vegetation
    "#0000FF": 1,    # lake_swamp_marsh
    "#473303": 3,    # paved_road
    "#000000": 3,    # footpath
    "#CD0065": 0     # out_of_bounds
}

traversal_scores: dict[str, float] = {
    "#F89412": calculate_traversal_score("#F89412"),  # open_land
    "#FFC000": calculate_traversal_score("#FFC000"),  # rough_meadow
    "#FFFFFF": calculate_traversal_score("#FFFFFF"),  # easy_movement_forest
    "#02D03C": calculate_traversal_score("#02D03C"),  # slow_run_forest
    "#028828": calculate_traversal_score("#028828"),  # walk_forest
    "#054918": calculate_traversal_score("#054918"),  # impassible_vegetation
    "#0000FF": calculate_traversal_score("#0000FF"),  # lake_swamp_marsh
    "#473303": calculate_traversal_score("#473303"),  # paved_road
    "#000000": calculate_traversal_score("#000000"),  # footpath
    "#CD0065": calculate_traversal_score("#CD0065")   # out_of_bounds
}

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

king_moves = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1), (1, 0), (1, 1)
]

pos_x = 230
pos_y = 327
visited = [(pos_x, pos_y)]
optimal_pixel = 25.9

def chebyshev_distance(current_pos: tuple[int, int], next_goal: tuple[int, int]):
    distance = max(abs(current_pos[0] - next_goal[0]), abs(current_pos[1] - next_goal[1]))
    return distance

def fn_score(g, h):
    return h + g



def pixel_calc(pixel: tuple[int, int]) -> int:
    t = traversal_scores.get(f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}".upper())
    return t

def heuristic(current: tuple[int, int], goal: tuple[int, int]):
    return chebyshev_distance(current, goal) * optimal_pixel

# this is incorrect for now
def gn_score(current: tuple[int, int], start: tuple[int, int], pixel):
    return chebyshev_distance(current, start) * pixel_calc(pixel[current[0], current[1]])




def a_star_test(start: tuple[int, int], goal: tuple[int, int], pixels):
    current = start
    pq = PriorityQueue(100)
    pq.put(current)
    vis = set(current)

    g = gn_score(current, start, pixels)
    h = heuristic(current, goal)
    f = fn_score(g, h)

    # while pq is not None:
    for i in range(5):
        for dx, dy in king_moves:
            neighbor_x = current[0] + dx
            neighbor_y = current[1] + dy
            if (neighbor_x, neighbor_y) in vis:
                continue
            gn = gn_score((neighbor_x, neighbor_y), start, pixels)
            print(f"pos_x: {neighbor_x}, pos_y: {neighbor_y}")
            print(f"g(n): {gn}")
            hn = heuristic((neighbor_x, neighbor_y), goal)
            print(f"h(n): {hn}")
            fn = fn_score(gn, hn)
            print(f"f(n): {fn}")
            print("-----")

    if current == goal:
        visited.append(coords[len(visited)])

def main():
    im = Image.open("terrain.png")
    im = im.convert("RGB")
    pixels = im.load()

    # print(coords[0], coords[1])
    a_star_test(coords[0], coords[1], pixels)

    im.save("terrain.png")
    # im.show()   

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    
    main()