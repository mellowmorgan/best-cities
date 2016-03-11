from flask import Flask, render_template, request
import jinja2
import os
import Quandl
from search import Search
import sqlite3
import pandas 


app = Flask(__name__)

# API Stuff
quandl_api_key = os.environ['QUANDL_API_KEY']

app.jinja_env.undefined = jinja2.StrictUndefined

sd = Search("Registered Nurse")
a = sd.avg_salary()
over = sd.over_med(a[0])
added = sd.add_codes(over) 
#will return cleaned list of lists containing location, occupation, median salary, number employed, and codes for rent added at end
clean = sd.remove_dup(added)

def best_list(big):
	for i in xrange(len(big)):
		listy=big[i]
	 	code = listy[4]
	 	code = 'ZILL/M' + code + "_RMP"
	 	data = Quandl.get(code, authtoken=quandl_api_key)
	 	last = data.tail(1)
	 	rent = int(last.Value)
	 	listy.append(rent)	
	 	listy.append(listy[2] - (12*listy[5]))
	return (big)

best = best_list(clean)
for item in best:
	print item

@app.route("/")
def homepage():
	return render_template("index.html")

@app.route("/results")
def occupation_handler():
	# Receive data from occupation input form and do stuff with it
	occupation = request.args.get("occupation")
	# API handling stuff goes here
	search = Search(occupation)
	tup=search.avg_salary()
	avg_salary= tup[0]
	occupation = tup[1]
	return render_template("results.html", occupation=occupation, avg_salary=avg_salary)


if __name__ == "__main__":
	app.run(debug=True)