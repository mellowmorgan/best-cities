from search import Search, key
from flask import Flask, render_template, request
import sqlite3
import jinja2

app = Flask(__name__)

app.jinja_env.undefined = jinja2.StrictUndefined



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route("/")
def homepage():
	"""Generates html template for homepage and uses key method in search.py to get list of all occupations for drop-down menu."""
	k=key() #returns list of all occupations for user to select from drop-down menu

	return render_template("index.html", jobs=k) 


@app.route('/results/page/<int:page>')
@app.route("/results/", defaults={'page': None})
def occupation_handler(page):
	"""Uses Search class and other methods in search.py to find five best cities for selected occupation"""
	try:
		if not page:
			"""if default page (page=None), obtains list of five best cities and gives the first in list for first(default) result page"""
			occupation = request.args.get("occupation")
			print occupation
			search_obj = Search(occupation)
			nat_avg = search_obj.nat_avg_salary() 
			#returns tuple with two items, one representing average salary in U.S. for given occupation and the other the tiptle of occupation as seen in database

			nat_avg = nat_avg[0] #avg method in Search class returns tuple with two items, get first which is average salary in U.S. for occupation 
			sal_over_avg = search_obj.over_med_salary(nat_avg) #returns list of rows as tuples from table "cities" where salary is over national average
			best_list = search_obj.get_rents(sal_over_avg) #returns list of lists with (median rental costs for each city) and (salary minus monthly rent times 12) added 	
			best_list = search_obj.remove_duplicates(best_list) #removes lists in list with duplicate location values and returns "cleaned" list

			global best_list_short
			#make global so when pagination occurs, search_obj does not have to be reinstantiated and can be used outside of above if statement 
			best_list_short = best_list[0:5] # final now has five best cities with their info in it! 

			global global_avg
			#make global so when pagination occurs, search_obj does not have to be reinstantiated and national average can be used outside of above if statement 
			global_avg = nat_avg

			page=1 #for future pagination back to this page
			current=best_list_short[page-1] #current page shows list of info for best city in sorted list 

		else:
			"""For other pages, give next best city and its info in list"""
			current=best_list_short[page-1] #pagination will allow user to see next best city in list 

		return render_template("results.html", current=current, global_avg=global_avg, page=page)
		"""Finally, render html template with best city info for current place in list"""
	except IndexError:
		return render_template('error.html')

if __name__ == "__main__":
	app.run(debug=True)