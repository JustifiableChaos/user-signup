from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True   

def space_checker(item):
    if ' ' in item:
        return True
def len_checker(item):
    if (len(item) < 2) or (len(item) > 20):
        return True
def empty_check(item):
    if (not item) or (item.strip == ''):
        return True
def empty_box_error():
    error = 'Please fill out all required boxes.'
    return redirect('/?error=' + error)
def space_error():
    error = 'One or more fields contains a space'
    return redirect('/?error=' + error)
def len_error():
    error = 'One or more fields is too long or too short. Please make all fields between 3 and 20 characters.'
    return redirect('/?error=' + error)

def username_validator():
    name = request.form['user']
    if empty_check(name):
        empty_box_error()

    elif space_checker(name):
        space_error()

    elif len_checker(name):
        error = 'Your username is too short or long!'
        return redirect('/?error=' + error)
    
def password_validate():
    passy = request.form['pass1']
    passy2 = request.form['pass2']

    if empty_check(passy) or empty_check(passy2):
        empty_box_error()
    
    elif space_checker(passy):
        space_error()
    
    elif len_checker(passy):
        len_error()
    elif passy2 != passy:
        error = 'Your passwords do not match.'
        return redirect('/?error=' + error)

def email_validate():
    mail = request.form['email']
    if mail:
        if ("@" not in mail) or ('.' not in mail):
            error = 'The e-mail you have submitted is not a valid email.'
            return redirect('/?error=' + error)
        elif len_checker(mail):
            len_error()
        elif space_checker(mail):
            space_error()


@app.route("/")
def index():
    encoded_error = request.args.get('error')
    if encoded_error == None:
        encoded_error = ' '
    return render_template('form.html', encoded_error=encoded_error and cgi.escape(encoded_error, quote=True))


@app.route('/submit', methods=['POST'])
def submit_form():
    print("it works")
    email_validate()
    print("it works")
    username_validator()
    print("it works")
    password_validate()
    print("it works")
    encoded_error = request.args.get('error')
    print(encoded_error)

    if encoded_error == None:
        encoded_error = ' '

    return render_template('form.html', encoded_error=encoded_error and cgi.escape(encoded_error, quote=True))
    

app.run()


