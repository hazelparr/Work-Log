import datetime

class Task:
	"""Asks for input from user regarding the
	task details"""

	def get_task_name(self):
		"""Asks user for the task name, checks if
		valid entry"""
		task_name = input("Task Name: ")
		if len(task_name) == 0:
			input("Task Name should be at least one character long. Press enter to continue.")
			self.get_task_name()
		else:
			self.task_name = task_name
		

	def get_minutes(self):
		"""Asks user for the time spent, check if 
		valid entry"""
		minutes = input("Number of minutes spent: ")
		try:
			int(minutes)
		except ValueError:
			input("Entry must be an integer. Example: 1, 20. Press enter to continue.")
			self.get_minutes()
		else:
			self.minutes = minutes

	
	def get_notes(self):
		"""Asks user for notes, optional"""
		self.notes = input("Notes (Press enter if None): ")
		

	def get_date(self):
		"""Asks user for date, check if valid entry"""
		date = input("Enter date (Format:DD/MM/YYYY): ")
		try:
			datetime.datetime.strptime(date, "%d/%m/%Y")
		except ValueError:
			input("Please enter date in this format: DD/MM/YYYY. Press enter to cotinue.")
			self.get_date()
		else:
			self.date = date

		

	def __init__(self):
		self.get_task_name()
		self.get_minutes()
		self.get_notes()
		self.get_date()


