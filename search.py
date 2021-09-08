import sqlite3

class Search: 

	def __init__(self, occupation):
	    self.occupation = str(occupation)

	def nat_avg_salary(self):
		"""Returns tuple containing the average salary for given occupation."""

		conn = sqlite3.connect('data/data.db') 
		curs = conn.cursor()

		curs.execute("SELECT avg(med) FROM tbl2 WHERE occu=?", (self.occupation,))
		salary_tuple = curs.fetchone()
		self.avg_salary = int(salary_tuple[0])

		return self.avg_salary

	def over_med_salary(self, avg):
		"""Returns list of tuples containing info of each row where salary of given occupation is higher than national average."""

		conn = sqlite3.connect('data/data.db')
		curs = conn.cursor()

		curs.execute("SELECT locu, occu, med, emp FROM cities WHERE occu LIKE ? AND med > ?", ('%'+self.occupation+'%', avg))
	 	#get selected rows where occupation equals selected occupation and median salary is over national average

		self.results=curs.fetchall() #returns selected rows as tuples in a list

		return (self.results) 

	def get_rents(self, best_city_list):
		"""Returns list of lists containing best cities, sorted descending by salary-rent*12"""
		
		conn = sqlite3.connect("data/data.db")
		curs = conn.cursor()
		
		for i in range(len(best_city_list)):
			tup = best_city_list[i]
			location = tup[0]
			curs.execute("SELECT rent FROM rentscodes WHERE city=?", (location,))
			rent = curs.fetchone()
			tuple_as_list = list(tup) #converts tuple to list so it is mutable
			
			if rent != None: 
				#For some cities, there is no rent information available in table.
				rent = rent[0] 
				tuple_as_list.append(rent)
				tuple_as_list.append(tuple_as_list[2]-(12*rent)) # formula for determining best cities: salary - rent*12 
			else:
				best_city_list.pop(i) #remove items in list where there is no rent info available

			best_city_list[i] = tuple_as_list

		best_city_list.sort(key=lambda x: x[5], reverse=True) 

		return best_city_list

	def remove_duplicates(self, best_city_list):
		"""Remove any duplicate lists in best_city_list"""
		
		non_duplicates=[]	
		i=0	
		
		while i<(len(best_city_list)):
			item=best_city_list[i]
			location=item[0]

			if location not in non_duplicates:
				non_duplicates.append(location)
				i=i+1
			else:
				best_city_list.remove(item)
		
		return best_city_list



def key():
	"""Returns list of all occupations for drop-down menu on homepage."""
	
	conn = sqlite3.connect('data/data.db')
	curs = conn.cursor()
	curs.execute("SELECT occu FROM cities WHERE locu = 'Portland, OR';") 
	#for efficiency, picked big city where there are most likely all occupations that exist within U.S.

	key = curs.fetchall()
	key.sort()
	key_list = []
	
	#makes list of tuples into simple list of occupations
	for entry in key:
		key_list.append(str(entry[0]))

	checker=[]	 
	i=0	
	while i<(len(key_list)):
		lil=key_list[i]
		if lil not in checker:
			checker.append(lil)
			i=i+1
		else:
			key_list.remove(lil)
	
	return key_list 