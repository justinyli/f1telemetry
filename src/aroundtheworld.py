from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    r = 3960 # miles
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

races = [
    ('Bahrain', 26, 50),
    ('Saudi Arabia', 21, 39),
    ('Australia', -37, 144),
    ('Azerbaijan', 40, 49),
    ('Miami', 26, -80),
    ('Emilia Romagna', 44, 12),
    ('Monaco', 44, 7),
    ('Spain', 42, 2),
    ('Canada', 45, -74),
    ('Austria', 47, 15),
    ('Britain', 52, -1),
    ('Hungary', 47, 19),
    ('Belgium', 50, 6),
    ('Netherlands', 52, 5),
    ('Italy', 45, 9),
    ('Singapore', 1, 104),
    ('Japan', 35, 136),
    ('Qatar', 25, 51),
    ('United States', 30, -98),
    ('Mexico City', 19, -99),
    ('Sao Paulo', -24, -47),
    ('Las Vegas', 36, -115),
    ('Abu Dhabi', 24, 54)
]

# distances = []
# for j in races:
#     row = []
#     for l in races:
#         row.append(int(distance(j[1], j[2], l[1], l[2])))
#     distances.append(row)

# # Print the distances in the desired format
# for row in distances:
#     print("{" + ", ".join(str(distance) for distance in row) + "},")

dist = 0

for i in range(len(races) - 1):
    dist += int(distance(races[i][1], races[i][2], races[i+1][1], races[i+1][2]))
dist += int(distance(races[22][1], races[22][2], races[0][1], races[0][2]))
print(dist)