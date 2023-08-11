import math
import random
import matplotlib.pyplot as plt
import numpy as np

##########################################################################
## Initialisation
random.seed(1000)

size_array = 2000
interval_value = 5 # [-10;10]
def generation_perlin_noise_random_points(nb_points, interval_value):
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
			value = 0
			while value == 0:
				value = random.randrange(-1,2,1) #[-1;1] => -1,0,1  , il faut exclure 0
			value = last_number + value

		array_of_y_values_of_points.append(value)
		iterator += 1
		last_number = array_of_y_values_of_points[iterator]

	return array_of_y_values_of_points
our_y_array1 = generation_perlin_noise_random_points(size_array, interval_value)

##########################################################################
## Function

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

def get_random1_Y(x):
	x = int(x)

	while x >= len(our_y_array1):
		x = x - len(our_y_array1)
	
	while x < 0:
		x = x + len(our_y_array1)

	return our_y_array1[x]


def perlin_noise_1D(x, decoupe, octave):
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
	
	P1 = [borne_inf, get_random1_Y(borne_inf/fraction)]
	P2 = [borne_sup, get_random1_Y(borne_sup/fraction)]

	x_interpol = sin_interpolation(x, P1, P2)

	return x_interpol

def perlin_noise_1D_multi_octave(x, decoupe, nb_octave):
	x_noised = 0
	for i in range(1, nb_octave+1):
		x_noised = x_noised + perlin_noise_1D(x, decoupe, i)
	
	return x_noised/nb_octave

def perlin_noise_2D_multi_octave(x,y, nb_octave):
	decoupe = 20

	x_noised = perlin_noise_1D_multi_octave(x, decoupe, nb_octave)
	y_noised = perlin_noise_1D_multi_octave(y+(4213*decoupe), decoupe, nb_octave)

	height = (x_noised + y_noised)/2
	return height
def perlin_noise_3D_multi_octave(x,y,z, nb_octave):
	decoupe = 16

	x_noised = perlin_noise_1D_multi_octave(x, decoupe, nb_octave)
	y_noised = perlin_noise_1D_multi_octave(y+(65138*decoupe), decoupe, nb_octave)
	z_noised = perlin_noise_1D_multi_octave(y+(83165*decoupe), decoupe, nb_octave)

	density = (x_noised + y_noised + z_noised)/3
	return density

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
## Main

x = np.linspace(-40, 40, num=100)
y = np.linspace(-40, 40, num=100)
X, Y = np.meshgrid(x, y)

z = []
for i in x:
	z_temp = []
	for j in y:
		z_temp.append(perlin_noise_2D_multi_octave(i,j,1))
	z.append(z_temp)
Z = np.asarray(z)


fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, cmap='viridis',edgecolor='green')
ax.set_title('3d')

################################################

#x = np.linspace(-50, 50, num=100)
#z = []
#for j in x:
#	z.append(perlin_noise_2D_multi_octave(j,0,1))

#fig, ax = plt.subplots()
#ax.plot(x,z)
plt.show()





