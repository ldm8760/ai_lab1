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


pos_x = 230
pos_y = 327
visited = [(pos_x, pos_y)]
optimal_pixel = 25.9

def king_random_move(current_pixel: tuple[int, int]) -> tuple[int, int]:
    new_pos_x = current_pixel[0] + zero_one_randomizer()
    new_pos_y = current_pixel[1] + zero_one_randomizer()
    return tuple(new_pos_x, new_pos_y)


def chebyshev_distance(current_pos: tuple[int, int], next_goal: tuple[int, int]):
    distance = max(abs(current_pos[0] - next_goal[0]), abs(current_pos[1] - next_goal[1]))
    return distance

def heuristic(start, goal):
    return chebyshev_distance(start, goal) * optimal_pixel 

# fix this its broken for whatever reason
def zero_one_randomizer() -> int:
    return Random.randint(-1, 1)

def a_star_test(start, goal):
    current = start
    pq = PriorityQueue(8)
    pq.put(current)

    for i in range(20):
        next_pixel = king_random_move(current)
        print(f"estimated distance from goal: {heuristic(next_pixel)}")

    if current == goal:
        visited.append(coords[len(visited)])

def main():
    im = Image.open("terrain.png")
    pixels = im.load()

    for key, value in traversal_scores.items():
        print(f"{key}: {value}")

    for i in range(len(coords) - 1):
        print(f"coord {i} and {i + 1}: {chebyshev_distance(coords[i], coords[i + 1])}")

    a_star_test(coords[i], coords[i + 1])

    im.save("modified.png")
    im.show()   

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    
    main()