from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event
from random import random

import sqlite3 as sql
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(5)


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("""INSERT INTO students (name,addr,city,pin) 
                VALUES (?,?,?,?)""",(nm,addr,city,pin) )

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",rows = rows)

def usersAmount():
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        cur.execute("select * from students")
        
        rows = cur.fetchall();
        con.close()
        amount = len(rows)
        return (amount)

amount = usersAmount()

def findNewAdditions():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    while not thread_stop_event.isSet():
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        cur.execute("select * from students")
        
        rows = cur.fetchall();
        con.close()

        # print ("ROWS PRINTED", rows)

        global amount
        og_Amount = amount

        amount = len(rows)
        # print("++++++ OG_AMOUNT PRINTED +++++",og_Amount)
        # print("++++++ AMOUNT PRINTED +++++",amount)

        data= []
        for row in rows:
                data.append([x for x in row])

        if amount > og_Amount:
            user = data[amount - 1]
            print('+++++++ USER TO BE SENT ++++++++ ',user)
            socketio.emit('newuser', {'user': user}, namespace='/test')
            socketio.sleep(5)
        else:
            socketio.sleep(5)

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(findNewAdditions)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
   app.run(debug = True)