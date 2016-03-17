from flask import Flask, render_template, request
from search import Search, key
import jinja2
import os

app = Flask(__name__)

app.jinja_env.undefined = jinja2.StrictUndefined

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route("/")
def homepage():
	"""Generates HTML template for homepage and uses key method in search.py to get list of all occupations for drop-down menu."""
	k=key() #returns list of all occupations for user to select from drop-down menu

	return render_template("index.html", jobs=k) 


@app.route('/results/page/<int:page>')
@app.route("/results/", defaults={'page': None})
def occupation_handler(page):
	"""Uses Search class and other methods in search.py to find five best cities for selected occupation"""
	try:
		if not page:
			occupation = request.args.get("occupation")
			search_obj = Search(occupation)
			nat_avg = search_obj.nat_avg_salary() 

			sal_over_avg = search_obj.over_med_salary(nat_avg) #list of results where salary > national average
			best_list = search_obj.get_rents(sal_over_avg) #returns list of lists with (median rental costs for each city) and (salary-monthly rent*12) added 	
			best_list = search_obj.remove_duplicates(best_list) #removes lists in list with duplicate location values and returns "cleaned" list

			# Make global so when pagination occurs, search_obj does not have to be reinstantiated 
			global best_list_short
			best_list_short = best_list[0:5] # five best cities

			global global_avg
			global_avg = nat_avg

			page=1
			current=best_list_short[page-1] 

		else:
			current=best_list_short[page-1] #pagination

		return render_template("results.html", current=current, global_avg=global_avg, page=page)
	except IndexError:
		return render_template('error.html')

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)