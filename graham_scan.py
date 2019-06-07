"""
Author: Ajinkya Shinde
"""
# Importing the necessary packages
from Stack import Stack
from math import atan2, sqrt, pi, cos, sin
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
import csv

def point_with_min_y(points):
	"""Returns the point with minimum y co-ordinate and the 
	leftmost incase of a tie from a set of points 	
	
	Input: points (array-type)

	Output: P0(tuple)
	"""

	min_idx = None

	for a,coord in enumerate(points):

		if min_idx == None:
			min_idx = a
			P0_Y = coord[1]
			P0_X = coord[0]
		elif coord[1] < P0_Y:
			# look for the point with lowest y co-ordinate
			min_idx = a
			P0_X = coord[0]
			P0_Y = coord[1]
		elif (coord[1] == P0_Y) & (coord[0] < P0_X):
			# In-case of tie with lowest y co-ordinate
			# take one which is leftmost or lowest x 
			# co-ordinate
			min_idx = a
			P0_X = coord[0]
			P0_Y = coord[1]


	return (P0_X,P0_Y)


def euclidean_distance(points, ref_point):
	"""Returns euclidean distance for all set of points 

	Input: points (array-like) : set of points whose
	       euclidean distance needs to be found

	       ref_point (tuple-like) : point to be used as
	       reference for distance calculation

	Output: array object with euclidean distance for all the points
	        passed

	Note: This function is used by sort_by_polar_angle - the original
          version for the sort by polar angle logic
	"""	

	euclidean_dist = []
	for each in points:
		eucl_dist = sqrt((ref_point[0]-each[0])**2 +(ref_point[1]-each[1])**2)
		euclidean_dist.append(eucl_dist)
	return np.asarray(euclidean_dist)



def euclidean_distance_v2(point, ref_point):
	# print('Calculating dist between',point,' and ',ref_point,end='')
	# print(sqrt((ref_point[0]-point[0])**2 +(ref_point[1]-point[1])**2))
	return sqrt((ref_point[0]-point[0])**2 +(ref_point[1]-point[1])**2)
	
	


def polar_angle(points):
	"""Returns list of polar angle between -pi and pi calculated
	   with respect to P0 - point with lowest x and y co-ordinate

	Input: points(array-like) : set of points whose polar angle
	needs to be calculated with respect to ref point

	Output: polar angle array
	"""

	polar_angle = []

	for each in points:
		dy = each[1] - P0[1]
		dx = each[0] - P0[0]
		polar_angle.append(atan2(dy, dx))

	return polar_angle



def sort_by_polar_angle_v2(pts):
	"""Returns sorted list of points with polar angle sorted in
	counterclockwise direction. For points with same polar angle 
	the farthest point

	Input: pts(array-like) : set of points for sorting by polar angle

	Output: sorted order of input array of points

	"""

	### make a copy of points array to avoid corruption
	### of original points array
	copy_pts = []
	for each in pts:
		if each not in copy_pts:
			copy_pts.append(each)

	P0_idx = copy_pts.index(P0)
	del copy_pts[P0_idx]


	# Call polar_angle function to calculate polar angle
	# of points with respect to P0
	p =polar_angle(copy_pts)
	

	#########For sorting polar angle array ######
	# Once we get the polar angle array, we use numpy.argsort
	# to get the indices of sorted polar angle array
	# using the indices serves two purpose
	# 1. Sort polar angle array
	# 2. Sort list of points array 
	# 3. Develop logic to take farthest point in case of
	#    collinear

	np_p = np.asarray(p)	
	sorted_idx = np.argsort(np_p,kind='mergesort')


	# Do steps 1. and 2. of above commented logic
	sorted_p = []
	sorted_pts = []
	for each in sorted_idx:
		sorted_p.append(p[each])
		sorted_pts.append(copy_pts[each])

	# Code for step 3.
	check_dict = {}
	for i in range(len(sorted_p)-1):
		for j in range(i+1,len(sorted_p)):
			if sorted_p[j] == sorted_p[i]:
				if sorted_p[i] not in check_dict:
					temp_list=[]
					temp_list.append(sorted_pts[i])
					check_dict[sorted_p[i]]=temp_list
				temp_list2 = []
				temp_list2 = check_dict[sorted_p[i]]
				if sorted_pts[j] not in temp_list2:
					temp_list2.append(sorted_pts[j])
					check_dict[sorted_p[i]]=temp_list2
				if sorted_pts[j] in temp_list2:
					break
			else:
				break


	for dict_val in check_dict.values():

		farthest_pt = dict_val[0]
		max_dist = euclidean_distance_v2(farthest_pt,P0)

		for each in dict_val[1:]:

			if euclidean_distance_v2(each,P0) > max_dist:
				sorted_pts = [x for x in sorted_pts if x!=farthest_pt]
				max_dist = euclidean_distance_v2(each,P0)
				farthest_pt = each
			if euclidean_distance_v2(each,P0) < max_dist:
				sorted_pts = [x for x in sorted_pts if x!=each]


	return sorted_pts





