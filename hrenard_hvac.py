import numpy as np
import matplotlib.pyplot as plt
import math

delta_t = 5 / 60 												# hr
time_values = np.arange(0, 91 * 24, delta_t)
change_over_time = time_values * 2 / 91

# Outside Temperature
a = 6 * np.sin(2 * math.pi * time_values) + 30
b = np.random.normal(0, .1, len(time_values))

outside_temperature = a + b.cumsum() + change_over_time

# Thermostat - heat
work = np.repeat(68, 9 / delta_t)
home = np.repeat(74, 6 / delta_t)
sleep = np.repeat(70, 9 / delta_t)

one_day = np.concatenate([work, home, sleep])

vacaction = np.repeat(55, 14 * 24 / delta_t)
pre_vac = np.tile(one_day, 37)
post_vac = np.tile(one_day, 40)

furnace = np.concatenate([pre_vac, vacaction, post_vac])

#Thermostat - A/C
work2 = np.repeat(82, 9 / delta_t)
home2 = np.repeat(79, 6 / delta_t)
sleep2 = np.repeat(79, 9 / delta_t)

one_day2 = np.concatenate([work2, home2, sleep2])

vacaction2 = np.repeat(88, 14 * 24 / delta_t)
pre_vac2 = np.tile(one_day2, 37)
post_vac2 = np.tile(one_day2, 40)

AC = np.concatenate([pre_vac2, vacaction2, post_vac2])

# variables
furnace_rate = 2											 	# degF / hr
AC_rate = 1.5												 	# degF / hr
house_leakage_factor = .02										 	# (degF / hr) / degF

hysteresis = 1  											 	# degF

furnace_on = np.empty(len(time_values))
AC_on = np.empty(len(time_values))

furnace_on[0] = False											 	# boolean
AC_on[0] = False											 	# boolean

inside_temperature = np.zeros(len(time_values))

inside_temperature[0] = outside_temperature[0]								 	# degF

furnace_cost_rate = 0											 	# (dollar / degF) / hr ???
AC_cost_rate = 0											 	# (dollar / degF) / hr ???

#Loop
for i in range(1, len(time_values)):
	# Furnace
	if furnace_on[i - 1]:
		if inside_temperature[i - 1] - furnace[i - 1] > hysteresis:
			furnace_on[i] = False							 		# boolean
			furnace_heat = 0							 		# degF / hr
		else:
			furnace_on[i] = True							 		# boolean
			furnace_heat = furnace_rate						 		# degF / hr
	else:
		if inside_temperature[i - 1] - furnace[i - 1] < -hysteresis:
			furnace_on[i] = True							 		# boolean
			furnace_heat = furnace_rate						 		# degF / hr
		else:
			furnace_on[i] = False							 		# boolean
			furnace_heat = 0							 		# degF / hr				
	# AC
	if AC_on[i - 1]:
		if inside_temperature[i - 1] - AC[i - 1] < hysteresis:
			AC_on[i] = False						 			# boolean
			AC_cool = 0							 			# degF / hr
		else:
			AC_on[i] = True							 			# boolean
			AC_cool = AC_rate								 	# degF / hr
	else:
		if inside_temperature[i - 1] - AC[i - 1] > -hysteresis:
			AC_on[i] = True							 			# boolean
			AC_cool = AC_rate						 			# degF / hr
		else:
			AC_on[i] = False						 			# boolean
			AC_cool = 0								 		# degF / hr				
	
	# TODO: calculate costs from rate
	furnace_cost = 0
	AC_cost = 0

	leakage_rate = (house_leakage_factor * (inside_temperature[i - 1] - outside_temperature[i - 1])) 	# degF / hr
	T_prime = furnace_heat - AC_cool - leakage_rate
	inside_temperature[i] = inside_temperature[i - 1] + T_prime * delta_t
		
# utility cost
print("estimated average monthly utility cost (in U.S. dollars): $" + str(furnace_cost + AC_cost))

# Plotting
plt.plot(time_values, outside_temperature, color='green', linestyle="-", label="Outside Temperature")
plt.plot(time_values, inside_temperature, color='black', linestyle="-", label="Inside Temperature")
plt.plot(time_values, furnace, color='red', linestyle="-", label="Furnace Setting")
plt.plot(time_values, AC, color='blue', linestyle="-", label="A/C Setting")
plt.plot(time_values, furnace_on * 2 + 5, color='orange', linestyle="-", label="Furnace on")
plt.plot(time_values, AC_on * 2 + 10, color='purple', linestyle="-", label="A/C on")
plt.ylim(0, 100)
plt.legend()
plt.show()
