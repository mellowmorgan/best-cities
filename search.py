import sqlite3
class Search: 

	def __init__(self, occupation):
	    self.occupation = str(occupation)

	#returns tuple containing avg salary of all salaries for given occupation in table
	def avg_salary(self):
		con = sqlite3.connect('data/data.db')
		curs = con.cursor()
		curs.execute("select avg(med) from tbl2 where occu LIKE ?", ('%'+self.occupation+'%',))
		salary_tuple = curs.fetchone() #fetch the first value it returns, since we only need one value
		curs.execute("select occu from cities where occu LIKE ?", ('%'+self.occupation+'%',))

		#obtain name of occupation as seem on table, so can print it correctly of results page (this is done in case user enters only part of name)
		occu = curs.fetchone(); 
		#returns tuple, must index to obtain text by itself
		self.occupation= occu[0]
		#same with average salary, must isolate integer from tuple given as fetchone() returns tuple
		self.avg_salary = int(round(salary_tuple[0]))		
		tup = (self.avg_salary, self.occupation) 
		return (tup)

	#returns list of tuples containing info of each row where salary of given occupation is higher than national average
	def over_med(self, avg):
		con = sqlite3.connect('data/data.db')
		curs = con.cursor()
	 	curs.execute("select locu,occu,med,emp from cities where occu LIKE ? AND med>?", ('%'+self.occupation+'%', avg))
	 	self.results=curs.fetchall()
	 	return (self.results)
	def add_codes(self, med_set):
		con=sqlite3.connect("data/data.db")
		cur =con.cursor()
		over_set = med_set
		for i in range(len(over_set)):
			tup =over_set[i]
			location = tup[0]
			cur.execute("SELECT code from rents WHERE city=?", (location,))
			code= cur.fetchone()
			list_tup = list(tup)
			if code != None:
				code = code[0]
			list_tup.append(code)
			over_set[i]=list_tup
		i=0
		while i<(len(over_set)):
			l = over_set[i]
		 	if l[4] == None:
		 		check = over_set.pop(i)
		 	else:
		 		i=i+1
		over_set.sort(key=lambda x: x[2], reverse=True)

		over_set= over_set[0:50]
		self.over_set = over_set
		return self.over_set
	def remove_dup(self, listy):
		checker=[]	
		i=0	
		while i<(len(listy)):
			lil=listy[i]
			locu=lil[0]
			if locu not in checker:
				checker.append(locu)
				i=i+1
			else:
				listy.remove(lil)
		return listy

#TEST METHODS IN CLASS
# test = Search("Software Developer")
# a=test.avg_salary()
# a= a[0]
# print a
# over = test.over_med(a)
# clean = test.add_codes(over)
# print clean


