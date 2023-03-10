from flask import Flask,request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.utils import secure_filename
import base64
import numpy as np

# app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1073741824  # 1 GB
db = SQLAlchemy(app)

# config the tabels
class contact(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(25), nullable = False)
    msg = db.Column(db.String(200), nullable = False)
    date = db.Column(db.String(6),nullable = False)    

class videos(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    video = db.Column(db.LargeBinary, nullable = False)
    titleimg = db.Column(db.LargeBinary, nullable = False)
    course = db.Column(db.String(50), nullable = False)
    date = db.Column(db.String(50), nullable = False)
    slug = db.Column(db.String(50), nullable = False)
    discription = db.Column(db.String(50), nullable = False)

# endpoints
@app.route('/')
def landingpage():
    return render_template('index.html')


@app.route('/home')
def home():
    data = videos.query.all()
    course_name_data = set({})
    courselist_data = []
    img_list =[]
    for course_name in data:
        course_name_data.add(course_name.course)
    
    for item in course_name_data:
        getcourse= videos.query.filter_by(course = item).first()
        courselist_data.append(getcourse)

    for img in courselist_data:
        imgdata = base64.b64encode(img.titleimg)
        imgdata = imgdata.decode('UTF-8')
        img_list.append(imgdata)
    
    return render_template('home.html',video = courselist_data,listimg = img_list)


@app.route('/courses')
def courseshow():
    data = videos.query.all()
    # iinitialize the courses 
    course_name_data = set({})

    # store the filter data
    courselist_data = []

    # image storing list
    img_list = []
    
    
    # filter the data
    for course_name in data:
        course_name_data.add(course_name.course)


    # short the courses
    for item in course_name_data:
        getcourse= videos.query.filter_by(course = item).first()
        courselist_data.append(getcourse)


    for img in courselist_data:
        imgdata = base64.b64encode(img.titleimg)
        imgdata = imgdata.decode('UTF-8')
        img_list.append(imgdata)
    
    return render_template('courses.html',video = courselist_data,listimg = img_list)


@app.route('/courses_video/<string:video_course>', methods = ['GET'])
def coursevideos(video_course):
    data = videos.query.filter_by(course = video_course).all()
    return render_template('videos.html', video = data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact',methods = ['GET','POST'])
def contact_form():
    if request.method =='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('message')
        entry = contact(name = name, email = email, msg = msg, date = datetime.now() ) 
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


@app.route('/blog')
def blog():
    return render_template('blogs.html')


@app.route('/user')
def account():
    return render_template('user.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/upload',methods=['GET','POST'])
def uploadvideos():
    if request.method == 'POST':
        title = request.files['vid_file'].filename
        video = request.files['vid_file'].read()
        thumbnail = request.files['thumbnail'].read()
        coursename = request.form.get('course_name')
        dis = request.form.get('dis')
        
        # slug
        # taking the last sno key
        datasno = videos.query.all()

        last = len(datasno)

        slug_data = f'{coursename[0:15]}{last}{datetime.now()}' 
        # SET GLOBAL max_allowed_packet=1073741824;
        data_push = videos(title=title, video=video, course=coursename, date=datetime.now(), slug=slug_data, discription=dis,titleimg=thumbnail)
                
        db.session.add(data_push)
        db.session.commit()

        # reset id 
        db.session.execute(text('SET @num:=0;UPDATE videos SET sno=@num :=(@num +1); ALTER TABLE videos AUTO_INCREMENT = 1;'))
    return render_template('upload.html')

app.run(debug=True)
