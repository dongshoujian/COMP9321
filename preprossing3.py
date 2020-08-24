import pandas as pd
import numpy as np 
# import missingno as msno
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import neighbors

def f(x):
    aa = x.index(",")
    return x[:aa]
def y(x):
	return str(x)+','

def pre():
	df = pd.read_csv('appstore_games.csv',thousands = ',')
	df.drop(['URL','User Rating Count','Name','In-app Purchases',\
		'Description','Subtitle','Icon URL','Original Release Date',\
		'Current Version Release Date','Primary Genre'], axis=1, inplace=True)

	#delete NULL rating
	a=[]
	for index,row in df.iterrows():
		if np.isnan(row['Average User Rating'])==True:
			a.append(index)
	b=a[::-1]
	df = df.drop(df.index[b],axis=0)


	max_min_scaler = lambda x : x/1000000
	df['Size'] = df[['Size']].apply(max_min_scaler)
	#print(df['Genres'].head(5))
	#see the NULL data
	# msno.matrix(df)
	# plt.show()

	df['Genres'] = df['Genres'].str.replace(r"Games,", "")
	df["Genres"] = df["Genres"].apply(y)
	df["Genres"] = df["Genres"].apply(f)
	df['Genres'] = df['Genres'].str.replace(r" ", "")


# 处理类别数据 one-hot encoder
#1.类别 Genres

	gen = pd.DataFrame()
	gen = pd.get_dummies(df['Genres'],prefix='Genre')
	# print(gen.to_string())
	df = pd.concat([df,gen],axis=1)
	# print(df.head().to_string())
#2.Age rating
	age = pd.DataFrame()
	age = pd.get_dummies(df['Age Rating'],prefix='Age')
	df = pd.concat([df,age],axis=1)

	df.to_csv(r'./newdata.csv',index=False,sep=',')	



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
	print('123')
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


	
	print(y.shape)

	x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
	print(type(x_test))
	linreg = neighbors.KNeighborsRegressor()
	linreg.fit(x_train, y_train)

	my_test = generatePredictArray(feature_cols,price,ageRating,size,genres)
	# my_test = np.array([[float(284),float(1.99),float(12328960)]])
	y_pred = linreg.predict(my_test)
	print(type(str(y_pred[0])))
	print(str(y_pred[0]))
	return str(y_pred[0])


if __name__ == "__main__":
	# pre()
    ml('12', 'Age_17+', '123231', 'Genre_RolePlaying')
