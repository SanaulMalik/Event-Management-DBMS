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

def get_event(event_id,conn):
    #conn = get_db_connection()
    event = conn.execute('SELECT * FROM Event WHERE Event_ID = ?', (event_id,)).fetchone()
    #conn.close()
    return event

def get_students_for_event(event_id,conn):
    #conn = get_db_connection()
    students = conn.execute("SELECT S.Name, S.Phone, S.Roll_no FROM Student S,Works_on W WHERE S.Roll_no = W.Roll_no AND W.Event_ID = ?",(event_id,)).fetchall()
    #conn.close()
    return students

def get_participants_for_event(event_id,conn):
    #conn = get_db_connection()
    participants = conn.execute("SELECT A.Name, A.Phone, A.College, A.Pid FROM Participants A, Participation B WHERE A.Pid = B.Pid AND B.Event_ID = ?",(event_id,)).fetchall()
    #conn.close()
    return participants

def get_venue_for_event(event_id,conn):
    #conn = get_db_connection()
    venue = conn.execute("SELECT V.Venue_ID, V.Venue_name, V.Faculty_incharge, V.Dept FROM Venue V, Event E WHERE V.Venue_ID = E.Venue_ID AND E.Event_ID = ?",(event_id,)).fetchone()
    #conn.close()
    return venue
def get_judges_for_event(event_id,conn):
    judges = conn.execute("SELECT J.Name, J.Judge_ID FROM Judge J WHERE J.Event_ID = ?",(event_id,)).fetchall()
    return judges


def get_winners_for_event(event_id,conn):
    #conn = get_db_connection()
    winners = conn.execute("SELECT P.Pid, P.Name, W.Position FROM Participants P,Winners W WHERE P.Pid = W.Pid AND W.Event_ID = ?",(event_id,) ).fetchall()
    #conn.close()
    return winners

def get_requirements_for_event(event_id,conn):
    requirements = conn.execute("SELECT Requirement, Count FROM Requirements WHERE Event_ID = ?",(event_id,))
    return requirements


def get_student(roll_no):
    conn = get_db_connection()
    student = conn.execute("SELECT Roll_no, Name, Email, Committee, Year, Phone FROM Student WHERE Roll_no = ?",(roll_no,)).fetchone()
    conn.close()
    return student

@app.route('/students/edit/<string:roll_no>',methods = ('GET','POST'))
def editstudent(roll_no):
    student = get_student(roll_no)

    if request.method == 'POST':
        #roll_no = request.form['roll_no']
        name = request.form['name']
        email = request.form['email']
        committee = request.form['committee']
        year = request.form['year']
        phone = request.form['phone']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE Student SET Name = ?'
                         ', Email = ?, Committee = ?, Year = ?, Phone = ? WHERE Roll_no = ?',
                         (name,email,committee,year,phone,roll_no))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
