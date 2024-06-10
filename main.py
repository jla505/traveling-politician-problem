import geopy.distance
import networkx as nx
import numpy as np

# Step 1: Load State Capitals Data
capitals = {
    "Alabama": (32.377716, -86.300568),
    "Alaska": (58.301598, -134.420212),
    "Arizona": (33.448376, -112.096962),
    "Arkansas": (34.746613, -92.288986),
    "California": (38.576668, -121.493629),
    "Colorado": (39.739227, -104.984856),
    "Connecticut": (41.764046, -72.682198),
    "Delaware": (39.157307, -75.519722),
    "Florida": (30.438118, -84.281296),
    "Georgia": (33.749027, -84.388229),
    "Hawaii": (21.307442, -157.857376),
    "Idaho": (43.617775, -116.199722),
    "Illinois": (39.798363, -89.654961),
    "Indiana": (39.768623, -86.162643),
    "Iowa": (41.591087, -93.603729),
    "Kansas": (39.048191, -95.677956),
    "Kentucky": (38.186722, -84.875374),
    "Louisiana": (30.457069, -91.187393),
    "Maine": (44.307167, -69.781693),
    "Maryland": (38.978764, -76.490936),
    "Massachusetts": (42.358162, -71.063698),
    "Michigan": (42.733635, -84.555328),
    "Minnesota": (44.955097, -93.102211),
    "Mississippi": (32.303848, -90.182106),
    "Missouri": (38.579201, -92.172935),
    "Montana": (46.585709, -112.018417),
    "Nebraska": (40.808075, -96.699654),
    "Nevada": (39.163914, -119.766121),
    "New Hampshire": (43.206898, -71.537994),
    "New Jersey": (40.220596, -74.769913),
    "New Mexico": (35.68224, -105.939728),
    "New York": (42.652843, -73.757874),
    "North Carolina": (35.78043, -78.639099),
    "North Dakota": (46.82085, -100.783318),
    "Ohio": (39.961346, -82.999069),
    "Oklahoma": (35.492207, -97.503342),
    "Oregon": (44.938461, -123.030403),
    "Pennsylvania": (40.264378, -76.883598),
    "Rhode Island": (41.830914, -71.414963),
    "South Carolina": (34.000343, -81.033211),
    "South Dakota": (44.367031, -100.346405),
    "Tennessee": (36.16581, -86.784241),
    "Texas": (30.27467, -97.740349),
    "Utah": (40.777477, -111.888237),
    "Vermont": (44.262436, -72.580536),
    "Virginia": (37.538857, -77.43364),
    "Washington": (47.035805, -122.905014),
    "West Virginia": (38.336246, -81.612328),
    "Wisconsin": (43.074684, -89.384445),
    "Wyoming": (41.140259, -104.820236),
    "Washington, DC": (38.89511, -77.03637),
}

# Step 2: Calculate Distance Matrix
def calculate_distance_matrix(capitals):
    capitals_list = list(capitals.keys())
    n = len(capitals_list)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                coords_1 = capitals[capitals_list[i]]
                coords_2 = capitals[capitals_list[j]]
                distance_matrix[i, j] = geopy.distance.geodesic(coords_1, coords_2).miles
    
    return distance_matrix, capitals_list

distance_matrix, capitals_list = calculate_distance_matrix(capitals)

# Step 3: Solve TSP using NetworkX
def solve_tsp(distance_matrix):
    G = nx.complete_graph(len(distance_matrix), create_using=nx.DiGraph)
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix)):
            if i != j:
                G[i][j]['weight'] = distance_matrix[i][j]
    
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=False)
    return tsp_path

tsp_path = solve_tsp(distance_matrix)

# Step 4: Adjust to start in Iowa and end in Washington, DC
def adjust_path(tsp_path, capitals_list):
    start_index = capitals_list.index("Iowa")
    end_index = capitals_list.index("Washington, DC")
    
    # Find the position of start and end in the tsp_path
    start_pos = tsp_path.index(start_index)
    end_pos = tsp_path.index(end_index)
    
    # Rotate the path to start from Iowa
    adjusted_path = tsp_path[start_pos:] + tsp_path[:start_pos]
    
    # Ensure the path ends at Washington, DC
    if adjusted_path[-1] != end_index:
        adjusted_path = adjusted_path[:-1] + [end_index]
    
    return adjusted_path

adjusted_path = adjust_path(tsp_path, capitals_list)
route = [capitals_list[i] for i in adjusted_path]

# Print the route
print("Most efficient route:")
for city in route:
    print(city)
