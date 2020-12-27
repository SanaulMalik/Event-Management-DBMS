from flask import Flask,render_template, request, url_for, redirect,flash
import sqlite3
from werkzeug.exceptions import abort



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret '

def get_auth():
    con=sqlite3.connect('datab.db')
    con.row_factory = sqlite3.Row
    return con

def check(user_id):
    con=get_auth()
    pw=con.execute('SELECT pw FROM authent WHERE user_id = ?',(user_id,)).fetchone()
    con.close()
    return pw


@app.route('/auth', methods=('GET','POST'))
def authenticate():
    if request.method == 'POST':
        us = request.form['user_id']
        pw= request.form['pw']
        pww = check(us)
        print (pww)
        #return  redirect(url_for('index'))
        if pww['pw'] == pw :
            return  redirect(url_for('index'))
        else :
           render_template('auth.html')
    

    return render_template('auth.html')from flask import Flask
