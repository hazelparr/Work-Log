import csv
import sys
import os
import re
import datetime
from task import Task


def clear():
	"""Clears screen whenever called"""
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")


def write_to_file(task):
	"""Writes an entry to a csv file"""
	already_exists = os.path.isfile("work_log.csv")

	with open("work_log.csv", "a") as csvfile:
		fieldnames = ["Task_Name", "Time_Spent(Min)", "Notes", "Date"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		if not already_exists:
			writer.writeheader()
		writer.writerow({fieldnames[0]: task.task_name,
						 fieldnames[1]: task.minutes,	
						 fieldnames[2]: task.notes,
						 fieldnames[3]: task.date})

def main_menu():
	"""Displays main menu and asks user input whether
	to add an entry, look up existing one or quit the
	program"""
	
	print("""
WORK.LOG - Log, edit, delete, save and seach your tasks!
--------------------------------------------------------
MAIN MENU
[A] - Add new task
[S] - Search existing task(s)
[D] - Display all saved tasks
[Q] - Quit and exit the program
""")

	option = input("Please select option from menu: "
				).lower().strip()

	if option == "a":
		clear()
		task = Task()
		add_new_task(task)
	elif option == "s":
		clear()
		search_menu()
	elif option == "d":
		clear()
		entries = open_file("work_log.csv")
		display_entries(entries)
	elif option == "q":
		sys.exit()
	else:
		input("Invalid entry. See menu for valid options. "
			"Press enter to continue.")
		clear()
		main_menu()


def search_menu():
	"""Displays search menu"""
	print("""
WORK.LOG - Log, edit, delete, save and seach your tasks!
--------------------------------------------------------
SEARCH MENU
[D] - Find by date
[T] - Find by time spent
[S] - Find by exact string
[R] - Find by regular expression
[M] - Back to main menu
[Q] - Quit and exit the program
""")
	option = input("Please select option from menu: "
					).lower().strip()

	if option == "d":
		clear()
		search_by_range_date()
	elif option == "t":
		clear()
		search_time_spent()
	elif option == "s":
		clear()
		search_string_regex("string")
	elif option == "r":
		clear()
		search_string_regex("regular expression")
	elif option == "m":
		clear()
		main_menu()
	elif option == "q":
		sys.exit()
	else:
		input("Invalid entry. See menu for valid options. "
			"Press enter to continue.")
		clear()
		search_menu()


def display_temp_entry(task):
	"""Print task not yet written to file, to be saved, 
	edited or deleted"""
	print("Task Name: {}".format(task.task_name))
	print("Time Spent (Minutes): {}"
		.format(task.minutes))
	print("Notes: {}".format(task.notes))
	print("Date: {}\n".format(task.date))


def add_new_task(task):
	"""Menu to ask user if the entry will be edited, 
	saved or deleted"""
	clear()
	display_temp_entry(task)
	print("""
Would you like to:
[S] - Save the entry
[E] - Edit the entry
[D] - Delete the entry
""")

	option = input("Please select option from menu: "
				).lower().strip()

	if option == "s":
		write_to_file(task)
		input("Entry saved!. Press enter to go back to main menu.")
		clear()
		main_menu()
	elif option == "e":
		clear()
		edit_entry(task)
	elif option == "d":
		input("Entry deleted!. Press enter to go back to main menu.")
		clear()
		main_menu()
	else:
		input("Invalid entry. See menu for valid options. "
			"Press enter to continue.")
		clear()
		add_new_task()


def edit_entry(task):
	"""Menu to edit the any of the fields in the task re: 
	name, time, notes and date"""
	display_temp_entry(task)
	print("""

Which field would you like to edit:
[A] - Task Name
[T] - Time Spent
[N] - Notes
[D] - Date

""")

	option = input("Please select option from menu: "
				).lower().strip()

	if option == "a":
		task.get_task_name()
		input("Task Name edited. Press enter to continue.")
		clear()
		add_new_task(task)
	elif option == "t":
		task.get_minutes()
		input("Time Spent edited. Press enter to continue.")
		clear()
		add_new_task(task)
	elif option == "n":
		task.get_notes()
		input("Notes edited. Press enter to continue.")
		clear()
		add_new_task(task)
	elif option == "d":
		clear()
		task.get_date()
		input("Date edited. Press enter to continue.")
		clear()
		add_new_task(task)
	else:
		input("Invalid entry. See menu for valid options. "
			"Press enter to continue.")
		clear()
		edit_entry()


def open_file(file_name):
	"""Takes file name as argument and returns a 
	list of dictionary of the entries"""
	with open(file_name, newline="") as csvfile:
		entries = list(csv.DictReader(csvfile, delimiter=","))
	return entries


def search_time_spent():
	"""Lets user search for exact number of minutes spent"""
	string = input("Enter the time spent to search: ")
	entries = open_file("work_log.csv")
	search_result = []
	for entry in entries:
		if re.search(r'{}'.format(string), entry["Time_Spent(Min)"]):
			search_result.append(entry)
	
	if search_result:
		display_entries(search_result)
	else:
		print("No result found for {} in 'Time Spent'.".format(string))
	
	input("Press enter to continue.")
	clear()
	search_menu()


def search_string_regex(text):
	"""Looks up string or the regex input to see if 
	it is in the file"""
	string = input("Enter the to search: "
		.format(text))
	entries = open_file("work_log.csv")
	search_result = []
	for entry in entries:
		if (re.search(r'{}'.format(string), entry["Task_Name"]) or
			re.search(r'{}'.format(string), entry["Notes"])):
			search_result.append(entry)

	if search_result:
		clear()
		display_entries(search_result)
	else:
		print("No result found for {} in file.".format(string))
	
	input("Press enter to continue.")
	clear()
	search_menu()

# is this needed? #######################################################
def search_by_regex():
	"""Looks up regeular expression input to see if it is in the file"""
	string = input("Enter the regular expression: ")
	entries = open_file("work_log.csv")
	search_result = []
	for entry in entries:
		for __, value in entry.items():
			if re.search(r'{}'.format(string), value):
				search_result.append(entry)
				break

	if search_result:
		print(search_result)### write show results function? #####################
	else:
		print("No result found for {}.".format(string))
	
	input("Press enter to continue.")
	clear()
	search_menu()


def search_date_input(text):
	"""Validates date entry if in correct format"""
	date = input("\nEnter the {} to search "
				"(DD/MM/YYYY): ".format(text))
	try:
		datetime.datetime.strptime(date, "%d/%m/%Y")
	except ValueError:
		input("Please enter date in this format: DD/MM/YYYY."
			" Press enter to continue.")
		clear()
		return search_date_input(text)
	else:
		return date


def list_dates(entries):
	"""Lists date results and user chooses which 
	entries to view"""
	print("Search yielded the following results: \n")
	counter = 1
	for entry in entries:
		print("[{}] - {}".format(counter, entry["Date"]))
		counter +=1
		

def date_display(entries):
	"""Look up entry based on list date search results"""
	list_dates(entries)
	print("""
Would you like to:
[E] - Look up an entry of date on the list
[S] - Back to Search Menu
[Q] - Quit and exit the program
""")
	
	option = input("Please select option from menu: "
		).lower().strip()

	if option == "e":
		clear()
		date_lookup(entries)
	elif option == "s":
		clear()
		search_menu()
	elif option == "q":
		main_menu()
	else:
		input("Invalid entry. See menu for valid options. "
			"Press enter to continue.")
		clear()
		date_display(entries)


def date_lookup(entries):
	"""Look up entry from result of date search"""
	list_dates(entries)
	date = input("\nFrom the list, enter date to look up entry. ")
	
	entry_to_display = []
	
	for entry in entries:
		if date == entry["Date"]:
			entry_to_display.append(entry)
			
	if entry_to_display:
		clear()
		display_entries(entry_to_display)		
	else:
		input("Input is not in the search result list. "
			"Try again.")
		clear()
		date_lookup(entries)


def search_by_range_date():
	"""Search file by range of dates. Input start date
	and end date from user """
	start = search_date_input("start date")
	clear()
	end = search_date_input("end date")

	start_date = datetime.datetime.strptime(
				start, "%d/%m/%Y")
	end_date = datetime.datetime.strptime(
				end, "%d/%m/%Y")

	entries = open_file("work_log.csv")
	search_result = []

	for entry in entries:
		entry_date = datetime.datetime.strptime(entry["Date"], 
					"%d/%m/%Y")
		if start_date <= entry_date and entry_date <= end_date:
			search_result.append(entry)
	
	if search_result:
		clear()
		date_display(search_result)
	else:
		print("No result found for date range: {} - {}.".format(
				start, end))
	
	input("Press enter to continue to Search Menu.")
	clear()
	search_menu()


def print_entries(index, entries, display=True):
	"""Prints the entries in a clean format"""
	if display:
		print("Displaying {} of {} entry/entries.\n"
			.format(index+1, len(entries)))

	print("Task Name: {}".format(entries[index]["Task_Name"]))
	print("Time Spent (Minutes): {}"
		.format(entries[index]["Time_Spent(Min)"]))
	print("Notes: {}".format(entries[index]["Notes"]))
	print("Date: {}\n".format(entries[index]["Date"]))


def display_choices(index, entries ):
	"""Menu choices to page through multiple entries"""
	p = "[P] - Previous Entry"
	n = "[N] - Next Entry"
	m = "[M] - Go back to Main Menu"
	menu = [p,n,m]

	if index == 0:
		menu.remove(p)
	if index == len(entries) - 1:
		menu.remove(n)

	for menu in menu:
		print(menu)



def display_entries(entries):
	"""Display entries to screen"""
	index = 0
	
	while True:
		print_entries(index, entries)

		if len(entries) == 1:
			input("Press enter to go back to main menu.")
			clear()
			main_menu()

		display_choices(index, entries)

		choice = input("\nPlease select option from"
			" menu. ").lower().strip()

		if index == 0 and choice == "n":
			index += 1
			clear()
		elif (index > 0 and index < len(entries)-1 
			and choice == "p"):
			index -= 1
			clear()
		elif (index > 0 and index < len(entries)-1 
			and choice == "n"):
			index += 1
			clear()
		elif index == len(entries)-1 and choice == "p":
			index -= 1
			clear()
		elif choice == "m":
			clear()
			main_menu()
		else:
			print("Invalid input. Refer to menu for valid "
				"choice. Press enter to continue. ")
			clear()





if __name__ == '__main__':
	clear()
	main_menu()
	