from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True   

error_dict = {'user': {'space': 'No spaces allowed!', 'empty': 'Please fill out all required boxes.', 'len': 'This box must be between 2 and 20 characters.',}, 'password': {'space': 'No spaces allowed!', 'empty': 'Please fill out all required boxes.', 'len': 'This box must be between 2 and 20 characters.','match': "Your passwords don't match!",},
 'email': {'space': 'No spaces allowed!', 'empty': 'Please fill out all required boxes.', 'len': 'This box must be between 2 and 20 characters.','invalid': 'The email you entered is invalid.'}, '':''}

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
    error = 'empty'
    return error
def space_error():
    error = 'space'
    return error
def len_error():
    error = 'len'
    return error

def username_validator():
    name = request.form['user']
    error = ''
    if empty_check(name):
        error += 'user empty'
    
    if space_checker(name):
        error += 'user space'

    if len_checker(name):
        error += 'user len'
    
    if error != '':
        return False, error

    else:
        return True, ''

            
        
    
def password_validate():
    passy = request.form['pass1']
    passy2 = request.form['pass2']
    error = ''
    if empty_check(passy) or empty_check(passy2):
        error += 'password empty'
    
    if space_checker(passy):
        error += 'password space'
    
    if len_checker(passy):
        error += 'password len'
    
    if passy2 != passy:
        error += 'password match'
    
    if error != '':
        return False, error
    else:
        return True, ''


def email_validate():
    error = ''
    mail = request.form['email']
    if mail != None and mail != '':
        if (("@" not in mail) or ('.' not in mail)):
            print(mail)
            error += 'email invalid'
        if len_checker(mail):
            error += 'email len'
        if space_checker(mail):
            error += 'email space'
        if error != '':
            return False, error
        else:
            return True, ''
    else:
        return True, ''


@app.route("/")
def index():
    encoded_error = request.args.get('error')
    if encoded_error == None:
        encoded_error = ''
    return render_template('form.html', encoded_error=encoded_error and cgi.escape(encoded_error, quote=True), error_dict= error_dict)


@app.route('/submit', methods=['POST'])
def submit_form():
    error = ''
    tf, err = email_validate()
    if tf == False:
        error += '--' + err
    tf, err = username_validator()
    if tf == False:
        error += '--' + err
            

    tf, err = password_validate()
    if tf == False:
        error += '--' + err

    if error != '':
        return redirect('/?error=' + error)

    encoded_error = request.args.get('error')
    print(encoded_error)

    if encoded_error == None:
        encoded_error = ''

    return render_template('form.html', encoded_error=encoded_error and cgi.escape(encoded_error, quote=True), error_dict=error_dict)
    

app.run()


