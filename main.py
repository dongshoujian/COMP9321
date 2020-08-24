from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields, reqparse, abort
from flask import request
from flask_cors import CORS, cross_origin
import pymongo
from bson.objectid import ObjectId
from localTest import *
import datetime
import json
from functools import wraps
import jwt
import pandas as pd
from preprossing import *
import os
import matplotlib.pyplot as matplt
import numpy as np 
# import missingno as msno
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import neighbors

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["mydatabase"]
profile_collection = db["user_profile"]

class AuthenticationToken:
    def __init__(self,secret_key,expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in

    def generate_token(self,username):
        info = {
            'username':username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expires_in)
        }
        return jwt.encode(info, self.secret_key, algorithm='HS256')

    def validate_token(self,token):
        info = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        return info['username']

SECRET_KEY = "THIS IS THE SECRET KEY FOR COMP9321 ROUND TABLE."
expires_in = 60000
auth = AuthenticationToken(SECRET_KEY, expires_in)


app = Flask(__name__)
api = Api(app, 
            authorizations={
                    'API-KEY':{
                        "type": 'apiKey',
                        "name": "AUTH-TOKEN",
                        "in": "header"
                    }
            },
            security= 'API-KEY',
            default='COMP9321 assignment 2',
            version='1.0', 
            title='RoundTable API',
            description='A simple API for COMP9321',
          )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')
        try:
            user = auth.validate_token(token)
        except Exception as e:
            abort(401,e)
        return f(*args, **kwargs)
    return decorated


cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #sovle cors issue

app.config['CORS_HEADERS'] = 'Content-Type'

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        if username == 'admin' and password == 'admin':
            return {"token": auth.generate_token(username).decode('utf-8')}

        return {"message": "Sorry"}

csv_data = pd.read_csv("appstore_games.csv")


@api.route('/login')
class Login(Resource):
    login_details = api.model('login_details', {
        'email': fields.String(required=True, example='roundtable@unsw.edu.au'),
        'password': fields.String(required=True, example='123456')
    })
    @api.expect(login_details)
    @api.response(200, 'Success')
    @api.response(403, 'Invalid username or password')
    def post(self):
        readData = request.json
        username = readData['username']
        password = readData['password']

        if username == 'admin' and password == 'admin':
            return {"message": auth.generate_token(username).decode('utf-8')}

        return {"message": "Sorry"}

@api.route('/login/changePassword/<string:user_id>')
class changePassword(Resource):
    pass_details = api.model('pass_details', {
        'password': fields.String(required=True, example='123456')
    })
    @api.expect(pass_details)
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    def put(self, user_id):
        readData = request.json
        getData = db.profile_collection.find_one({'_id': ObjectId(user_id)})
        if getData:
            updateData = {'password': readData['password']}
            db.profile_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': updateData}
            )
            return {'result': 'Success'}
        else:
            return {'result': 'No such user'}

@api.route('/predict')
class predict(Resource):
    predict_details = api.model('predict_details', {
        'price': fields.String(required=True, example='1.99'),
        'ageRating': fields.String(required=True, example='Age_17+'),
        'size': fields.String(required=True, example='100000'),
        'genres': fields.String(required=True, example='Genre_RolePlaying'),
    })
    @api.expect(predict_details)
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    @api.doc(description="predict the rating of a game based on price, age, size and genres.")
    # @api.expect(predict_parser, validate=True)
    def post(self):
        readData = request.json
        price = readData["price"]
        ageRating = readData["ageRating"]
        size = readData["size"]
        genres = readData["genres"]
        result = ml(price,ageRating,size,genres)
        print(type(result))
        return {"result": result}


def generatePredictArray(colName, price,ageRating,size,genres):
	l = []
	dic = { "Price" : price, "Size" : size, ageRating : 1, genres : 1}
	for i in colName:
		if i in dic:
			if i in ["Price"]:
				l.append(float(dic[i]))
			else:
				l.append(dic[i])
		else:
			l.append(0)
	print(l)
	return np.array([l])
    
