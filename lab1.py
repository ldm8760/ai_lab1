from random import Random
import sys
from PIL import Image, ImageColor
import heapq

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

def chebyshev_distance(current_pos: tuple[int, int], next_goal: tuple[int, int]):
    return max(abs(current_pos[0] - next_goal[0]), abs(current_pos[1] - next_goal[1]))

def position_cost(pixels, pos: tuple[int, int]) -> int:
    rgb = pixels[pos[0], pos[1]]
    cost = traversal_scores.get(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper())
    return cost

def heuristic(current: tuple[int, int], goal: tuple[int, int]) -> float:
    optimal_pixel = 25.9
    return chebyshev_distance(current, goal) * optimal_pixel

def reconstruct_path(came_from: dict, current: tuple[int, int]) -> list:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star_search(start: tuple[int, int], goal: tuple[int, int], pixels) -> list:
    pq = []
    heapq.heappush(pq, (heuristic(start, goal), start))

    g_score: dict[tuple[int, int], int] = {start: 0}
    came_from: dict[tuple[int, int], tuple[int, int]] = {}

    while pq:
        _, current = heapq.heappop(pq)
        
        if current == goal:
            return reconstruct_path(came_from, current)

        for dx, dy in king_moves:
            neighbor = (current[0] + dx, current[1] + dy)

            tentative_g = g_score[current] + position_cost(pixels, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score, neighbor))

    return []

visited = [(230, 327)]
terrain = sys.argv[1]
elevation = sys.argv[2]
coords_file = sys.argv[3]
output_file = sys.argv[4]
points_to_visit = []
with open(f"{coords_file}", "r") as f:
    for line in f:
        x, y = map(int, line.split())
        points_to_visit.append((x, y))  

def main():
    im = Image.open(f"{terrain}")
    # im = Image.open("terrain.png")
    im = im.convert("RGB")
    pixels = im.load()

    total_path = []
    for i in range(len(points_to_visit) - 1):
        path = a_star_search(points_to_visit[i], points_to_visit[i + 1], pixels)

        for position in path:
            total_path.append(position)         

    print(len(total_path) * pixel_area)

    for x, y in total_path:
        pixels[x, y] = ImageColor.getcolor("#a146dd", "RGB")

    im.save(f"{output_file}")
    # im.save(f"modified.png")
    im.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    main()