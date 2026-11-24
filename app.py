from flask import Flask, render_template, request, redirect, url_for 
import pymysql 
app = Flask(__name__) 

def get_db_connection(): 
    return pymysql.connect( 
     host='localhost', 
     user='root',          
     password='',          
     database='flask_todo_db', 
     cursorclass=pymysql.cursors.DictCursor 
    ) 
@app.route('/') 
def index(): 
    conn = get_db_connection() 
    with conn.cursor() as cursor: 
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC") 
        tasks = cursor.fetchall() 
    conn.close()
    return render_template('index.html', tasks=tasks) 
@app.route('/add', methods=['POST']) 
def add_task(): 
    title = request.form.get('title') 
    if title: 
        conn = get_db_connection() 
    with conn.cursor() as cursor: 
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,)) 
        conn.commit() 
        conn.close()
        return redirect(url_for('index')) 
@app.route('/complete/<int:task_id>') 
def complete_task(task_id): 
    conn = get_db_connection() 
    with conn.cursor() as cursor: 
        cursor.execute("UPDATE tasks SET status = NOT status WHERE id = %s", 
    (task_id,)) 
        conn.commit() 
        conn.close() 
        return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True)