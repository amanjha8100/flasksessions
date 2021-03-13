from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask import session
from flask import redirect,url_for,g,abort

app = Flask(__name__)
app.secret_key='placementcell'


class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

    def __repr__(self):
        return f'<User:{self.username}>'

#Users
users=[]
users.append(User(id=1 , username='Anthony' ,password='password'))
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']
        
        use=[x for x in users if x.username==username]
        if not use:
            return render_template('login.html')
        else:
            user=use[0]
        
            if user and user.password == password:
                session['user_id']=user.id
                return redirect(url_for('work'))
    return render_template('login.html')

@app.route('/work')
def work():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('tester.html')


if __name__ == '__main__':
    app.run(debug=True)