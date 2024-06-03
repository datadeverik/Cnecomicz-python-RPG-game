import random

def roll_x_d_n_and_keep_highest_k(x, n, k):
	result = 0
	results_list = [ ]
	for i in range(x):
		results_list.append(random.randint(1,n))
	for j in range(k):
		highest = max(results_list)
		result += highest
		results_list.remove(highest)
	return result

def roll_x_d_n(x, n):
	return roll_x_d_n_and_keep_highest_k(x, n, x)

def thread_the_needle(low, high):
	return low < roll_x_d_n(1, 20) < high

def roll_below(value):
	return thread_the_needle(0, value)

def roll_above(value):
	return thread_the_needle(value, 21)