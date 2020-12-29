import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('MainDatabase.db')
    conn.row_factory = sqlite3.Row #row wise access, treats rows like python dictionaries

    return conn


def populateEvents():
    conn = get_db_connection()
    conn.execute("INSERT INTO Event ('Event_ID','Event_name','Venue_ID') VALUES ('E1','Blueprint','ECE11')")
    conn.execute("INSERT INTO Event ('Event_ID','Event_name','Venue_ID') VALUES ('E2','CubeOut','CS20')")
    conn.execute("INSERT INTO Event VALUES ('E101', 'MnM','2020-03-05 12:00:00' , 'inactive','V101')")
    conn.execute("INSERT INTO Event VALUES ('E102', 'Gaming','2020-03-05 12:00:00' , 'inactive','V102')")
    conn.execute("INSERT INTO Event VALUES ('E103', 'Wheels','2020-03-06 09:00:00' , 'inactive','V103')")
    conn.commit()
    conn.close()

def populateStudents():
    conn = get_db_connection()
    conn.execute("INSERT INTO Student VALUES ('B180618CS','Sanaul','sanauls@hotmail.com','PC',3,9995234575)")
    conn.execute("INSERT INTO Student VALUES('B180623CS','Sujoy','sujoyjan2@gmail.com','PC',3,9994532345)")
    conn.execute("INSERT INTO Student VALUES ('B180502CS', 'Nihal','nihal123@gmail.com' , 'program',1999,0562718015)")
    #conn.execute("INSERT INTO Student VALUES ('S102', 'Sanaul','sanaul123@gmail.com' , 'program',2000,05580889066)")
    conn.execute("INSERT INTO Student VALUES ('B180629CS', 'Arjun','arjun123@gmail.com' , 'program',2000,0562718111)")
    conn.commit()
    conn.close()

def populateVenues():
    conn = get_db_connection()
    conn.execute("INSERT INTO Venue VALUES ('ECE11','ECE Seminar hall','Youwillnotsee Future','ECE')")
    conn.execute("INSERT INTO Venue VALUES('S20','CSE Seminar Hall','Binod','CSE')")
    conn.execute("INSERT INTO Venue VALUES ('V101','Aryabhatta','Kuriath','CSE')")
    conn.execute("INSERT INTO Venue VALUES ('V102','Rajpath','Sujoy','ECE')")
    conn.execute("INSERT INTO Venue VALUES ('V103','Basketball Ground','Kumar','EEC')")
    conn.commit()
    conn.close()

def populateJudges():    
    conn = get_db_connection()    
    conn.execute("INSERT INTO Judge VALUES ('J101', 'Malik','E101' )")
    conn.execute("INSERT INTO Judge VALUES ('J102', 'Babu','E102')")
    conn.execute("INSERT INTO Judge VALUES ('J103', 'James','E103')")
    conn.commit()
    conn.close()

def populateParticipants():
    conn = get_db_connection()
    conn.execute("INSERT INTO Participants VALUES ('P101', '055123456','VIT','Aditya' )")
    conn.execute("INSERT INTO Participants VALUES ('P102', '055123478','NITW','Manu' )")
    conn.execute("INSERT INTO Participants VALUES ('P103', '055123401','RAJAGIRI','Akhil' )")
    conn.commit()
    conn.close()

def populateWinners():
    conn = get_db_connection()
    conn.execute("INSERT INTO Winners VALUES ('P101','E101',1,'n')")
    conn.execute("INSERT INTO Winners VALUES ('P102','E102',2,'n')")
    conn.execute("INSERT INTO Winners VALUES ('P103','E103',3,'n')")
    conn.commit()
    conn.close()

def populateParticipation():
    conn = get_db_connection()
    conn.execute("INSERT INTO Participation VALUES ('E101','P101')")
    conn.execute("INSERT INTO Participation VALUES ('E101','P102')")
    conn.execute("INSERT INTO Participation VALUES ('E101','P103')")
    conn.execute("INSERT INTO Participation VALUES ('E102','P101')")
    conn.execute("INSERT INTO Participation VALUES ('E103','P103')")
    conn.execute("INSERT INTO Participation VALUES ('E103','P102')")
    conn.commit()
    conn.close()

def populateWorksOn():
    conn = get_db_connection()
    conn.execute("INSERT INTO Works_on VALUES ('E101','B180618CS')")
    conn.execute("INSERT INTO Works_on VALUES ('E102','B180629CS')")
    conn.execute("INSERT INTO Works_on VALUES ('E103','B180502CS')")
    conn.commit()
    conn.close()

def main():
    populateEvents()
    populateStudents()
    populateVenues()
    populateJudges()
    populateParticipants()
    populateWinners()
    populateParticipation()
    populateWorksOn()

main()