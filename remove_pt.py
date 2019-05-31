# def remove_points(points,*pt):
#     check_pts = x
#     for p in pt:
#     	print(p)
#     	check_pts.remove(p)
#     return check_pts
def remove_points(points, *pt):
	# print(points)
	# print('pt',pt)
	for t in pt:
		for p in points:
			if t == p:
				points.remove(p)


x = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)] 
print('x',x)
test = x.copy()
remove_points(test,(0,0),(4,4))
print('test',test)
remove_points(test,(3,3))
print('test',test)
print('x',x)
