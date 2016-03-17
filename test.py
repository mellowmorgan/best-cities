import sqlite3
"""USES QUANDL ZILLOW API TO FILL TABLE rentscodes WITH CURRENT MEDIAN RENTAL COSTS BY CITY CODE IN TABLE"""

quandl_api_key = os.environ['QUANDL_API_KEY']
con = sqlite3.connect("data/data.db")
cur = con.cursor()
cur.execute("SELECT code from rentscodes")
codes = cur.fetchall()

for item in codes:
	code=item[0]
	value = 'ZILL/M' + code + "_RMP"
	try:
		data = Quandl.get(value, authtoken=quandl_api_key)
		last = data.tail(1)
		rent = int(last.Value)
		cur.execute("UPDATE rentscodes SET rent=? WHERE code=?", (rent,code))
		con.commit()
	except:
		cur.execute("DELETE FROM rentscodes WHERE code=?", (code,))
		con.commit()

con.close()