@app.route('/events/<string:event_id>/remove/workson/<string:roll_no>',methods = ('POST',))
def remove_works_on(roll_no,event_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Works_on WHERE Roll_no = ? AND Event_ID = ?', (roll_no,event_id))
    conn.commit()
    conn.close()
    #flash('"{}" was successfully deleted!'.format(student['title']))
    return redirect(url_for('index'))

@app.route('/events/<string:event_id>/remove/participant/<string:pid>',methods = ('POST',))
def remove_participation(event_id,pid):
    conn = get_db_connection()
    conn.execute('DELETE FROM Participation WHERE Event_ID = ? AND Pid = ?',(event_id,pid))
    conn.commit()
    #conn.close()
    return redirect(url_for('event',event_id = event_id))

@app.route('/events/<string:event_id>/remove/winner/<string:pid>',methods = ('POST',))
def remove_winner(event_id,pid):
    conn = get_db_connection()
    conn.execute('DELETE FROM Winners WHERE Event_ID = ? AND Pid = ?',(event_id,pid))
    
    conn.commit()
    conn.close()
    return redirect(url_for('event',event_id = event_id))

@app.route('/students/newstudent',methods = ('GET','POST'))
def newstudent():
    if request.method == 'POST':
            name = request.form['name']
            roll_no = request.form['roll_no']
            email = request.form['email']
            committee = request.form['committee']
            year = request.form['year']
            phone = request.form['phone']

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

@app.route('/judges/newjudge',methods = ('GET','POST'))
def newjudge():
    if request.method == 'POST':
            name = request.form['name']
            judge_id = request.form['judge_id']
            event_id = request.form['event_id']

            if not name:
                flash('Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO Judge VALUES (?,?,?)', (judge_id,name,event_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('addjudge.html')

@app.route('/participants/newparticipant',methods = ('GET','POST'))
def newparticipant():
    if request.method == 'POST':
            name = request.form['name']
            pid = request.form['pid']
            phone = request.form['phone']
            college = request.form['college']

            if not name:
                flash('Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO Participants VALUES (?,?,?,?)', (pid,phone,college,name))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('addparticipant.html')

@app.route('/venues/newvenue',methods = ('GET','POST'))
def newvenue():
    if request.method == 'POST':
            venue_name = request.form['venue_name']
            venue_id = request.form['venue_id']
            faculty_incharge = request.form['faculty_incharge']
            dept = request.form['dept']

            if not venue_name:
                flash('Venue Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO Venue VALUES (?,?,?,?)', (venue_id,venue_name,faculty_incharge,dept))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
    return render_template('addvenue.html')

@app.route('/events/<string:event_id>/newwinner', methods = ('GET','POST'))
def newwinner(event_id):
    if request.method == 'POST':
        pid = request.form['pid']
        position = request.form['position']
        #reception_status = request.form['reception_status']

        conn = get_db_connection()
        participant = conn.execute("SELECT Pid FROM Participation WHERE Pid = ? AND Event_ID = ?",(pid,event_id)).fetchone()
        if not participant:
            flash('Enter a valid participant')
        else:
            conn.execute("INSERT INTO Winners (Pid,Position,Event_ID) VALUES (?,?,?)",(pid,position,event_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('addwinner.html')

@app.route('/events/<string:event_id>/newrequirement', methods = ('GET','POST'))
def newrequirement(event_id):
    if request.method == 'POST':
        requirement = request.form['requirement']
        count = request.form['count']
        #reception_status = request.form['reception_status']

        conn.execute("INSERT INTO Requirements (Requirement,Count, Event_ID) VALUES (?,?,?)",(requirement,count,event_id))
        conn.commit()
        conn.close()
        return redirect(url_for('event',event_id = event_id))
    render_template((url_for('addrequirement.html')))
 

@app.route('/events/<string:event_id>/newparticipant', methods = ('GET','POST'))
def newparticipation(event_id):
    if request.method == 'POST':
        pid = request.form['pid']
        #reception_status = request.form['reception_status']

        conn = get_db_connection()
        participant = conn.execute("SELECT Pid FROM Participants WHERE Pid = ?",(pid,)).fetchone()
        if not participant:
            flash('Enter a valid participant')
        else:
            conn.execute("INSERT INTO Participation (Pid,Event_ID) VALUES (?,?)",(pid,event_id))
            conn.commit()
            return redirect(url_for('event',event_id = event_id))
    return render_template('addparticipation.html')

@app.route('/events/<string:event_id>/newwork', methods = ('GET','POST'))
def newwork(event_id):
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        #reception_status = request.form['reception_status']

        conn = get_db_connection()
        student = conn.execute("SELECT Roll_no FROM Student WHERE Roll_no = ?",(roll_no,)).fetchone()
        if not student:
            flash('Enter a valid student')
        else:
            conn.execute("INSERT INTO Works_on VALUES (?,?)",(event_id,roll_no))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('addwork.html')

        

#events not completed
@app.route('/events/<string:event_id>')
def event(event_id):
    conn = get_db_connection()
    
    event = get_event(event_id,conn)
    students = get_students_for_event(event_id,conn)
    participants = get_participants_for_event(event_id,conn)
    judges = get_judges_for_event(event_id, conn)
    winners = get_winners_for_event(event_id,conn)
    venue = get_venue_for_event(event_id,conn)
    requirements = get_requirements_for_event((event_id,conn))
    
    return render_template('event2.html',event = event, venue = venue,judges = judges,students = students,participants = participants,winners = winners,requirements = requirements)


@app.route("/events")
def allevents():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM Event').fetchall()
    #print (events)
    conn.close()
    return render_template('events2.html', events = events)  

@app.route("/students")
def allstudents():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Student').fetchall()
    #print (events)
    conn.close()
    return render_template('students2.html', students = students)

@app.route("/participants")
def allparticipants():
    conn = get_db_connection()
    participants = conn.execute('SELECT * FROM Participants').fetchall()
    #print (events)
    conn.close()
    return render_template('participants2.html', participants = participants)

@app.route("/venues")
def allvenues():
    conn = get_db_connection()
    venues = conn.execute('SELECT * FROM Venue').fetchall()
    #print (events)
    conn.close()
    return render_template('venues2.html', venues = venues)

@app.route("/winners")
def allwinners():
    conn = get_db_connection()
    winners = conn.execute("SELECT P.Pid, P.Name, P.College, P.Phone, W.Event_ID, W.Position, W.Reception_status FROM Participants P, Winners W, Event E WHERE P.Pid = W.Pid AND W.Event_ID = E.Event_ID")
    conn.commit()
    #conn.close()
    return render_template('winners.html',winners = winners)

@app.route('/judges')
def alljudges():
    conn = get_db_connection()
    judges = conn.execute("SELECT * FROM Judge")
    #conn.close()
    return render_template('judges.html', judges = judges)

@app.route("/")
def  index():
    return render_template('indexf2.html')