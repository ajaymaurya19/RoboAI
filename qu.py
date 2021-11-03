import multiprocessing

def square_list(q):
	"""
	function to square a given list
	"""
	# append squares of mylist to queue

	while True:
         q.put()

def print_queue(q):
	"""
	function to print queue elements
	"""
	print("Queue elements:")
	while True:
		print(q.get())
	print("Queue is now empty!")

if __name__ == "__main__":
	# input list
	mylist = [i for i in range(100)]
	# creating multiprocessing Queue
	q = multiprocessing.Queue()

	# creating new processes
	p1 = multiprocessing.Process(target=square_list, args=(q,))
	p2 = multiprocessing.Process(target=print_queue, args=(q,))

	# running process p1 to square list
	p1.start()

	# running process p2 to get queue elements
	p2.start()

