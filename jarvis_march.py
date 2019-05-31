from Stack import Stack
from math import atan2, sqrt, pi, cos, sin
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import operator

def point_with_min_y(points):
	min_idx = None

	for a,coord in enumerate(points):
		if min_idx == None:
			min_idx = a
			P0_Y = coord[1]
			P0_X = coord[0]
		elif coord[1] < P0_Y:
			min_idx = a
			P0_X = coord[0]
			P0_Y = coord[1]
		elif (coord[1] == P0_Y) & (coord[0] < P0_X):
			min_idx = a
			P0_X = coord[0]
			P0_Y = coord[1]


	return (P0_X,P0_Y)


def euclidean_distance(points, ref_point):
	euclidean_dist = []
	for each in points:
		eucl_dist = sqrt((ref_point[0]-each[0])**2 +(ref_point[1]-each[1])**2)
		euclidean_dist.append(eucl_dist)
	return np.asarray(euclidean_dist)


def polar_angle(points, ref_point):
	polar_angle = []

	for each in points:
		dy = each[1] - ref_point[1]
		dx = each[0] - ref_point[0]

		if atan2(dy, dx)*57.2958 <0:
			polar_angle.append(360+(atan2(dy, dx)*57.2958))
		else:
			polar_angle.append(atan2(dy, dx)*57.2958)

	return polar_angle


def sort_by_polar_angle(points, ref_point):

	print('points',points)
	print('ref_point',ref_point)

	p = polar_angle(points,ref_point)
	polar_angle_arr = np.asarray(p)

	print('polar_angle_arr',polar_angle_arr)
	vals1, idx_start1, count1 = np.unique(polar_angle_arr, return_counts=True,
	                                return_index=True)

	idx_sorted_pang = np.argsort(polar_angle_arr)

	sorted_polar_angle_arr = polar_angle_arr[idx_sorted_pang]
	print('sorted_polar_angle_arr',sorted_polar_angle_arr) 
	vals, idx_start, count = np.unique(sorted_polar_angle_arr, return_counts=True,
	                                return_index=True)


	res = np.split(idx_sorted_pang, idx_start[1:])
	print(res)
	#filter them with respect to their size, keeping only items occurring more than once
	final_points =[]
	for each in res:
		# print("len(each)",len(each))
		if len(each) > 1:
			i = each.tolist()
			check_points = []
			for j in i:
				check_points.append(points[j])
			check_points_arr = np.asarray(check_points)
			
			max_far_idx = np.argmax(euclidean_distance(check_points,ref_point))
			


			final_points.append(check_points[max_far_idx])
		elif len(each) == 1:
			
			final_points.append(points[each.tolist()[0]])

	print('final_points',final_points)
	return final_points



def cross_product(p0,p1,p2):
	print((p1[0]-p0[0])*(p2[1]-p0[1])-(p2[0]-p0[0])*(p1[1]-p0[1]))

	return (((p1[0]-p0[0])*(p2[1]-p0[1]))-((p2[0]-p0[0])*(p1[1]-p0[1])))
	



def read_points():
	points = []
	f = open(r'sample_points.txt')
	while True:
		nstr = f.readline()
		if len(nstr) == 0:
			break
		line = nstr.rstrip('\n').split(', ')
		# print(line)

		points.append((round(float(line[0]),3),round(float(line[1]),3))) 

	print(points)
	return points



def create_random_points(n):

	return [(random.randint(0,n),random.randint(0,n)) for i in range(n)]



def points_on_circumference(center=(0, 0), r=50, n=100):
    return [
        (
            center[0]+(cos(2 * pi / n * x) * r),  
            center[1] + (sin(2 * pi / n * x) * r) 

        ) for x in range(0, n + 1)]


def remove_points(points, *pt):
	for t in pt:
		for p in points:
			if t == p:
				points.remove(p)
	return points



