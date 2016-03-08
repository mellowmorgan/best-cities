from flask import Flask, render_template, request
import jinja2
from search import Search

app = Flask(__name__)

app.jinja_env.undefined = jinja2.StrictUndefined

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