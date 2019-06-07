class Stack:

	def __init__(self):
		self.__list = []

	def push(self, x):
		"""Pushes the point on the stack
		"""
		self.__list.append(x)

	def pop(self):
		"""Pops the point from the Stack
		"""
		self.__list.pop()

	def top(self):
		"""Returns the point at 1st position from top of the Stack
		"""
		return self.__list[len(self.__list)-1]

	def next_to_top(self):
		"""Returns the point at 2nd position from top of the Stack
		"""

		return self.__list[len(self.__list)-2]

	def print_all(self):
		"""Returns all the points on the Stack
		"""
		return self.__list

	def get_stack_len(self):
		return len(self.__list)




def initialize():
	"""Tester function to simulate the working of Stack

	"""
	while True:
		if input("Do you want to create a Stack?[Y|N]") == "Y":
			break
		elif input("Do you want to create a Stack?[Y|N]") == "N":
			System.out.println("Exiting the program")
			exit()
		else:
			System.out.println("Enter a valid choice either Y or N")
	s= Stack()
	s.push((1,2))
	s.push((4,5))
	print(s.top())
	print(s.next_to_top())
	print(s.print_all())


if __name__ == '__main__':
	initialize()