def ml(price,ageRating,size,genres):
	feature_cols = ['Price', 'Size','Genre_Action'	,'Genre_Adventure',	'Genre_Board',\
		'Genre_Books',	'Genre_Business'	,'Genre_Card'	,'Genre_Casino', 'Genre_Casual',\
		'Genre_Education'	,'Genre_Entertainment'	,'Genre_Family',	'Genre_Finance'	,'Genre_Food&Drink',\
		'Genre_Health&Fitness'	,'Genre_Lifestyle'	,'Genre_Magazines&Newspapers',	'Genre_Medical',\
		'Genre_Music'	,'Genre_Navigation'	,'Genre_News'	,'Genre_Photo&Video',	'Genre_Productivity',\
		'Genre_Puzzle'	,'Genre_Racing'	,'Genre_Reference'	,'Genre_RolePlaying',	'Genre_Shopping',\
		'Genre_Simulation',	'Genre_SocialNetworking',	'Genre_Sports',	'Genre_Stickers',	'Genre_Strategy',\
		'Genre_Travel',	'Genre_Trivia',	'Genre_Utilities',	'Genre_Word',\
		'Age_12+'	,'Age_17+',	'Age_4+'	,'Age_9+']

	df = pd.read_csv('newdata.csv',thousands = ',')

	# print(df)
	x = df[feature_cols]
	y = df['Average User Rating']	
	# print(y.shape)
	x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
	print(type(x_test))
	linreg = neighbors.KNeighborsRegressor()
	linreg.fit(x_train, y_train)

	my_test = generatePredictArray(feature_cols,price,ageRating,size,genres)
	# my_test = np.array([[float(284),float(1.99),float(12328960)]])
	y_pred = linreg.predict(my_test)
	print(y_pred[0])
	return str(y_pred[0])

@api.route('/potentialCustomer')
class gameVsLanguage(Resource):
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    @api.doc(description="Show the games with the most potential customers")
    def get(self):
        mergedDF = pd.read_csv("appstore_games_languages.csv")
        json_file = []
        for index,row in mergedDF.iterrows():
            # print(row)
            json_file.append({
                "Icon URL" : row["Icon URL"],
                "Names" : row["Names"],
                "Genres" : row["Genres"],
                "Price" : row["Price"],
                "Total(million)" : row["Total(million)"],
                "Languages" : row["Languages"]
            })
        # print(json_file)
        return {"result" : json_file}

@api.route('/avgUserRatingFreeGames')
class avgUserRatingVSfree(Resource):
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    @api.doc(description="Show the average user rating in free games.")
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        csv_data = csv_data[csv_data["Price"]==0]
        aur = csv_data['Average User Rating'].value_counts().sort_index()
        # create bokeh figure for containing bar chart
        p = figure(x_range=list(map(str,aur.index.values)), plot_height=250, title="Average User Rating VS Free", toolbar_location=None, tools = "")
        
        # create bar chart with x (rating 4.0 4.5...) and y (numbers)
        p.vbar(x=list(map(str,aur.index.values)),top=aur.values,width=0.9,color="firebrick")
        p.xgrid.grid_line_color = None
        p.y_range.start=0
        p.output_backend = 'svg'
        if os.path.exists('frontend/src/views/countRating/avgUserRatingFree.svg'):
            return {'result': 'avgUserRatingFree has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/countRating/avgUserRatingFree.svg')
            return {'result': 'avgUserRatingFree success'}


@api.route('/avgUserRatingPaidGames')
class avgUserRatingVSpaid(Resource):
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    @api.doc(description="Show the average user rating in paid games.")
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        csv_data = csv_data[csv_data["Price"]>0]
        aur = csv_data['Average User Rating'].value_counts().sort_index()
        # create bokeh figure for containing bar chart
        p = figure(x_range=list(map(str,aur.index.values)), plot_height=250, title="Average User Rating VS Paid", toolbar_location=None, tools = "")
        
        # create bar chart with x (rating 4.0 4.5...) and y (numbers)
        p.vbar(x=list(map(str,aur.index.values)),top=aur.values,width=0.9,color="green")
        p.xgrid.grid_line_color = None
        p.y_range.start=0
        p.output_backend = 'svg'
        if os.path.exists('frontend/src/views/countRating/avgUserRatingPaid.svg'):
            return {'result': 'avgUserRatingPaid has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/countRating/avgUserRatingPaid.svg')
            return {'result': 'avgUserRatingPaid success'}


