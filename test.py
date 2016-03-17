import sqlite3
"""Uses Quandl Zillow API to fill table 'rentscodes' with current median rental costs by city code in table."""

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