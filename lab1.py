import sys
from PIL import Image, ImageColor
import heapq
from math import sqrt, pow

pixel_long = 10.29 # meters, east/west
pixel_lat = 7.55 # meters, north/south

traversal_scores: dict[str, float] = {
    "#F89412": 1,  # open_land
    "#FFC000": 1.36,  # rough_meadow
    "#FFFFFF": 1.11,  # easy_movement_forest
    "#02D03C": 1.30,  # slow_run_forest
    "#028828": 1.86,  # walk_forest
    "#054918": float("inf"),  # impassible_vegetation
    "#0000FF": 3,  # lake_swamp_marsh
    "#473303": 1,  # paved_road
    "#000000": 1,  # footpath
    "#CD0065": float("inf")   # out_of_bounds
}

king_moves = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1), (1, 0), (1, 1)
]

def position_cost(pixels, current: tuple[int, int], goal: tuple[int, int]) -> float:
    distance = heuristic(current, goal)
    rgb = pixels[goal[0], goal[1]]
    cost = traversal_scores.get(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper())
    return distance * cost

def heuristic(current: tuple[int, int], goal: tuple[int, int]) -> float:
    xmove = abs(current[0] - goal[0]) * pixel_long
    ymove = abs(current[1] - goal[1]) * pixel_lat
    zmove = abs(elevation_matrix[current[1]][current[0]] - elevation_matrix[goal[1]][goal[0]])
    total_cost = sqrt(pow(xmove, 2) + pow(ymove, 2) + pow(zmove, 2))
    return total_cost

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
            neighbor_x = current[0] + dx
            neighbor_y = current[1] + dy

            if 0 <= neighbor_x < 395 and 0 <= neighbor_y < 500:
                neighbor = (neighbor_x, neighbor_y)
            else:
                continue

            tentative_g = g_score[current] + position_cost(pixels, current, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score, neighbor))

    return []

visited = [(230, 327)]
terrain = sys.argv[1]
elevation = sys.argv[2]
elevation_matrix = []
with open(f"{elevation}", "r") as f:
    for line in f:
        across = [float(value) for value in line.split()[:-5]]
        elevation_matrix.append(across)

coords_file = sys.argv[3]
output_file = sys.argv[4]
points_to_visit = []
with open(f"{coords_file}", "r") as f:
    for line in f:
        x, y = map(int, line.split())
        points_to_visit.append((x, y))  

def main():
    im = Image.open(f"{terrain}")
    im = im.convert("RGB")
    pixels = im.load()

    total_path = []
    for i in range(len(points_to_visit) - 1):
        path = a_star_search(points_to_visit[i], points_to_visit[i + 1], pixels)

        for position in path:
            total_path.append(position)         

    total_distance = 0
    for i in range(len(total_path) - 1):
        dx = (total_path[i][0] - total_path[i + 1][0]) * pixel_long
        dy = (total_path[i][1] - total_path[i + 1][1]) * pixel_lat

        z1 = elevation_matrix[total_path[i][1]][total_path[i][0]]
        z2 = elevation_matrix[total_path[i + 1][1]][total_path[i + 1][0]]

        dz = z1 - z2
        total_distance += (dx**2 + dy**2 + dz**2) ** 0.5

    print(total_distance)

    for x, y in total_path:
        pixels[x, y] = ImageColor.getcolor("#a146dd", "RGB")

    im.save(f"{output_file}")
    im.show()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError(f"Four arguments required, got {len(sys.argv) - 1}")
    main()