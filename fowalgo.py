import math

N = 6	#number of rays
R = 6
   #range of line of sight

degrees = 90 / N 	

def angle_to_tangens(degrees):
	angle_in_radians = math.pi*degrees/180
	tangens = math.tan(angle_in_radians)
	return tangens

tan_set = []
for i in range(N+1):
	tan_set.append(angle_to_tangens(degrees*i))
print(tan_set)

rays = []

for r, tan in enumerate(tan_set):
	y = R / math.sqrt(1 + tan*tan)
	x = y*tan
	#print(int(x),int(y), "a to ich wspołrzedne cząstokoe")
	rays.append([])
	for px in range(int(x)):
		py = int(px/tan)
		rays[r].append([py, px])
	for py in range(int(y)):
		px = int(py*tan)
		rays[r].append([py, px])
	rays[r] = sorted(rays[r], key=lambda x: sum(x))
#	print(rays[r])

lists_to_remove = [[0, 0], [1, 0], [0, 1], [1, 1]]

# Filter out the unwanted lists
rays = [[r for r in ray if r not in lists_to_remove] for ray in rays]


rays1 = []
rays2 = []
rays3 = []


for ray in rays:
	ray1 = [[-r[0], r[1]] for r in ray]
	rays1.append(ray1)
for ray in rays:
	ray1 = [[r[0], -r[1]] for r in ray]
	rays2.append(ray1)
for ray in rays:
	ray1 = [[-r[0], -r[1]] for r in ray]
	rays3.append(ray1)

rays = rays + rays1 + rays2 + rays3