def sort_by_polar_angle(points):
	"""Returns sorted order of points array. 
	This is initial version of sort_by_polar_angle function.

	Input: points(array-like) : set of points to be sorted with
	respect to P0

	Output: sorted array of remaining points
	"""

	# Call polar_angle function to calculate polar angle
	# of points with respect to P0

	p = polar_angle(points)
	polar_angle_arr = np.asarray(p)


	vals1, idx_start1, count1 = np.unique(polar_angle_arr, return_counts=True,
	                                return_index=True)

	idx_sorted_pang = np.argsort(polar_angle_arr)

	sorted_polar_angle_arr = polar_angle_arr[idx_sorted_pang] 
	vals, idx_start, count = np.unique(sorted_polar_angle_arr, return_counts=True,
	                                return_index=True)


	res = np.split(idx_sorted_pang, idx_start[1:])

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
			
			max_far_idx = np.argmax(euclidean_distance(check_points,P0))
			


			final_points.append(check_points[max_far_idx])
		elif len(each) == 1:
			
			final_points.append(points[each.tolist()[0]])



	return final_points




def cross_product(p0,p1,p2):
	"""Returns the cross product of points of p0,p1 and p2.
	The value returned is +ve, -ve or 0
	"""
	return (((p1[0]-p0[0])*(p2[1]-p0[1]))-((p2[0]-p0[0])*(p1[1]-p0[1])))


def read_points():
	"""
	Work In Progress file to read points from text file
	"""
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
	"""Returns random points for input choice 1 from menu screen

	Input:n(int) : size of input

	Output: points array
	"""

	return [(random.randint(0,n),random.randint(0,n)) for i in range(n)]



def points_on_circumference(center=(0, 0), r=50, n=100):
	""" Returns points around the boundary of circle with random distribution
	 	It is called when choice of input entered is 2
	"""
	return [
        (
            center[0]+(cos(2 * pi / n * x) * r),  
            center[1] + (sin(2 * pi / n * x) * r) 

        ) for x in range(0, n + 1)]


def create_export_files(n,input_choice,timing,min_hull_per):
	"""Creates folder analysis if not exists in current directory and creates 
	results.csv file

	Input: n(int): size of input
	       input_choice(int): choice of input from menu
	       timing(decimal): Timing in sec of algo
	       min_hull_per(int): percentage of hull points from n

	Output: Appends results of execution to the csv file
	"""


	exists = os.path.isdir('analysis')
	if exists:
		f = open('analysis/results.csv','a',newline='')
		results = csv.writer(f)
	else:
		os.mkdir('analysis')
		f = open('analysis/results.csv','w',newline='')
		results = csv.writer(f)
		results.writerow(['Algo','Size of Input','Min. Hull Pts Per','Type of Input','Timing'])


	results.writerow(['Graham Scan',n,min_hull_per,input_choice,timing])


def points_on_circumference_with_per(center=(0, 0), r=50, n=100, per = 50):
	"""Returns points around boundary of circle with random points distributed
	 inside circle. It is called when choice of input entered is 3

	 Input: center(tuple) : co-ordinates for center of circle
	        r(int) : input for radius of circle
	        n(int) : size of input
	        per(int) : percentage of points of n that should be on boundary

	Output : points array
	"""

	# circum_cnt is actual points on cicumference as a percentage of total 
	# random points(n) = Percentage_of_Total_Points * n / 100
	circum_cnt = int(per*n/100)

	# random_cnt is points inside the circle = Total random points - Points on Circum
	random_cnt = n - circum_cnt

	# Append points on circumference
	final_pts = [
		(
			center[0]+(cos(2 * pi / circum_cnt * x) * r),  
			center[1] + (sin(2 * pi / circum_cnt * x) * r) 
		) for x in range(0, circum_cnt + 1)]




	# Generate random points inside circle
	# random points inside circle should have atleast 5 radius to be visible enough
	for i in range(1,random_cnt+1):
		final_pts.append( (center[0]+  cos(2 * pi / circum_cnt * i) * random.randint(1,r-20),
							center[1] + sin(2 * pi / circum_cnt * i) * random.randint(1,r-20)))


	return final_pts





