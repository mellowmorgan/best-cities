from flask import Flask, render_template, request
import jinja2

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
	return render_template("results.html", occupation=occupation)

if __name__ == "__main__":
	app.run(debug=True)