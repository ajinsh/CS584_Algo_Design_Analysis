from Stack import Stack
from math import atan2, sqrt
import numpy as np
import matplotlib.pyplot as plt
# from decimal import *
import time
import random

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


# def euclidean_distance(points, ref_point):
# 	euclidean_dist = []
# 	print('ref_point',ref_point)
# 	print('points',points)
# 	for each in points:
# 		eucl_dist = (ref_point[0]-each[0])**2 -(ref_point[1]-each[1])**2
# 		euclidean_dist.append(eucl_dist)
# 	print('euclidean_dist',euclidean_dist)
# 	return euclidean_dist


def polar_angle(points):
	polar_angle = []

	for each in points:
		dy = each[1] - P0[1]
		dx = each[0] - P0[0]
		polar_angle.append(atan2(dy, dx)+90.00003218077504)

	return polar_angle


def sort_by_polar_angle(points):



	p = polar_angle(points)
	polar_angle_arr = np.asarray(p)
	print("polar_angle_arr",polar_angle_arr)


	vals1, idx_start1, count1 = np.unique(polar_angle_arr, return_counts=True,
	                                return_index=True)

	idx_sorted_pang = np.argsort(polar_angle_arr)
	print(idx_sorted_pang) 

	sorted_polar_angle_arr = polar_angle_arr[idx_sorted_pang] 
	print('sorted_polar_angle_arr',sorted_polar_angle_arr)
	vals, idx_start, count = np.unique(sorted_polar_angle_arr, return_counts=True,
	                                return_index=True)


	# print("vals",vals)
	# print("vals where count =1",vals[count == 1])
	# print("count>1",count>1)


	# print("vals",vals)
	# print("idx_start",idx_start)
	# print("count",count)
	# sets of indices
	res = np.split(idx_sorted_pang, idx_start[1:])
	#filter them with respect to their size, keeping only items occurring more than once
	print("res",res)
	print(type(res))


	final_points =[]
	for each in res:
		# print("len(each)",len(each))
		if len(each) > 1:
			i = each.tolist()
			# print(i)
			check_points = []
			for j in i:
				check_points.append(points[j])
			# print('check_points',check_points)
			check_points_arr = np.asarray(check_points)
			# print('check_points_arr',check_points_arr)
			print(check_points_arr.shape)
			print(np.amax(check_points_arr,axis=0))
			
			far_x = np.amax(check_points_arr,axis=0)[0]
			far_y = np.amax(check_points_arr,axis=0)[1]
			final_points.append((far_x,far_y))
		elif len(each) == 1:
			# print('points[each.tolist[0]]',each.tolist()[0])
			final_points.append(points[each.tolist()[0]])

	# print('final_points',final_points)
	return final_points

	# print("np.asscalar(each)",np.asscalar(each))
# points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]


def cross_product(p0,p1,p2):
	# print((p1[0]-p0[0])*(p2[1]-p0[1])-(p2[0]-p0[0])*(p1[1]-p0[1]))

	return ((p1[0]-p0[0])*(p2[1]-p0[1])-(p2[0]-p0[0])*(p1[1]-p0[1]))
	# print((p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0]))

	# return ((p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0]))


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


# def create_random_points_circle(n):



	

def show_convex_hull(points,hull_points):
	for each in points:
		# print('each',each)
		plt.plot(each[0],each[1],'o-')


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


def graham_scan():

	# choice_of_input = input("Enter choice of random point distribution:\n1. Random scatter 2. Circle")

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
	# 			break
	# 		except ValueError:
	# 			print("Enter integer value for input size")

	# 	points = create_random_points_circle(n)



	# points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
	# points =[(1,0),(0,-1),(-1,0),(0,1)]
	points = [(-25,-99),(37,-100),(-80,4),(-83,11),(12,-28)]
	# points = read_points()

	

	global P0


	start = time.time()
	print('start time',start)
	P0 = point_with_min_y(points)

	sorted_points = sort_by_polar_angle(points)
	del sorted_points[0]
	print('P0',P0)


	s = Stack()
	s.push(P0)
	# print(sorted_points[0])
	s.push(sorted_points[0])
	s.push(sorted_points[1])
	print('sorted_points before',sorted_points)
	sorted_points = sorted_points[2:]
	print('sorted_points after',sorted_points)
	print('s.print_all()',s.print_all())
	# print(s.next_to_top())
	# print(s.top())
	# print(sorted_points[0])
	# print(cross_product(s.next_to_top(),s.top(),sorted_points[0]))
	for i in range(len(sorted_points)):
		# print(i)
		while cross_product(s.next_to_top(),s.top(),sorted_points[i]) <= 0:
			s.pop()
			print("Stack now {} for i:{}".format(s.print_all(),i))
		s.push(sorted_points[i])

	print("Calling stack")
	print(s.print_all())

	end = time.time()
	print('end time',end)
	print("Total executuion time: {}".format(end-start))

	show_convex_hull(points,s.print_all())




if __name__ == '__main__':
	graham_scan()
	# read_points()
	# cross_product((3,1),(4,4),(1,2))
	# cross_product((1,1),(2,2),(1,3))