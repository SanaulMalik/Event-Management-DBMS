import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create',methods = ('GET','POST'))
def create():
    if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            if not title:
                flash('Title is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (title,content) values (?,?)', (title,content))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('create.html')

def get_db_connection():
    conn = sqlite3.connect('MainDatabase.db')
    conn.row_factory = sqlite3.Row #row wise access, treats rows like python dictionaries

    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_event(event_id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM Event WHERE Event_ID = ?', (event_id,)).fetchone()
    conn.close()
    return event

def get_students_for_event(event_id):
    conn = get_db_connection()
    students = conn.execute("SELECT Name, Phone, Roll_no FROM Student S,Works_on W WHERE S.Roll_no = W.Roll_no AND W.Event_ID = event_id")
    conn.close()
    return students

def get_participants_for_event(event_id):
    conn = get_db_connection()
    participants = conn.execute("SELECT Name, Phone, College FROM Participants A, Participation B WHERE A.Pid = B.Pid AND B.Event_ID = event_id")
    conn.close()
    return participants

@app.route('/students/newstudent',methods = ('GET','POST'))
def newstudent():
    if request.method == 'POST':
            name = request.form['name']
            roll_no = request.form['roll_no']
            email = request.form['email']
            committee = request.form['committee']
            year = request.form['year']
            phone = request.form['year']

            if not name:
                flash('Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO Student VALUES (?,?,?,?,?,?)', (roll_no,name,email,committee,year,phone))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('addstudent.html')

@app.route('/events/newevent', methods = ('GET','POST'))
def newevent():
    if request.method == 'POST':
            event_name = request.form['event_name']
            event_id = request.form['event_id']
            date_time = request.form['date_time']
            status = request.form['status']
            venue_id = request.form['venue_id']
            if not event_name:
                flash('Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO Event VALUES (?,?,?,?,?)', (event_id,event_name,date_time,status, venue_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('addevent.html')



@app.route('/events/<string:event_id>')
def event(event_id):
    event = get_event(event_id)
    students = get_students_for_event(event_id)
    participants = get_participants_for_event(event_id)
    return render_template('event.html',event = event)

@app.route("/events")
def allevents():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM Event').fetchall()
    #print (events)
    conn.close()
    return render_template('events.html', events = events)  

@app.route("/students")
def allstudents():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Student').fetchall()
    #print (events)
    conn.close()
    return render_template('students.html', students = students)

@app.route("/participants")
def allparticipants():
    conn = get_db_connection()
    participants = conn.execute('SELECT * FROM Participants').fetchall()
    #print (events)
    conn.close()
    return render_template('participants.html', participants = participants)

@app.route("/venues")
def allvenues():
    conn = get_db_connection()
    venues = conn.execute('SELECT * FROM Venue').fetchall()
    #print (events)
    conn.close()
    return render_template('venues.html', venues = venues)

@app.route("/")
def  index():
    return render_template('indexf.html')