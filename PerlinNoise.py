import math
import random
import matplotlib.pyplot as plt
import numpy as np

##########################################################################



#data_set is a list of random int ∈ [-interval_value, interval_value] with size = size_array
#the generation algorith can be totally normal but i need for my other project this algorith for generation:
#last value of data set must be close to the first value
#each new value can't be the same as the last one meaning if we got 2 and last one is 2, we roll another random number
#each new value is -1 or +1 of the last one, this create a flat continuity
#you can at any moment change generation_data_set to make it fully random
def generation_data_set(nb_points, interval_value):
	array_of_y_values_of_points = [random.randrange(interval_value, interval_value+1,1)]

	last_number = array_of_y_values_of_points[0]
	iterator = 0
	while len(array_of_y_values_of_points) <= nb_points or (last_number != array_of_y_values_of_points[0]+1 and last_number != array_of_y_values_of_points[0]-1):

		value = 0
		if last_number >= interval_value:
			value = interval_value - 1

		elif last_number <= -interval_value:
			value = -interval_value + 1

		else:
			while value == 0:
				value = random.randrange(-1,2,1) #[-1;1] => -1,0,1  , il faut exclure 0
			value = last_number + value

		array_of_y_values_of_points.append(value)
		iterator += 1
		last_number = array_of_y_values_of_points[iterator]

	return array_of_y_values_of_points



##########################################################################
## Function

#return the value of f(x) for a specific f sin function between 2 points
def sin_interpolation(x, P1, P2):
	if P1[1] != P2[1] :
		A = (P2[1]-P1[1])/2
		f = 1/(2*(P2[0]-P1[0]))
		Offset = (P2[1]+P1[1])/2

		in_asin = (P2[1]-Offset)/A
		if in_asin > 1:
			in_asin = 1
		elif in_asin < -1:
			in_asin = -1
		rho = math.asin(in_asin)-2*math.pi*f*P2[0]

		return A * math.sin(2*math.pi*f*x+rho) + Offset

	else:
		return P1[1]


#for each 'decoupe' return the y coord, creating a point P(x,y) with x being 'decoupe' multiple and y a random number
#if x is out of our data_set lenght, we replace it in our list range. it's the modulo of data_set lenght
def get_Y_data_set(x, data_set):
	x = int(x)

	while x >= len(data_set):
		x = x - len(data_set)
	
	while x < 0:
		x = x + len(data_set)

	return data_set[x]


def perlin_noise_1D(x, decoupe, octave, data_set):
	fraction = 16
	if (octave == 1):
		fraction = decoupe
	else:
		fraction = decoupe/((octave*2-2))
	
	borne_inf = fraction * math.floor(x/fraction)
	borne_sup = borne_inf + fraction
	if x >= 0:
		borne_inf = fraction * math.floor(x/fraction)
		borne_sup = borne_inf + fraction
	else:
		borne_sup = fraction * (math.floor(x/fraction)+1)
		borne_inf = borne_sup - fraction
	
	P1 = [borne_inf, get_Y_data_set(borne_inf/fraction, data_set)]
	P2 = [borne_sup, get_Y_data_set(borne_sup/fraction, data_set)]

	x_interpol = sin_interpolation(x, P1, P2)

	return x_interpol

#return the mean of each octave
def perlin_noise_1D_multi_octave(x, decoupe, nb_octave, data_set):
	x_noised = 0
	for i in range(1, nb_octave+1):
		x_noised = x_noised + perlin_noise_1D(x, decoupe, i, data_set)
	
	return x_noised/nb_octave


#decoupe must be divisible by 2^nb_octave such as if decoupe = 20 and nb_octave 3
#at first octave decoupe = 20,
#seconde octave decoupe = 10,
#third ocatave decoupe = 5
#in this example if decoupe = 20, nb_octave can't be >=3
#---
#each subsequent octave is x2 frenquency and /2 amplitude
#---
#when we get our second perlin noise graph (or third), here y_noised
#we need to put an offset to y so we can use the same data_set
#otherwise we need to generate a new data_set
def perlin_noise_2D_multi_octave(x,y, nb_octave, data_set):
	decoupe = 20

	x_noised = perlin_noise_1D_multi_octave(x, decoupe, nb_octave, data_set)
	y_noised = perlin_noise_1D_multi_octave(y+(4213*decoupe), decoupe, nb_octave, data_set)

	height = (x_noised + y_noised)/2
	return height
def perlin_noise_3D_multi_octave(x,y,z, nb_octave, data_set):
	decoupe = 20

	x_noised = perlin_noise_1D_multi_octave(x, decoupe, nb_octave, data_set)
	y_noised = perlin_noise_1D_multi_octave(y+(65138*decoupe), decoupe, nb_octave, data_set)
	z_noised = perlin_noise_1D_multi_octave(y+(83165*decoupe), decoupe, nb_octave, data_set)

	density = (x_noised + y_noised + z_noised)/3
	return density

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
## Main

## Initialisation
random.seed(1000)

size_array = 2000
interval_value = 5 # [-10;10]
data_set_1 = generation_data_set(size_array, interval_value)



x = np.linspace(-40, 40, num=100)
y = np.linspace(-40, 40, num=100)
X, Y = np.meshgrid(x, y)


## 3D plot height


z = []
for i in x:
	z_temp = []
	for j in y:
		z_temp.append(perlin_noise_2D_multi_octave(i,j,1, data_set_1))
	z.append(z_temp)
Z = np.asarray(z)


fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, cmap='viridis',edgecolor='green')
ax.set_title('3d')

## 2D plot

#x = np.linspace(-50, 50, num=100)
#z = []
#for j in x:
#	z.append(perlin_noise_2D_multi_octave(j,0,1, data_set_1))

#fig, ax = plt.subplots()
#ax.plot(x,z)
plt.show()





