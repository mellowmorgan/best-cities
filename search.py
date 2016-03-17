import sqlite3

class Search: 

	def __init__(self, occupation):
	    self.occupation = str(occupation)

	def nat_avg_salary(self):
		"""Returns tuple containing the average salary for given occupation in table and occupation as seen in table."""
		
		"""Database data contains U.S. salary data obtained from Federal Bureau of Labor Statistics website.
		Code below enables python to go into sqlite database and retrieve data in tables"""  
		conn = sqlite3.connect('data/data.db') 
		curs = conn.cursor()

		curs.execute("SELECT avg(med) FROM tbl2 WHERE occu=?", (self.occupation,))
		salary_tuple = curs.fetchone() #returns tuple containing national average salary for given occupation
		self.avg_salary = int(salary_tuple[0]) #Same with average salary, must isolate integer from tuple

		"""This chunk of code below is actually superfluous given drop-down menu that restricts user to selecting occupation 
		exactly as it appears in database, but if they were to enter it in themselves, this code would be necessary"""
		curs.execute("SELECT occu FROM cities WHERE occu LIKE ?", ('%'+self.occupation+'%',))
		occupation_tuple = curs.fetchone() 
		self.occupation= occupation_tuple[0] #Must index tuple to obtain text by itself

		tuple_salary_occupation = (self.avg_salary, self.occupation) #make tuple containing average salary and occupation
		
		return (tuple_salary_occupation)

	def over_med_salary(self, avg):
		"""Returns list of tuples containing info of each row where salary of given occupation is higher than national average."""

		conn = sqlite3.connect('data/data.db')
		curs = conn.cursor()

	 	curs.execute("SELECT locu, occu, med, emp FROM cities WHERE occu LIKE ? AND med > ?", ('%'+self.occupation+'%', avg))
	 	#get selected rows where occupation equals selected occupation and median salary is over national average for given occupation

	 	self.results=curs.fetchall() #returns selected rows as tuples in a list
	 	
	 	return (self.results) 

	def get_rents(self, best_city_list):
		"""Converts tuples in list to lists in list, so that rent can be appended
		as well as median annual salary minus rent*12 to determine best cities
		and sorts list of best cities, descending"""
		
		conn=sqlite3.connect("data/data.db")
		curs =conn.cursor()
		
		for i in range(len(best_city_list)):
			tup =best_city_list[i] #tup represents each tuple in list
			location = tup[0]
			curs.execute("SELECT rent FROM rentscodes WHERE city=?", (location,))
			rent= curs.fetchone() #returns rent at location in tuple
			tuple_as_list = list(tup) #converts tuple to list so it is mutable
			if rent != None: 
				"""For some cities, there is no rent information available in table."""
				rent=rent[0] #isolate rent from tuple
				tuple_as_list.append(rent)
				tuple_as_list.append(tuple_as_list[2]-(12*rent)) #salary minus rent*12; formula for determining best cities
			else:
				best_city_list.pop(i) #remove list in list where there is no rent info available

			best_city_list[i] = tuple_as_list

		best_city_list.sort(key=lambda x: x[5], reverse=True) 
		#sorts list according to the last item in each list in list, which is salary minus rent*12, descending from best	
		return best_city_list

	def remove_duplicates(self, best_city_list):
		"""Remove any duplicate lists for one city in best_city_list"""
		
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
		
		return best_city_list #return list with removed duplicates



def key():
	"""Returns list of all occupations in cities table for drop-down menu on homepage"""
	
	conn = sqlite3.connect('data/data.db')
	curs = conn.cursor()
	curs.execute("SELECT occu FROM cities WHERE locu = 'Portland, OR';") 
	"""for efficiency, picked big city where there are most likely all occupations that exist within U.S.""" 

	key = curs.fetchall() #returns list of tuples
	key.sort() #sorts list alphabetically
	key_list = []
	
	#For loop makes list of tuples into simple list of type string occupations
	for entry in key:
		key_list.append(str(entry[0]))

	checker=[]	 
	i=0	
	while i<(len(key_list)):
		"""Just in case, remove duplicates"""
		lil=key_list[i]
		if lil not in checker:
			checker.append(lil)
			i=i+1
		else:
			key_list.remove(lil)
	
	return key_list 