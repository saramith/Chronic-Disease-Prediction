from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Blu_kuttu9'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/output')
def output():
	msg='s'
	return render_template('output.html',msg = msg)

@app.route('/cardio', methods =['GET', 'POST'])
def cardio():
	msg = ''
	if request.method == 'POST' and 'gender' in request.form and 'age' in request.form and 'hypertension' in request.form and 'heart_disease' in request.form and 'ever_married' in request.form and 'work_type' in request.form and 'residence_type' in request.form and 'avg_glucose_level' in request.form and 'bmi' in request.form and 'smoking_status' in request.form:
		gender = request.form['gender']
		age = request.form['age']
		hypertension = request.form['hypertension']
		heart_disease = request.form['heart_disease']
		ever_married = request.form['ever_married']
		work_type = request.form['work_type']
		residence_type = request.form['residence_type']
		avg_glucose_level = request.form['avg_glucose_level']
		bmi = request.form['bmi']
		smoking_status = request.form['smoking_status']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		if not gender or not age or not hypertension or not heart_disease or not work_type or not residence_type or not ever_married or not avg_glucose_level or not bmi or not smoking_status:
		 	msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO account_stroke VALUES (NULL, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,NULL)', (gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,avg_glucose_level,bmi,smoking_status, ))
			mysql.connection.commit()
			msg=strokeml(gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,avg_glucose_level,bmi,smoking_status)
			return render_template('output.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('cardio.html', msg = msg)

def strokeml(gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,avg_glucose_level,bmi,smoking_status):
	heart_data = pd.read_csv("Stroke.csv",sep=",")

	heart_data['bmi'].fillna(heart_data['bmi'].median(),inplace=True)

	heart_data.drop('id',axis=1,inplace=True)

	heart_data.gender[heart_data.gender=='Male']=0
	heart_data.gender[heart_data.gender=='Female']=1
	heart_data.ever_married[heart_data.ever_married=='Yes']=1
	heart_data.ever_married[heart_data.ever_married=='No']=0
	heart_data.work_type[heart_data.work_type=='Private']=0
	heart_data.work_type[heart_data.work_type=='Self-employed']=1
	heart_data.work_type[heart_data.work_type=='children']=2
	heart_data.work_type[heart_data.work_type=='Govt_job']=3
	heart_data.work_type[heart_data.work_type=='Never_worked']=4
	heart_data.Residence_type[heart_data.Residence_type=='Urban']=0
	heart_data.Residence_type[heart_data.Residence_type=='Rural']=1
	heart_data.smoking_status[heart_data.smoking_status=='formerly smoked']=0
	heart_data.smoking_status[heart_data.smoking_status=='never smoked']=1
	heart_data.smoking_status[heart_data.smoking_status=='smokes']=2
	heart_data.smoking_status[heart_data.smoking_status=='Unknown']=3

	S= heart_data[heart_data.stroke == 0]
	NS= heart_data[heart_data.stroke == 1]

	S_sample=S.sample(n=251)

	#concatenating the two datasets 
	nds=pd.concat([S_sample,NS],axis=0)

	#nds is our new dataset 
	nds['stroke'].value_counts()

	X=nds.drop(columns='stroke',axis=1)
	Y=nds['stroke']

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, stratify=Y, random_state=99)

	model = LogisticRegression()

	model.fit(X_train, Y_train)

	input_data=(gender,age,hypertension,heart_disease,ever_married,work_type,residence_type,avg_glucose_level,bmi,smoking_status)	
	# change the input data to a numpy array
	input_data_as_numpy_array= np.asarray(input_data)
	# reshape the numpy array as we are predicting for only on instance
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	prediction = model.predict(input_data_reshaped)
	# print(prediction)
	if (prediction[0]== 0):
		return "Congratulations!\n\nYour demographics, lifestyle and body parameters suggest that you’re NOT AT RISK. Spread the will for a health-friendly lifestyle that you follow now and get yourself checked periodically from us or a professional.\n\nCheers!"
	else:
		return "Your demographics, lifestyle and body parameters suggest that you’re AT RISK. Visit a General Physician or a Neurologist near you to confirm, and secure your health and future!\n Adopt a healthier lifestyle and get your family checked as well, as stroke may also be hereditary.\n\nHealth is wealth indeed."


