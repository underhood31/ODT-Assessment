import pickle
import flask
from flask import render_template, make_response
from flask import request
import pygal
import json
import pdfkit
from urllib.request import urlopen 
from pygal.style import DarkSolarizedStyle

app = flask.Flask(__name__)
dict1=None
dict2=None
dict3=None

def make_graphs(dist_dict,r):
    line_chart = pygal.Line(width=1200, height=600,explicit_size=True,disable_xml_declaration=True)
    line_chart.title = 'Pattern of derailment from planned trip v/s stop number'
    line_chart.x_title = "Trip ID"
    line_chart.y_title = "Distance in meters"

    for i in dist_dict.keys():
        line_chart.add(str(i), list(dist_dict[i].values()))
    line_chart.x_labels = map(str, range(1, r))
    
    total_avg_dist_dict={}
    #Graph 2
    for i in dist_dict.keys():
        total_dist=0
        for j in list(dist_dict[i].values()):
            total_dist+=float(j)
        total_dist=total_dist/len(list(dist_dict[i].values()))
        total_avg_dist_dict[i]=total_dist
    bar_chart = pygal.HorizontalBar(width=1200, height=600,explicit_size=True,disable_xml_declaration=True)
    bar_chart.title = 'Average distance from planned position v/s trip numbers'
    bar_chart.y_title = "Stop number"
    bar_chart.x_title = "Distance in meters"
    for i in total_avg_dist_dict.keys():
        bar_chart.add(str(i), total_avg_dist_dict[i])
    
    return line_chart,bar_chart


@app.route('/')
def homepage():
    line_chart1,bar_chart1=make_graphs(dict1,40)
    line_chart2,bar_chart2=make_graphs(dict2,65)
    line_chart3,bar_chart3=make_graphs(dict3,45)
    rendered = render_template("Stats.html", line_chart1=line_chart1, bar_chart1=bar_chart1,line_chart2=line_chart2, bar_chart2=bar_chart2,line_chart3=line_chart3, bar_chart3=bar_chart3)
    return rendered

@app.route('/dnld', methods=['POST'])
def dnld_pop():
    line_chart1,bar_chart1=make_graphs(dict1,40)
    line_chart2,bar_chart2=make_graphs(dict2,65)
    line_chart3,bar_chart3=make_graphs(dict3,45)
    rendered = render_template("Stats.html", line_chart1=line_chart1, bar_chart1=bar_chart1,line_chart2=line_chart2, bar_chart2=bar_chart2,line_chart3=line_chart3, bar_chart3=bar_chart3)
    pdf=pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"  
    response.headers['Content-Disposition'] = "attachment; filename=Report.pdf"  
    return response
if __name__ == "__main__" :
    with open('trip_dist_diff1.dictionary', 'rb') as dict_file:
        dict1 = pickle.load(dict_file)
    with open('trip_dist_diff2.dictionary', 'rb') as dict_file:
        dict2 = pickle.load(dict_file)
    with open('trip_dist_diff3.dictionary', 'rb') as dict_file:
        dict3 = pickle.load(dict_file)
    app.run(debug=True)