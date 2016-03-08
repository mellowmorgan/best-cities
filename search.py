import sqlite3
class Search: 

	def __init__(self, occupation):
	    self.occupation = str(occupation)
	def avg_salary(self):
		con = sqlite3.connect('data/data.db')
		curs = con.cursor()
		curs.execute("select avg(med) from tbl2 where occu LIKE ?", ('%'+self.occupation+'%',))
		salary_tuple = curs.fetchone()
		curs.execute("select occu from tbl2 where occu LIKE ?", ('%'+self.occupation+'%',))
		occu = curs.fetchone();
		self.occupation= occu[0]
		self.avg_salary = int(round(salary_tuple[0]))
		tup = (self.avg_salary, self.occupation)
		return (tup)

	def over_med(self):
		con = sqlite3.connect('data/data.db')
		curs = con.cursor()
	 	curs.execute("select locu,occu,med,emp from cities where occu LIKE ? AND med>=?", ('%'+self.occupation+'%', self.avg_salary))
	 	self.results=curs.fetchall()
	 	return (self.results)

	def cpi(self):
		return 0