def show_convex_hull(points, input_choice, timing,percent_pts,size,hull_points = None):
	"""Returns plot with parameters from menu screen and saves the plot in /plots
	directory
	"""
	exists = os.path.isdir('plots')
	if not exists:        
		os.mkdir('plots')


	for each in points:
		plt.plot(each[0],each[1],'o-')

	if hull_points is not None:
		hull_pt_list = []
		for each in hull_points:
			hull_pt_list.append(list(each))

		hull_pt_arr = np.asarray(hull_pt_list)
		# print(hull_pt_arr)
		plt.plot(hull_pt_arr[:,0],hull_pt_arr[:,1],'k-')
		first_coord = hull_pt_arr[0,:].reshape(1,2)
		last_coord = hull_pt_arr[len(hull_pt_arr)-1,:].reshape(1,2)

		last_coord_arr = np.append(first_coord, last_coord, axis = 0)
		plt.plot(last_coord_arr[:,0],last_coord_arr[:,1],'k-')
		plt.title(label = 'For input : '+input_choice+percent_pts+' time taken = '+str(timing)+' s\n'+'N='+str(size))
	
	plt.savefig('plots/'+'Graham_Scan_'+str(input_choice)+str(percent_pts)+'_N='+str(size)+'.png')
	plt.show()



def graham_scan():
	### Menu Screen for Program Starts
	choice_of_input = input("Enter choice of random point distribution:\n1. Random scatter\n2. Circle\n3. Minimal Points on Circle\n")

	if choice_of_input == "1":

		while True:
			try:
				input_size = input("Enter the input size")
				n=int(input_size)
				per_min_pt = ''
				break
			except ValueError:
				print("Enter integer value for input size")

		points = create_random_points(n)

	elif choice_of_input == "2":

		while True:
			try:
				input_size = input("Enter the input size")
				n=int(input_size)
				per_min_pt = ''
				radius = input("Enter the radius")
				r = int(radius)
				center_str = input("Enter comma seperated x and y co-ordinates")
				center_str = center_str.split(",")
				center_x = int(center_str[0])
				center_y = int(center_str[1])		
				break
			except ValueError:
				print("Enter integer value for input size/radius")

		points = points_on_circumference((center_x,center_y),r, n)

	elif choice_of_input == "3":

		while True:
			try:
				input_size = input("Enter the input size")
				n=int(input_size)
				per_min_pt = input("Enter percentage of points on hull")
				per_min_pt = float(per_min_pt)
				radius = input("Enter the radius")
				r = int(radius)
				center_str = input("Enter comma seperated x and y co-ordinates")
				center_str = center_str.split(",")
				center_x = int(center_str[0])
				center_y = int(center_str[1])		
				break

			except ValueError:
				print("Enter integer value for input size/radius")

		points = points_on_circumference_with_per((center_x,center_y),r, n, per_min_pt)

	### Menu Screen for Program Ends
	

	# Set P0 to be global so that it can be access by other functions
	global P0


	# Find P0 with minimum y co-ordinate
	P0 = point_with_min_y(points)

	# Begin tracking the execution time
	start = time.time()
	


	# Sort the remaining points in points array by polar angle
	# in counterclockwise order around P0
	sorted_points = sort_by_polar_angle_v2(points)


	# Inital version of sort by polar angle - faster than the current one
	# sorted_points2 = sort_by_polar_angle(points)
	
	# Create an empty stack
	s = Stack()
	
	# Push P0, two points from sorted array on stack
	s.push(P0)
	s.push(sorted_points[0])
	s.push(sorted_points[1])


	# Update the sorted array from 3rd element
	sorted_points = sorted_points[2:]



	# Find the boundary using cross product
	for i in range(len(sorted_points)):
		while cross_product(s.next_to_top(),s.top(),sorted_points[i]) < 0:
			s.pop()
		s.push(sorted_points[i])



	end = time.time()

	#helper dictionary for generating plots
	input_choice_title = {1:'Random Scatter',2:'Circle',3:'Circle with min. hull pts %'}


	##Call results function 
	show_convex_hull(points,input_choice_title[int(choice_of_input)],round((end-start),6),str(per_min_pt),n,s.print_all())

	create_export_files(n,input_choice_title[int(choice_of_input)],(end-start),str(per_min_pt))


if __name__ == '__main__':
	graham_scan()