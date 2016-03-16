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

#list of lists containing info for best cities

@app.route('/results/page/<int:page>')
@app.route("/results/", defaults={'page': None})
def occupation_handler(page):
	# Receive data from occupation input form and do stuff with it
	if not page:
		occupation = request.args.get("occupation")
		s = Search(occupation)
		a = s.avg_salary()
		over = s.over_med(a[0])
		added = s.add_codes(over) 	
		clean = s.remove_dup(added)
		best = get_rents(clean)
		best.sort(key=lambda x: x[6],reverse=True)
		global final 
		final= best[0:5] #final now has five best cities with their info in it!
		global avg
		avg = a[0]
		page=1
		current=final[page-1]	
	else:
		current=final[page-1]

	return render_template("results.html", current=current,avg=avg,  page=page)



if __name__ == "__main__":
	app.run(debug=True)