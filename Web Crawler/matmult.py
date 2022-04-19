import math
def mult_scalar(matrix, scale):
	newM = matrix
	for i in range(len(newM)):
		for j in range(len(newM[0])):
			newM[i][j] *= scale #multiplys each index by the scaler
	return newM

def mult_matrix(a, b):
	#a square 2d matrix (ex 10x10)
	#b list with length same as matrix (ex 10)
	length = len(b)
	c = [] #sets matrix size to be the same as "b"
	temp = 0
	for i in range(length):
		for j in range(length):
			temp += (a[j][i] * b[j])
		c.append(temp)
		temp = 0	
	return c
	
def euclidean_dist(a,b):
	eD = float(0.0)
	for i in range(len(a)):
		eD += ((a[i]  - b[i]) ** 2)
	eD = math.sqrt(eD)
	return eD
#put this here to steamline the norming proccess
def euclidean_norm(a):
	eN = float(0.0)
	for i in range(len(a)):
		eN += (a[i]**2)
	eN = math.sqrt(eN)
	return eN