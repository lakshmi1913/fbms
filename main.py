from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

main=Flask(__name__)
main.config['MYSQL_HOST']='localhost'
main.config['MYSQL_USER']='root'
main.config['MYSQL_PASSWORD']='mahalakshmiv'
main.config['MYSQL_DB']='feedback'

mysql=MySQL(main)

main.secret_key="super secret key"
@main.route('/')
def signin():
    return render_template('Login.html')


@main.route('/signup')
def signup():
    return render_template('Signup.html')


@main.route('/feedback')
def feedback():
    return render_template('Feedback.html', username=session['username'],name=session['name'],course=session['course'])


@main.route('/signup', methods=['POST'])
def signup_post():
    if request.method=="POST":
        name=request.form.get('username')
        email=request.form.get('email')
        phone=request.form.get('phone')
        college=request.form.get('college')
        course=request.form.get('course')
        password=request.form.get('password')

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO students (name,email,phone,college,course,password) VALUES (%s,%s,%s,%s,%s,%s)", (name,email,phone,college,course,password))
        mysql.connection.commit()
        print(name,email,phone,college,course,password)

        return redirect(url_for('signin'))

@main.route('/signin', methods=['GET','POST'])
def signin_post():
    msg=''
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE email=%s AND password=%s", (username,password))
        record=cur.fetchone()
        if record:
            session['loggedin']=True
            session['name']=record[1]
            session['username']=record[2]
            session['course']=record[5]
            return redirect(url_for('feedback'))
        else:
            msg="Invalid credentials"

        mysql.connection.commit()
    return render_template('Login.html', msg=msg)


@main.route('/feedback', methods=['POST'])
def feedback_post():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        course=request.form.get('course')
        depth=request.form.get('depth')
        prepare=request.form.get('prepare')
        questions=request.form.get('questions')
        comments=request.form.get('comments')

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name,email,course,class_understanding,ins_prepare_org,ins_discus_qs,comments) VALUES (%s,%s,%s,%s,%s,%s,%s)", (name,email,course,depth,prepare,questions,comments))
        mysql.connection.commit()

        return redirect(url_for('feedback'))
    



@main.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    session.pop('name',None)
    session.pop('course',None)
    return redirect(url_for('signin'))