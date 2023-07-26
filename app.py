from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
const_firebaseConfig = {
  "apiKey": "AIzaSyC8EgAa3Z_GxBQk-2scxGsW_xvxpMoER5I",
  "authDomain": "example-628cb.firebaseapp.com",
  "databaseURL":"https://example-628cb-default-rtdb.firebaseio.com",
  "projectId":"example-628cb",
  "storageBucket": "example-628cb.appspot.com",
  "messagingSenderId": "503931398850",
  "appId": "1:503931398850:web:7128323c95fa98969aa95b",
  "measurementId": "G-XZY132B6D2",
  "databaseURL": "https://example-628cb-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(const_firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route("/" , methods = ['GET', 'POST'])
def home_page():
	if request.method == 'POST':
		if request.form.get('action1') == 'sign up':
			return redirect(url_for('sign_up'))
		elif request.form.get('action2') == 'sign in':
			return redirect(url_for('sign_in'))

	return render_template("home_page.html")




@app.route("/sign_up", methods = ['GET', 'POST'])
def sign_up():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			UID = login_session['user']['localId']
			user = {"email": email, "password": password, "posts": {}}
			db.child("Users").child(UID).set(user)
			return redirect(url_for('post_something'))
		except:
			error = "Authentication failed"
			return render_template("sign_up.html")
	else:
		return render_template("sign_up.html")




@app.route("/sign_in" , methods = ['GET', 'POST'])
def sign_in():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('post_something'))
		except:
			error = "Eror"
			return render_template("sign_in.html")
	else:
		return render_template("sign_in.html")


@app.route("/post_something"  , methods = ['GET', 'POST'])
def post_something():
	eror = ""
	if request.method == 'POST':
		try:
			post = request.form['post']
			update_posts = {"post" : post}
			UID = login_session['user']['localId']
			db.child("Users").child(UID).child("posts").push(update_posts)
			return redirect(url_for('my_posts'))
		except:
			return render_template("post_something.html")
	else:
		return render_template("post_something.html")

@app.route("/all_posts"  , methods = ['GET', 'POST'])
def all_post():
	user_post = db.child("Users").get().val()
	list_posts = []
	for uid in user_post:
		if "email" in user_post[uid]:
			email = user_post[uid]["email"]
		else:
			email = "no email"
		if "posts" in user_post[uid]:
			posts = user_post[uid]["posts"]
			for post in posts:
				list_posts.append((posts[post]["post"], email))
	return render_template("all_posts.html", list_posts = list_posts) 

#the uid of the person that wrotr this posts
@app.route("/my_posts"  , methods = ['GET', 'POST'])
def my_posts():
	UID = login_session['user']['localId']
	user_post = db.child("Users").child(UID).child("posts").get().val()
	return render_template("my_post.html", user = user_post) 
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)