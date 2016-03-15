from flask import Flask, render_template, request
import jinja2
import os
import Quandl
from search import Search, key,best_list, get_rents
import sqlite3
import pandas 
app = Flask(__name__)
# API Stuff
quandl_api_key = os.environ['QUANDL_API_KEY']

app.jinja_env.undefined = jinja2.StrictUndefined

#will return cleaned list of lists containing location, occupation, median salary, number employed, and codes for rent added at end

@app.route("/")
def homepage():
	k=key()
	return render_template("index.html", jobs=k)

@app.route("/results")
def occupation_handler():
	# Receive data from occupation input form and do stuff with it
	occupation = request.args.get("occupation")
	print occupation
	# API handling stuff goes here
	s = Search(occupation)
	a = s.avg_salary()
	over = s.over_med(a[0])
	added = s.add_codes(over) 	
	clean = s.remove_dup(added)
	best = get_rents(clean)
	best.sort(key=lambda x: x[6],reverse=True)
	final = best[0:5]
	first= final[0]
	loc= first[0]
	avg = a[0]
	occu=first[1]
	med = first[2]
	try:
		num = int(first[3])
	except:
		num = None
	rent = first[5]
	return render_template("results.html", loc=loc,occupation=occupation, occu=occu, avg=avg,med=med,num=num,rent=rent)

if __name__ == "__main__":
	app.run(debug=True)