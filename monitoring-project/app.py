#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from flask import Flask, g, render_template, url_for, redirect, request, session
import mysql.connector
from passlib.hash import argon2
import requests


app = Flask(__name__)
app.config.from_object('secret_config')

def connect_db() :
	g.mysql_connection = mysql.connector.connect(
		host = app.config['DATABASE_HOST'],
		user = app.config['DATABASE_USER'],
		password = app.config['DATABASE_PASSWORD'],
		database = app.config['DATABASE_NAME']
		)
	return g.mysql_connection

def get_db() :
	if not hasattr(g, 'db') :
		g.db = connect_db()
	return g.db

@app.route('/')
def show_sites ():
	db = get_db()
	crs = db.cursor()
	crs.execute('SELECT * FROM websites')
	sites = crs.fetchall()
	return render_template('index.html', sites=sites)

@app.route('/login/', methods = ['GET', 'POST'])
def login() :
	email = str(request.form.get('email'))
	password = str(request.form.get('password'))

	db = get_db()
	crs = db.cursor()
	crs.execute('SELECT email, password, is_admin FROM user WHERE email= %(email)s', {'email' : email})
	users = crs.fetchall()

	user_correct = False
	for user in users :
		if argon2.verify(password, user[1]) :
			user_correct = user

	if user_correct :
		session['user'] = user_correct
		return redirect(url_for('admin'))

	return render_template('login.html')

@app.route('/admin/')
def admin () :

	db = get_db()
	crs = db.cursor()
	crs.execute('SELECT * FROM websites')
	sites = crs.fetchall()
	return render_template('admin.html', user = session['user'], sites=sites)

@app.route('/add/', methods= ['GET', 'POST'])
def add () :

	url = str(request.form.get('url'))
	if url!='None' :

		r = requests.get(url)
		status = r.status_code
		
		add_website = "INSERT INTO websites (url, status) VALUES (%s, %s)"
		data_website = (url, status)
		db = get_db()
		crs = db.cursor()
		crs.execute(add_website, data_website)
		db.commit()
		
		try:
			if session.get('user'):
				admin()
				return redirect(url_for('admin'))
		except PasAdmin:
			show_sites()
			return redirect(url_for('/'))
		
	return render_template('add.html')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