def show_convex_hull(points,hull_points = None):
	for each in points:
		plt.plot(each[0],each[1],'o-')

	if hull_points is not None:
		hull_pt_list = []
		for each in hull_points:
			hull_pt_list.append(list(each))

		hull_pt_arr = np.asarray(hull_pt_list)

		plt.plot(hull_pt_arr[:,0],hull_pt_arr[:,1],'k-')
		first_coord = hull_pt_arr[0,:].reshape(1,2)
		last_coord = hull_pt_arr[len(hull_pt_arr)-1,:].reshape(1,2)

		last_coord_arr = np.append(first_coord, last_coord, axis = 0)
		plt.plot(last_coord_arr[:,0],last_coord_arr[:,1],'k-') 
	plt.show()


def jarvis_march():

	# choice_of_input = input("Enter choice of random point distribution:\n1. Random scatter\n2. Circle\n")

	# if choice_of_input == "1":

	# 	while True:
	# 		try:
	# 			input_size = input("Enter the input size")
	# 			n=int(input_size)
	# 			break
	# 		except ValueError:
	# 			print("Enter integer value for input size")

	# 	points = create_random_points(n)

	# elif choice_of_input == "2":

	# 	while True:
	# 		try:
	# 			input_size = input("Enter the input size")
	# 			n=int(input_size)
	# 			radius = input("Enter the radius")
	# 			r = int(radius)
	# 			center_str = input("Enter comma seperated x and y co-ordinates")
	# 			center_str = center_str.split(",")
	# 			center_x = int(center_str[0])
	# 			center_y = int(center_str[1])		
	# 			break
	# 		except ValueError:
	# 			print("Enter integer value for input size/radius")

	# 	points = points_on_circumference((center_x,center_y),r, n)

	points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
	# points =[(1,0),(0,-1),(-1,0),(0,1)]
	# points = [(-25,-99),(37,-100),(-80,4),(-83,11),(12,-28)]




	global P0
	print('Points array',points)

	start = time.time()
	print('start time',start)
	P0 = point_with_min_y(points)

	print('P0',P0)



	s = Stack()
	s.push(P0)


	ref_point = None

	while ref_point != P0:

		if ref_point is None:
			ref_point = P0
		
		p1_points = points.copy()
		p1_points = remove_points(p1_points, ref_point)

		ccw_dict = {}
		
		print('p1_points',p1_points)
		
		p2_points = p1_points.copy()
		
		for p1 in p1_points:
		
			print('Inside p1')
			print('p1',p1)
			p2_points = remove_points(p2_points,p1)
		
			print('p2_points',p2_points)
		
			ccw_dict[p1] = 0
			
			for p2 in p2_points:
		
				print('Inside p2')
				print('p2',p2)
				print('ref_point',ref_point)
				print('p1',p1)
				print('cross_product(ref_point,p2,p1)',cross_product(ref_point,p2,p1))
				if cross_product(ref_point,p2,p1) < 0:
					# print('cross_product(ref_point,p2,p1)',cross_product(ref_point,p2,p1))
					ccw_dict[p1]+=1

		

		print('ccw_dict',ccw_dict)
		# print('break')
		# print(max(ccw_dict.items(), key=operator.itemgetter(1))[0])
		ref_point = max(ccw_dict.items(), key=operator.itemgetter(1))[0]
		s.push(ref_point)
		break

	print('Printing hull')
	print('points',points)
	print(s.print_all())

	show_convex_hull(points,s.print_all())


if __name__ == '__main__':
	# jarvis_march()
	points = [(0, 3), (1, 1), (2, 2), (0, 0), (1, 2), (3, 3), (3, 1)]
	sort_by_polar_angle(points,(4,4))
	# cross_product((0,0),(0,3),(3,1))
	# cross_product((0,0),(0,4),(4,3))
	# show_convex_hull([(0,0),(0,4),(4,3)])
	# show_convex_hull([(0,0),(0,3),(1,1)])