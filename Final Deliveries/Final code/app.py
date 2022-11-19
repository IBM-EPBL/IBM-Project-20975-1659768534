from flask import Flask,render_template,request,redirect,url_for,session
from flask_session import Session
from flask_login import current_user,login_required
import requests
from mydb import connection as db
import ibm_db,ibm_db_dbi

app = Flask(__name__)
app.secret_key = 'login'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;PROTOCOL=TCPIP;UID=zpk91239;PWD=kcAFB7vdtgiV994R;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
connection = ibm_db_dbi.Connection(conn)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user (
	username VARCHAR(50) NOT NULL,  
	gmail VARCHAR(50) NOT NULL, 
    number VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
    )''')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('home.html',cases = case)

@app.route('/business')
def business():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('business.html',cases = case)

@app.route('/sports')
def sports():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('sports.html',cases = case)

@app.route('/entertainment')
def entertainment():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('entertainment.html',cases = case)

@app.route('/technology')
def technology():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('tech.html',cases = case)

@app.route('/science')
def science():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('science.html',cases = case)

@app.route('/health')
def health():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=a1920320e3f94345807b6b8ace35a04c"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('health.html',cases = case)

@app.route('/search',methods = ['GET','POST'])
def search():
    msg = ''
    if request.method == 'POST':
        text = request.form["search"]
        print(text)
        if (text == "sports"):
            return redirect('/sports')
        if (text == "science"):
            return redirect("/science")
        if (text == "buisness"):
            return redirect("/buisness")
        if (text == "entertainment"):
            return redirect("/entertainment")
        if (text == "technology"):
            return redirect("/technology")
        if (text == "health"):
            return redirect("/health")

    return redirect('home', msg = msg)

@app.route('/profile')
def profile():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ZPK91239.USER WHERE USERNAME = ?",(session["name"],))
    account = cursor.fetchall()
    print(account)
    return render_template('profile.html',acc = account)

@app.route("/register",methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form["username"]
        email = request.form["email"]
        number = request.form["number"]
        password = request.form["password"]
        session["name"] = request.form["username"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        print(name,email,number,password)
        db.register(name,email,number,password)
        return render_template('login.html', msg = msg) 
    else:
        return render_template('register.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        name = request.form["username"]
        password = request.form["password"]
        result_dict = db.login(name,password)
        msg = 'Invalid Username / Password'
        if result_dict != False:
            print(msg)
            session["name"] = request.form["username"]
            print(session["name"])
            return redirect(url_for('home'))
        return render_template('login.html', msg = msg)

    else:
        return render_template('login.html', msg = msg)
    
#log-out

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)