@api.route('/avgUserRating')
class avgUserRating(Resource):
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    @api.doc(description="generate a bar chart to show average rating.")
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        aur = csv_data['Average User Rating'].value_counts().sort_index()
        # create bokeh figure for containing bar chart
        p = figure(x_range=list(map(str,aur.index.values)), plot_height=250, title="Average User Rating", toolbar_location=None, tools = "")
        
        # create bar chart with x (rating 4.0 4.5...) and y (numbers)
        p.vbar(x=list(map(str,aur.index.values)),top=aur.values,width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start=0
        p.output_backend = 'svg'
        if os.path.exists('frontend/src/views/countRating/avgUserRating.svg'):
            return {'result': 'avgUserRating has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/countRating/avgUserRating.svg')
            return {'result': 'avgUserRating success'}

def sim(p,a,g):
    csv_data = pd.read_csv("appstore_games.csv")
    
    csv_data = csv_data.drop(['URL','ID','Subtitle','In-app Purchases','Description','Developer','Original Release Date','Current Version Release Date','Primary Genre'], axis=1)
    
    csv_data = csv_data.drop('Genres', axis=1).join(csv_data['Genres'].str.split(', ',expand=True).stack().reset_index(level=1, drop=True).rename('Genre'))
    csv_data.index = range(len(csv_data))
    csv_data = csv_data[csv_data["Price"]==float(p)]
    csv_data = csv_data[csv_data["Age Rating"]==a[4:]]
    csv_data = csv_data.loc[csv_data["Genre"]==g]
    csv_data = csv_data.dropna()
    # print(csv_data)
    # print(csv_data.head())
    
    csv_data = csv_data.sort_values(["Average User Rating"], ascending=False)
    csv_data = csv_data[:10]
    # print(csv_data)
    return csv_data
    

@api.route('/searchAttribute')
class avgUserRatingVSpaid(Resource):
    search_details = api.model('search_details', {
        'price': fields.String(required=True, example='0'),
        'ageRating': fields.String(required=True, example='Age_4+'),
        'genres': fields.String(required=True, example='Strategy'),
    })
    @api.expect(search_details)
    @requires_auth
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @api.doc(description="Show the top ten games in selected attributes.")
    def post(self):
        readData = request.json
        price = readData["price"]
        ageRating = readData["ageRating"]
        genres = readData["genres"]
        similarTop = sim(price,ageRating,genres)
        json_file = []
        for index,row in similarTop.iterrows():
    
            json_file.append({
                "Icon URL" : row["Icon URL"],
                "Name" : row["Name"],
                "Genre" : row["Genre"],
                "Price" : row["Price"],
                "Size" : row["Size"],
                "AgeRating" : row["Age Rating"],
                "AverageUserRating" : row["Average User Rating"]
            })
        print(json_file)
        return {"result" : json_file}


@api.route('/countGeners')
class getImages(Resource):
    @api.doc(description="Generates a graph to show game counts in differnet geners.")
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
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
        category = cleaned_category
        cate_list = sorted(category, key=category.get, reverse=True)
        cate_value = []
        cate_color = ["maroon","navy","orange","blue", "grey","purple","yellow","pink","brown","olive","cyan","magenta","limegreen","gold","darkkhaki"]

        for key in cate_list:
            cate_value.append(category[key])

        squarify.plot(sizes=cate_value, label=cate_list, alpha=.7, color=cate_color )
        matplt.axis('off')
        if os.path.exists('frontend/src/views/Dashboard/countGeners.svg'):
            return {'result': 'countGeners has been exported'}
        else:
            matplt.savefig('frontend/src/views/Dashboard/countGeners.svg')
            return {'result': 'countGeners success'}

@api.route('/category')
class getCategory(Resource):
    @api.doc(description="Generates a graph to show different category.")
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        # global csv_data
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
        category = cleaned_category
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
        p.output_backend = 'svg'
        if os.path.exists('frontend/src/views/Dashboard/categoryChart.svg'):
            return {'result': 'categoryChart has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/Dashboard/categoryChart.svg')
            return {'result': 'categoryChart success'}

@api.route('/dateVsAppSize')
class getCount(Resource):
    @api.doc(description="Show the trend of date and size.")
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
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
        if os.path.exists('frontend/src/views/Dashboard/dateVsAppSize.svg'):
            return {'result': 'dateVsAppSize has been exported'}
        else:
            export_svgs(p, filename = 'frontend/src/views/Dashboard/dateVsAppSize.svg')
            return {'result': 'dateVsAppSize success'}



@api.route('/getTopFive')
class getTopTen(Resource):
    @api.doc(description="Search the top five games according to rating.")
    @api.response(200, 'Success')
    @api.response(403, 'Error')
    @requires_auth
    def get(self):
        csv_data = pd.read_csv("appstore_games.csv")
        csv_data['User Rating Count'] = csv_data['User Rating Count'].fillna(0)
        csv_data['User Rating Count'] = csv_data['User Rating Count'].astype('int64')
        # sort by rating
        temp = csv_data.sort_values(['User Rating Count'], ascending=False)
        
        # pick specific columns
        final = temp.loc[:, ['Icon URL','Name', 'Genres', 'Price', 'Size', 'Average User Rating']]
        
        # pick top 10 rows
        final = final[:5]
        # print(final)
        json_file = []
        for index,row in final.iterrows():
            # print(row[1])
            json_file.append({
            "Icon URL" : row[0],
            "Name" : row[1],
            "Genres" : row["Genres"],
            "Price" : row["Price"],
            "App Size" : row["Size"],
            "Rating" : row["Average User Rating"]
            })
        # print(json_file)
        # global csv_data
        return {"result" :json_file}



if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(debug=True)
