import pickle
import flask
from flask import render_template
from flask import request
import pygal
import json
from urllib.request import urlopen 
from pygal.style import DarkSolarizedStyle

app = flask.Flask(__name__)
dict1=None

def make_graphs(dist_dict){
    line_chart = pygal.Line(width=1200, height=600,explicit_size=True,disable_xml_declaration=True)
    line_chart.title = 'Pattern of derailment from planned route v/s stop number'
    line_chart.x_title = "Stop number"
    line_chart.y_title = "Distance in meters"

    for i in dist_dict.keys():
        line_chart.add(str(i), list(dist_dict[i].values()))
    line_chart.x_labels = map(str, range(1, 40))
    
    total_avg_dist_dict={}
    #Graph 2
    for i in dist_dict.keys():
        total_dist=0
        for j in list(dist_dict[i].values()):
            total_dist+=float(j)
        total_dist=total_dist/len(list(dist_dict[i].values()))
        total_avg_dist_dict[i]=total_dist
    bar_chart = pygal.HorizontalBar(width=1200, height=600,explicit_size=True,disable_xml_declaration=True)
    bar_chart.title = 'Average distance from real distance v/s route numbers'
    bar_chart.y_title = "Stop number"
    bar_chart.x_title = "Distance in meters"
    for i in total_avg_dist_dict.keys():
        bar_chart.add(str(i), total_avg_dist_dict[i])
    
    return line_chart,bar_chart
}

@app.route('/')
def homepage():
    make_graphs(dict1)
    return render_template("Stats.html", line_chart=line_chart, bar_chart=bar_chart)

# @app.route('/allbooks')
# def allbooks():
# 	global books
# 	return render_template("allBooks.html",booo=books)

# @app.route('/addbook')
# def addbook():
# 	return render_template("addBook.html")

# @app.route('/addingBook',methods=['POST'])
# def addingBook():
# 	global books
# 	var1 = request.form['title']
# 	var2 = request.form['author']
	
# 	new_book = [var1,var2]
# 	books.append(new_book)
# 	return "Task Done"


# @app.route('/welcome')
# def welcome():
# 	return("This your welcome page")
# @app.route('/booksissued/<user>')
# def booksIssue(user):
# 	#return('<center>Hello m\'lad <b>' + user + '</b></center>')
# 	return render_template("allBooks.html",var1=user)
# @app.route('/issueBook')
# def issueBook():
# 	return render_template("issueBook.html")
if __name__ == "__main__" :
    with open('trip_dist_diff.dictionary', 'rb') as dict_file:
        dict1 = pickle.load(dict_file)
    app.run(debug=True)