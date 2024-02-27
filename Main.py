
from flask import Flask,render_template,request,redirect,flash
import config,time,hashlib
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12121212ssss",
  database="url_short"
)
baseurl = "127.0.0.1:8080/"
mycursor = mydb.cursor()
def GetDatabase(short_url):	
	mycursor.execute("SELECT * FROM Links")
	Data = mycursor.fetchall()
	for i in Data:
		if short_url == i[1]:
			return "http://" + i[0]	
	return "/"
def Add_Link(Url):
	st = str(time.time()) + Url
	short = hashlib.sha256(st.encode()).hexdigest()
	short = short[:10]
	val = (Url, short)
	mycursor.execute('INSERT INTO Links VALUES(%s, %s)',val)
	mydb.commit()
	return baseurl + short
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def Root():
	return render_template("index.html")
@app.route("/add",methods=['POST'])
def Short_link():
	Shorted_Url = request.form["url"]
	Shorted_Url = Shorted_Url.replace("http://", " ")
	Shorted_Url = Shorted_Url.replace("https://", " ")
	Shorted_Url = Shorted_Url.replace(" ", "")
	g = Add_Link(Shorted_Url)
	return g
@app.route("/<Shorted_Url>")
def View_link(Shorted_Url):
	return redirect(GetDatabase(Shorted_Url))