@app.route('/diabetes', methods =['GET', 'POST'])
def diabetes():
	msg = ''
	if request.method == 'POST' and 'pregnancies' in request.form and 'glucose' in request.form and 'bloodpressure' in request.form and 'skinthickness' in request.form and 'insulin' in request.form and 'bmi_dia' in request.form and 'diabetes_pedigree_fnc' in request.form and 'age_dia' in request.form:
		pregnancies = request.form['pregnancies']
		glucose = request.form['glucose']
		bloodpressure = request.form['bloodpressure']
		skinthickness = request.form['skinthickness']
		insulin = request.form['insulin']
		bmi_dia = request.form['bmi_dia']
		diabetes_pedigree_fnc = request.form['diabetes_pedigree_fnc']
		age_dia = request.form['age_dia']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		if not pregnancies or not glucose or not bloodpressure or not skinthickness or not insulin or not bmi_dia or not diabetes_pedigree_fnc or not age_dia:
		 	msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO account_dia VALUES (NULL, %s, %s, %s,%s,%s,%s,%s,%s,NULL)', (pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi_dia,diabetes_pedigree_fnc,age_dia, ))
			mysql.connection.commit()
			msg=diaml(pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi_dia,diabetes_pedigree_fnc,age_dia)
			return render_template('output.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('diabetes.html', msg = msg)

def diaml(pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi_dia,diabetes_pedigree_fnc,age_dia):
	db =pd.read_csv("db.csv",sep=",")

	S= db[db.Outcome == 0]
	NS= db[db.Outcome == 1]
	S_sample=S.sample(n=232)
	nds=pd.concat([S,NS],axis=0)

	X=nds.drop(columns='Outcome',axis=1)
	Y=nds['Outcome']

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, stratify=Y, random_state=0)

	model = LogisticRegression()

	model.fit(X_train, Y_train)

	input_data=(pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi_dia,diabetes_pedigree_fnc,age_dia)	
	# change the input data to a numpy array
	input_data_as_numpy_array= np.asarray(input_data)

	# reshape the numpy array as we are predicting for only on instance
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

	prediction = model.predict(input_data_reshaped)

	if (prediction[0]== 0):
		return "Congratulations!\n\nYour demographics, lifestyle, and body parameters suggest that you’re NOT AT RISK. Spread the will for a health-friendly lifestyle that you follow now and get yourself checked periodically from us or a professional.\n\nCheers!"
	else:
		return "Your demographics, lifestyle and body parameters suggest that you’re AT RISK. Visit a General Physician or an Endocrinologist near you to confirm, and secure your health and future!\nAdopt a healthier lifestyle by moving more often and get your family checked as well, as diabetes is hereditary.\nHealth is wealth indeed."

@app.route('/cardiovascular', methods =['GET', 'POST'])
def cardiovascular():
	msg = ''
	if request.method == 'POST' and 'age1' in request.form and 'gender1' in request.form and 'height' in request.form and 'weight' in request.form and 'ap_hi' in request.form and 'ap_lo' in request.form and 'cholesterol' in request.form and 'glu' in request.form and 'smoke' in request.form and 'alco' in request.form and 'active' in request.form:
		age1 = request.form['age1']
		gender1 = request.form['gender1']
		height = request.form['height']
		weight = request.form['weight']
		ap_hi = request.form['ap_hi']
		ap_lo = request.form['ap_lo']
		cholesterol = request.form['cholesterol']
		glu = request.form['glu']
		smoke = request.form['smoke']
		alco = request.form['alco']
		active = request.form['active']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		if not age1 or not gender1 or not height or not weight or not ap_hi or not ap_lo or not cholesterol or not glu or not smoke or not alco or not active:
		 	msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO account_cardiovascular VALUES (NULL, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,NULL)', (age1,gender1,height,weight,ap_hi,ap_lo,cholesterol,glu,smoke,alco,active,))
			mysql.connection.commit()
			msg=cardiovascularml(age1,gender1,height,weight,ap_hi,ap_lo,cholesterol,glu,smoke,alco,active)
			return render_template('output.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form2!'
	return render_template('cardiovascular.html', msg = msg)

def cardiovascularml(age1,gender1,height,weight,ap_hi,ap_lo,cholesterol,glu,smoke,alco,active):
 	heart_data = pd.read_csv("3.csv",sep=";")

 	S= heart_data[heart_data.CARDIO_DISEASE == 0]
 	NS= heart_data[heart_data.CARDIO_DISEASE == 1]

 	#concatenating the two datasets 
 	nds=pd.concat([S,NS],axis=0)

 	#nds is our new dataset 
 	nds['CARDIO_DISEASE'].value_counts()

 	X=nds.drop(columns='CARDIO_DISEASE',axis=1)
 	Y=nds['CARDIO_DISEASE']

 	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, stratify=Y, random_state=0)

 	model = LogisticRegression()

 	model.fit(X_train, Y_train)

 	input_data=(age1,gender1,height,weight,ap_hi,ap_lo,cholesterol,glu,smoke,alco,active)	
 	# change the input data to a numpy array
 	input_data_as_numpy_array= np.asarray(input_data)

 	# reshape the numpy array as we are predicting for only on instance
 	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
 	prediction = model.predict(input_data_reshaped)

 	if (prediction[0]== 0):
 		return "Congratulations!\n\nYour demographics, lifestyle, and body parameters suggest that you’re NOT AT RISK of cardiovascular diseases.Spread the will for a health-friendly lifestyle that you follow now and get yourself checked periodically from us or a professional.\n\nCheers!"
 	else:
 		return "Your demographics, lifestyle, and body parameters suggest that you’re AT RISK of one or many of the cardiovascular diseases ( Coronary heart disease, Cardiac arrest, Heart failure etc)\nVisit a General Physician or a Cardiologist near you to confirm, and secure your health and future! Adopt a healthier lifestyle and clean eating habits, and get your family checked as well, as these diseases can be hereditary. \nHealth is wealth indeed."


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
