from math import atan2, sqrt, pi, cos, sin
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import operator
import os
import csv


global max_polar_angle

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



def cross_product(p0,p1,p2):
	# print((p2[0]-p0[0])*(p1[1]-p0[1])-(p1[0]-p0[0])*(p2[1]-p0[1]))

	return (((p2[0]-p0[0])*(p1[1]-p0[1]))-((p1[0]-p0[0])*(p2[1]-p0[1])))



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



def create_export_files(n,input_choice,timing,min_hull_per):
	exists = os.path.isfile('analysis/results_v2.csv')
	if exists:
		f = open('analysis/results_v2.csv','a',newline='')
		results = csv.writer(f)
	else:
		# os.mkdir('analysis')
		f = open('analysis/results_v2.csv','w',newline='')
		results = csv.writer(f)
		results.writerow(['Algo','Size of Input','Min. Hull Pts Per','Type of Input','Timing'])


	results.writerow(['Jarvis March',n,min_hull_per,input_choice,timing])




def create_random_points(n):

	return [(random.randint(0,n),random.randint(0,n)) for i in range(n)]



def points_on_circumference(center=(0, 0), r=50, n=100):
    return [
        (
            center[0]+(cos(2 * pi / n * x) * r),  
            center[1] + (sin(2 * pi / n * x) * r) 

        ) for x in range(0, n + 1)]


def points_on_circumference_with_per(center=(0, 0), r=50, n=100, per = 50):
	# circum_cnt is actual points on cicumference as a percentage of total 
	# random points(n) = Percentage_of_Total_Points * n / 100
	circum_cnt = int(per*n/100)

	# random_cnt is points inside the circle = Total random points - Points on Circum
	random_cnt = n - circum_cnt

	# print("random_cnt",random_cnt)
	# print("circum_cnt",circum_cnt)
	# Append points on circumference
	final_pts = [
		(
			center[0]+(cos(2 * pi / circum_cnt * x) * r),  
			center[1] + (sin(2 * pi / circum_cnt * x) * r) 
		) for x in range(0, circum_cnt + 1)]

	# Generate random points inside circle
	# random points inside circle should have atleast 5 radius to be visible enough

	for i in range(1,random_cnt+1):
		# print(i)
		# print('inside random pt Generate')
		final_pts.append( (center[0]+  cos(2 * pi / circum_cnt * i) * random.randint(1,r-20),
							center[1] + sin(2 * pi / circum_cnt * i) * random.randint(1,r-20)))


	return final_pts

def show_convex_hull(points, input_choice, timing,percent_pts,size,hull_points = None):
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
		plt.title(label = 'For input : '+input_choice+percent_pts+' time taken = '+str(timing)+' ms\n'+'N='+str(size))
	
	plt.savefig('plots/'+'Jarvis_March_'+str(input_choice)+str(percent_pts)+'_N='+str(size)+'.png')
	plt.show()



def jarvis_march():

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
				radius = input("Enter the radius")
				r = int(radius)
				center_str = input("Enter comma seperated x and y co-ordinates")
				center_str = center_str.split(",")
				center_x = int(center_str[0])
				center_y = int(center_str[1])
				per_min_pt = ''		
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
				per_min_pt = int(per_min_pt)
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



	# points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
	# points =[(1,0),(0,-1),(-1,0),(0,1)]
	# points = [(-25,-99),(37,-100),(-80,4),(-83,11),(12,-28)]
	print('Per MIN pt',per_min_pt)



	global P0
	print('Points array',points)

	start = time.time()
	print('start time',start)
	P0 = point_with_min_y(points)
	len_pts = len(points)
	print('P0',P0)


	pointOnHull = P0

	hullV = [None] * len_pts

	i=0
	while True:
		hullV[i] = pointOnHull
		endpoint = points[0]

		for j in range(1,n):
			if (endpoint[0]==pointOnHull[0] and endpoint[1]==pointOnHull[1]) or cross_product(pointOnHull,points[j],endpoint) < 0:
				endpoint = points[j]

		i = i + 1
		pointOnHull = endpoint

		if endpoint[0] == P0[0] and endpoint[1] == P0[1]:
			break

	for i in range(n):
			if hullV[-1] == None:
				del hullV[-1]

	print(hullV)


	end = time.time()
	print('end time',end)
	print("Total execution time: {}".format(end-start))



	# if input_choice == 1:
	# 	input_type = 'Random Scatter'
	# elif input_choice == 2:
	# 	input_type = 'Circle'
	# elif input_choice == 3:
	# 	input_type = 'Circle with min. hull pts'

	input_choice_title = {1:'Random Scatter',2:'Circle',3:'Circle with min. hull pts %'}

	show_convex_hull(points,input_choice_title[int(choice_of_input)],round(round((end-start),6)*1000,3),str(per_min_pt),n,hullV)

	create_export_files(n,input_choice_title[int(choice_of_input)],(end-start),str(per_min_pt))

if __name__ == '__main__':
	jarvis_march()
	# create_export_files(10,11,0.111)
	# cross_product((0,0),(4,4),(1,2))
