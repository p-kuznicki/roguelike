import math

class Sight():
	def __init__(self, rays_density = 12, sight_range = 6):
		D = rays_density 	# number of rays in a quadrant
		SR = sight_range
		self.degrees = 90 / D
		rays=[]
		for i in range(D+1):
			tan = math.tan(i*(math.pi*self.degrees/180))	
			max_y = SR / math.sqrt(1 + tan*tan)
			max_x = max_y*tan
			rays.append([])
			for x in range(1,int(max_x)):
				y = int(x/tan)
				rays[i].append([y, x])
			for y in range(1, int(max_y)):
				x = int(y*tan)
				rays[i].append([y, x])

			rays[i] = sorted(rays[i], key=lambda z: sum(z))

		rays1 = []
		rays2 = []
		rays3 = []

		for ray in rays:
			rays1.append([[-r[0], r[1]] for r in ray])
			rays2.append([[r[0], -r[1]] for r in ray])
			rays3.append([[-r[0], -r[1]] for r in ray])

		rays = rays + rays1 + rays2 + rays3
		
		self.rays = rays
