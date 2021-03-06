from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_mysqldb import MySQL
from math import floor
import json, validators
import string
from random import choice
import psycopg2
import mysql.connector
app = Flask(__name__)

db = json.load(open('db.json',))
conn = psycopg2.connect(database = db['mysql_db'], user = db['mysql_user'], password = db['mysql_password'], host = db['mysql_host'], port = db['port'])

host = "https://vip-vik-short.herokuapp.com/"



def create_table_if_not_exit():
	table = "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, longurl TEXT);"
	try:
		cur = conn.cursor()
		cur.execute(table)
		conn.commit()
		print("table created")
	except Exception as e:
		conn.rollback()
		print("failure in table creation")

def operation(long_url):
	temp = long_url.split('://', 1)[0]
	if temp == long_url:
		return 'http://' + long_url
	else : return long_url

def base10(str):
	bs = 62
	str = str.split('-', 1)[0]
	base = string.digits + string.ascii_lowercase + string.ascii_uppercase
	length = len(str)
	res = 0
	for i in range(length):
		res = res * bs + base.find(str[i])
	return res


def base62(num):
   base = string.digits + string.ascii_lowercase + string.ascii_uppercase
   q = num
   bs = 62
   r = q % bs
   res = base[r]
   q = floor(q / bs)
   while q:
   	r = q % bs
   	res = base[r] + res
   	q = floor(q / bs)
   return res
  
def make_of_length7(short_url):
	temp_url = short_url
	str = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(7))
	length = len(temp_url)
	if length < 7:
		temp_url += '-'
		++length
	temp_url = temp_url + str[:7 - length]
	return temp_url



def view(long_url):
	try:
		cur = conn.cursor()
		cnt = 0
		cur.execute("""INSERT INTO users ("longurl") VALUES ('{}') RETURNING id""".format(long_url))
		cnt = cur.fetchone()[0]
		conn.commit()
		cur.close()
	except Exception as e:
		print(e)
		conn.rollback()
	short_url = base62(cnt)
	short_url = make_of_length7(short_url)
	return short_url



@app.route('/')
def index():
	return render_template('index.html')



@app.route('/short_url', methods = ['POST'])
def short_url():
	if request.is_xhr:
		long_url = request.form['longurl']
		if(long_url == ""):
			return jsonify({'error': "empty input"})
		long_url = operation(long_url)
		if not validators.url(long_url):
			return jsonify({'error' : "invalid url"})
		else :
			short_url1 = host + 'load/' + view(long_url)
			return jsonify({'short_url' : short_url1})
        

	else : abort(404)






@app.route('/load/<short_url>')
def redirect_short_url(short_url):
	if len(short_url) > 8 :
		return "<h1> wrong url</h1>" + '<a href = "{}"> back </a>'.format(host)
	ID1 = base10(short_url)

	try:
		cur = conn.cursor()
		cur.execute("""SELECT longurl FROM users WHERE id = {}""".format(ID1))
	except Exception as e:
		conn.rollback()
		print(e)
	try:
		redirect_url = cur.fetchone()[0]
	except Exception as e:
		return "<h1> wrong url</h1>"  + '<a href = "{}"> back </a>'.format(host)
	return redirect(redirect_url)


if __name__ == '__main__':
	create_table_if_not_exit()
	app.run(debug = True)