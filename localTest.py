#from flask import Flask, jsonify
#from flask_restplus import Api, Resource, fields
#from flask import request
#import pymongo
#from pymongo import MongoClient
#from bson.objectid import ObjectId
#import time
import pandas as pd
import bokeh.plotting as plt
from bokeh.plotting import figure

from bokeh.palettes import Category20c
from math import pi
from bokeh.transform import cumsum

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, export_svgs
import matplotlib.pyplot as matplt
import squarify


def read_svg(path):
    svg = None
    with open(path, 'r') as f:
        svg = f.read()
    return svg


def avgUserRating(csv_data):
    # just get column of ave rating
    aur = csv_data['Average User Rating'].value_counts().sort_index()
    # create bokeh figure for containing bar chart
    p = figure(x_range=list(map(str,aur.index.values)), plot_height=250, title="Average User Rating", toolbar_location=None, tools = "")
    
    # create bar chart with x (rating 4.0 4.5...) and y (numbers)
    p.vbar(x=list(map(str,aur.index.values)),top=aur.values,width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start=0
    p.output_backend = 'svg'
    export_svgs(p, filename = "avgUserRating.svg")
    return read_svg("avgUserRating.svg")

def dateVsAppSize(csv_data):
    # format data string
    csv_data['Original Release Date'] = pd.to_datetime(csv_data['Original Release Date'], format = '%d/%m/%Y')
    
    # just get column of Original Release Date
    date_size = pd.DataFrame({'size':csv_data['Size']})
    date_size = date_size.set_index(csv_data['Original Release Date'])
    date_size = date_size.sort_values(by=['Original Release Date'])
    date_size.head()
    
    # compute monthly number for each app
    monthly_size = date_size.resample('M').mean()
    tmp = date_size.resample('M')
    monthly_size['min'] = tmp.min()
    monthly_size['max'] = tmp.max()
    monthly_size.head()

    p = figure(x_axis_type='datetime',           
             plot_height=250, plot_width=750,
             title='Date vs App Size (Monthly)')
    p.line(y='size', x='Original Release Date', source=monthly_size, line_width=2, line_color='Green')
    p.output_backend = 'svg'
    export_svgs(p, filename = "dataVsAppSize.svg")
    return 'success'
    # show(p)


def computeUniq(csv_data):
    # extract categories from geners
    genres = pd.DataFrame({ 'category' : csv_data["Genres"]})
    category = {}
    for row in csv_data["Genres"]:
        cate_list = row.split(',')
        for i in cate_list:
            if i not in category:
                category[i] = 1
            else:
                category[i] += 1
    cleaned_category = {}
    
    # remains category which is larger than 100
    for key in category:
        if category[key] > 100 :
            cleaned_category[key] = category[key]
    return cleaned_category


def categoryChart(csv_data):
    
    category = computeUniq(csv_data)


    # create dataframe for category
    data = pd.Series(category).reset_index(name='value').rename(columns={'index':'category'})

    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[20] + Category20c[3]
#    data["value"] = data['value']
    
    # create figure for containing pie chart
    p = figure(plot_height=350, plot_width=750, title="Numbers of Different Genres", toolbar_location=None,
        tools="hover", tooltips="@category: @value")
        
    # create pie chart auto compute angle for each category
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='category', source=data)

    # source = ColumnDataSource(data)

    # labels = LabelSet(x=0, y=1, text='value', level='glyph',
    #         angle=cumsum('angle', include_zero=True), source=source, render_mode='canvas')

    # p.add_layout(labels)

    # p.axis.axis_label=None
    # p.axis.visible=False
    # p.grid.grid_line_color = None

    p.output_backend = 'svg'
    export_svgs(p, filename = "categoryChart.svg")
    return read_svg("categoryChart.svg")
    
    # print(genres)

#def countGeners(csv_data):
#
#    category = computeUniq(csv_data)
#
#    cate_list = sorted(category, key=category.get, reverse=True)
#
#    cate_value = []
#
#    for key in cate_list:
#        cate_value.append(category[key])
#
#    # create figure for containing pie chart
#    p = figure(x_range=cate_list, plot_height=250, plot_width=1500,title="Number of genres", toolbar_location=None, tools = "")
#
#    # create bar chart with x (category) and y (count of each category)
#    p.vbar(x=cate_list,top=cate_value,width=0.9)
#    p.xgrid.grid_line_color = None
#    p.y_range.start=0
#    show(p)

def compute(csv_data):
    genres = pd.DataFrame({ 'category' : csv_data["Genres"]})
    category = {}
    for row in csv_data["Genres"]:
        cate_list = row.split(',')
        for i in cate_list:
            if i not in category:
                category[i] = 1
            else:
                category[i] += 1
    cleaned_category = {}
    for key in category:
        if category[key] > 500 :
            cleaned_category[key] = category[key]
    return cleaned_category

def countGeners(csv_data):

    category = compute(csv_data)

    cate_list = sorted(category, key=category.get, reverse=True)

    cate_value = []
    
    cate_color = ["maroon","navy","orange","blue", "grey","purple","yellow","pink","brown","olive","cyan","magenta","limegreen","gold","darkkhaki"]

    for key in cate_list:
        cate_value.append(category[key])

    squarify.plot(sizes=cate_value, label=cate_list, alpha=.7, color=cate_color )
    matplt.axis('off')
    matplt.savefig('countGeners.svg')
    return read_svg("countGeners.svg")
    # matplt.show()

def getTopTen(csv_data):

    # fill Nan with 0 and set type as int64
    csv_data['User Rating Count'] = csv_data['User Rating Count'].fillna(0)
    csv_data['User Rating Count'] = csv_data['User Rating Count'].astype('int64')
    # sort by rating
    temp = csv_data.sort_values(['User Rating Count'], ascending=False)
    
    # pick specific columns
    final = temp.loc[:, ['Icon URL','Name', 'Genres', 'Price', 'Size', 'Average User Rating']]
    
    # pick top 10 rows
    final = final[:5]

    # source = ColumnDataSource(final)

    # columns = [
    #         TableColumn(field="Icon URL", title="Icon"),
    #         TableColumn(field="Name", title="Name"),
    #         TableColumn(field="Genres", title="Genres"),
    #         TableColumn(field="Price", title="Price"),
    #         TableColumn(field="Size", title="App Size"),
    #         TableColumn(field="Average User Rating", title="Rating"),
    #     ]
        
    # # create data table
    # data_table = DataTable(source=source, columns=columns, width=400, height=280)

    # show(data_table)

    json_file = []
    for row in final:
        json_file.append({
           "Icon URL" : row["Icon URL"],
           "Name" : row["Name"],
           "Genres" : row["Genres"],
           "Price" : row["Price"],
           "App Size" : row["Size"],
           "Rating" : row["Average User Rating"]
        })
    print(json_file)
    return json_file

# csv_data = pd.read_csv("appstore_games.csv")
#avgUserRating(csv_data)
# dateVsAppSize(csv_data)
#categoryChart(csv_data)
# countGeners(csv_data)
#getTopTen(csv_data)
# print(csv_data)
