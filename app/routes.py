from flask import Blueprint, render_template, request, redirect

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "123":
            return redirect('/dashboard')
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')


@main.route('/dashboard')
def dashboard():
    return "Welcome to Dashboard 🚀"