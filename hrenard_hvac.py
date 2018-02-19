import numpy as np
import matplotlib.pyplot as plt
import math

delta_t = 5 / 60 												# hr
time_values = np.arange(0, 91 * 24, delta_t)
change_over_time = time_values * 1.5 / 91

# Outside Temperature
a = 6 * np.sin(2 * math.pi * time_values) + 35
b = np.random.normal(0, .1, len(time_values))

outside_temperature = a + b.cumsum() + change_over_time

# Thermostat - furnace
work_furnace = np.repeat(68, 9 / delta_t)
home_furnace = np.repeat(74, 6 / delta_t)
sleep_furnace = np.repeat(70, 9 / delta_t)

one_day_furnace = np.concatenate([work_furnace, home_furnace, sleep_furnace])

vacaction_furnace = np.repeat(55, 14 * 24 / delta_t)
pre_vac_furnace = np.tile(one_day_furnace, 37)
post_vac_furnace = np.tile(one_day_furnace, 40)

furnace = np.concatenate([pre_vac_furnace, vacaction_furnace, post_vac_furnace])

#Thermostat - A/C
work_AC = np.repeat(82, 9 / delta_t)
home_AC = np.repeat(79, 6 / delta_t)
sleep_AC = np.repeat(79, 9 / delta_t)

one_day_AC = np.concatenate([work_AC, home_AC, sleep_AC])

vacaction_AC = np.repeat(88, 14 * 24 / delta_t)
pre_vac_AC = np.tile(one_day_AC, 37)
post_vac_AC = np.tile(one_day_AC, 40)

AC = np.concatenate([pre_vac_AC, vacaction_AC, post_vac_AC])

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

furnace_cost_rate = 5											 	# dollar / hour
AC_cost_rate = 7											 	# dollar / hour

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
	leakage_rate = (house_leakage_factor * (inside_temperature[i - 1] - outside_temperature[i - 1])) 	# degF / hr
	T_prime = furnace_heat - AC_cool - leakage_rate
	inside_temperature[i] = inside_temperature[i - 1] + T_prime * delta_t
		
# utility cost
furnace_cost = furnace_on.sum() * (furnace_cost_rate * delta_t)								# dollar
AC_cost = AC_on.sum() * (AC_cost_rate * delta_t)										# dollar
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

