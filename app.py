from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re
import os
from datetime import datetime

app=Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key') 
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='<your_password'
app.config['MYSQL_DB']='LibManage'

mysql= MySQL(app)

        
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        # Check if the user exists
        if user:
            # Directly compare password (no hashing for now)
            if user[2] == password:  # user[2] contains the stored password
                # Store the user's info in the session
                session['logged_in'] = True
                session['username'] = user[1]  # user[1] contains the username
                return redirect(url_for('dashboard'))  # Redirect to the dashboard
            else:
                return redirect(url_for('login'))
        else:
            return 'User not found'
        
    return render_template('login.html')  # Return login page for GET request

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))  # If not logged in, redirect to login

@app.route('/add_book',methods=['GET','POST'])
def add_book():
    cursor = mysql.connection.cursor()
    if request.method=='POST':
        howmany=int(request.form['how_many'])
        
        for i in range(howmany):
            book_name = request.form[f'book_name_{i}']
            author_name = request.form[f'author_name_{i}']
            genre = request.form[f'genre_{i}']
            quantity = int(request.form[f'quantity_{i}'])
            cursor.execute(""" INSERT INTO BOOKS (book_name,author_name,genre,quantity)
                           VALUES (%s,%s,%s,%s)
                           """,(book_name,author_name,genre,quantity))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))


    return render_template('add_book.html')

@app.route('/borrow_book',methods=['GET','POST'])
def borrow_book():
    cursor=mysql.connection.cursor()
    if request.method=='POST':
        member_id=int(request.form['member_id'])
        member_name=request.form['member_name']
        book_id=int(request.form['book_id'])
        book_name=request.form['book_name']
        borrow_date=datetime.now().strftime('%Y-%m-%d')
    
        cursor.execute('SELECT quantity FROM BOOKS WHERE BOOK_ID=%s', (book_id,))
        curr_quantity=cursor.fetchone()

        if( not curr_quantity or curr_quantity[0]==0):
            return "Book Currently not available"
        else:
            cursor.execute("""INSERT INTO CURRENTBORROWED(member_id,member_name,book_id,book_name,borrow_date)
                        VALUES (%s,%s,%s,%s,%s)"""
                        ,(member_id,member_name,book_id,book_name,borrow_date))
            mysql.connection.commit()
            new_quan=curr_quantity[0]-1
            cursor.execute("""UPDATE BOOKS SET QUANTITY=%s 
                        WHERE BOOK_ID=%s
                        """,(new_quan,book_id))
            mysql.connection.commit()
            return redirect(url_for('dashboard'))
    
    return render_template('borrow_book.html')
        
@app.route('/return_book',methods=['GET','POST'])
def return_book():
    cursor=mysql.connection.cursor()
    if(request.method=='POST'):
        member_id=int(request.form['member_id'])
        member_name=request.form['member_name']
        book_id=int(request.form['book_id'])
        book_name=request.form['book_name']
        return_date=datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT BORROW_DATE FROM CURRENTBORROWED WHERE BOOK_ID=%s AND MEMBER_ID=%s',(book_id,member_id))
       
        temp=cursor.fetchone()
        if(not temp):
            return "Book has not been borrowed by user"
        borrow_date=temp[0]

        cursor.execute("""INSERT INTO BORROWHISTORY(member_id,member_name,book_id,book_name,borrow_date,return_date)
                        VALUES (%s,%s,%s,%s,%s,%s)"""
                        ,(member_id,member_name,book_id,book_name,borrow_date,return_date))
        mysql.connection.commit()
        cursor.execute('DELETE FROM CURRENTBORROWED WHERE BOOK_id=%s AND MEMBER_ID=%s',(book_id,member_id))
        mysql.connection.commit()
        cursor.execute('SELECT quantity FROM BOOKS WHERE BOOK_ID=%s', (book_id,))
        curr_quantity=cursor.fetchone()
        new_quan=curr_quantity[0]+1
        cursor.execute("""UPDATE BOOKS SET QUANTITY=%s 
                        WHERE BOOK_ID=%s
                        """,(new_quan,book_id))
        mysql.connection.commit()


        
        return redirect(url_for('dashboard'))
    return render_template("return_book.html")

@app.route('/book_list',methods=['GET'])
def booklist():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT BOOK_ID,BOOK_NAME,AUTHOR_NAME,GENRE FROM BOOKS')
    books=cursor.fetchall()
    return render_template('book_list.html',books=books)

@app.route('/member_list',methods=['GET'])
def memberlist():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT MEMBER_ID,MEMBER_NAME FROM MEMBERS')
    members=cursor.fetchall()
    return render_template('member_list.html',members=members)


@app.route('/current_borrowed',methods=['GET'])
def current_borrowed():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT MEMBER_ID,MEMBER_NAME,BOOK_NAME,BORROW_DATE FROM CURRENTBORROWED')
    current=cursor.fetchall()
    return render_template('current_borrowed.html',current=current)

@app.route('/borrow_history',methods=['GET'])
def borrow_history():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT MEMBER_ID,MEMBER_NAME,BOOK_NAME,BORROW_DATE,RETURN_DATE FROM BORROWHISTORY')
    history=cursor.fetchall()
    return render_template('borrow_history.html',history=history)

@app.route('/add_member',methods=['GET','POST'])
def add_member():
    cursor=mysql.connection.cursor()
    if request.method=='POST':
        howmany=int(request.form['how_many'])
        
        for i in range(howmany):
            member_name=request.form[f'member_name_{i}']
            cursor.execute("""INSERT INTO MEMBERS(member_name)
                           VALUES (%s)
                           """,(member_name,))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_member.html')

@app.route('/advance_search')





@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # Redirect to login

if __name__ == "__main__":
    app.run(debug=True)