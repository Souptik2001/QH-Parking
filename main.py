from flask import Flask,render_template, redirect,request, session
from flask_sqlalchemy import SQLAlchemy

log_uname = 'qwertyiooplkj'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/parking"
db = SQLAlchemy(app)

# class parklots(db.Model):
#     sl_no = db.Column(db.Integer, primary_key=True)
#     Uname = db.Column(db.String(80), unique=True, nullable=False)
#     # Name = db.Column(db.String(80), unique=False, nullable=False)
#     Bio = db.Column(db.Integer, unique=False, nullable=False)
#     Non_Bio = db.Column(db.Integer, unique=False, nullable=False)
#     E_waste = db.Column(db.Integer, unique=False, nullable=False)

class login(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.Integer, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard/<string:uname>')
def dashboard(uname):
    if ('user' in session and session['user']==log_uname and uname==log_uname):
        return render_template("map3.html")
    else:
        return redirect('/')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if ('user' in session and session['user']==log_uname):
        return redirect('/')
    page='signup'
    same_u='F'
    same_e='F'
    if (request.method=='POST'):
        Uname = request.form.get('uname')
        Name = request.form.get('name')
        email = request.form.get('email')
        ph_no = request.form.get('ph_no')
        password = request.form.get('pass')
        duplicate_u = login.query.filter_by(Uname=Uname).first()
        duplicate_e = login.query.filter_by(email=email).first()
        # print(duplicate.Uname)
        try:
            try:
                if (duplicate_e.email==email):
                    same_e = 'T'
                    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)
            except:
                if (duplicate_u.Uname==Uname):
                    same_u = 'T'
                    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)
        except:
            entry_login = login(username=Uname, name=Name, password=password, email=email, phone=ph_no)
            db.session.add(entry_login)
            db.session.commit()
    # print(same_u)
    # print(same_e)
    return render_template("signup.html", same_u=same_u, same_e=same_e,page=page)







@app.route('/login', methods=['GET', 'POST'])
def login():
    global log_uname
    if ('user' in session and session['user']==log_uname):
        return redirect('/')
    page='login'
    u_w='F'
    p_w='F'
    if (request.method=='POST'):
        Uname=request.form.get('uname')
        password= request.form.get('pass')
        log_det = login.query.filter_by(Uname=Uname).first()
        try:
            if (log_det.username==Uname and log_det.password==password):
                log_uname=Uname
                session['user']=Uname
            else:
                p_w='T'
                return render_template("login.html", p_w=p_w,page=page)
        except:
            u_w='T'
            return render_template("login.html", u_w=u_w,p_w=p_w,page=page)
        return redirect('/')
    return render_template("login.html", u_w=u_w,p_w=p_w,page=page)



app.run(debug=True)