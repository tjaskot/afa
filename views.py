from flask import Flask, render_template, request, url_for, redirect, session
import variables

# Application Generated Routes
# @app.route('/')
def index():
    # TODO: Need to update for if session is active, then redirect for home?
    if 'username' in session:# and db.query.filter_by('id') != 'admin':
        return 'Logged in as {}'.format(session['username'])
    elif 'username' is 'admin':
        db.get_pass() #refer to something like this for password
        db.query.filter_by('password')
        return 'logged in'
    return redirect(url_for('home'))

# Stay-Alive verification
# @app.route('/hello', methods=['GET'])
def hello():
    return "Return 200"

# @app.route('/home')
def home():
    return render_template('index.html', bkgrnd1 = variables.bkgrnd1, bkgrnd2d0 = variables.bkgrnd2d0, bkgrnd2d1 = variables.bkgrnd2d1, bkgrnd3 = variables.bkgrnd3, navBarEl="homeLi", sideBarEl="sideHomeLi")

# @app.route('/generate', methods=['POST', 'GET'])
def generate():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = "Invalid username/password"
            return redirect(url_for('.not_found', error = error))
    return render_template('generate.htm', navBarEl="generateLi", sideBarEl="sideGenerateLi")

# @app.route('/contacts')
#Syntax of python flask does not require variable from redirect to be passed into the below def function
def contacts():
    sendEmail = 'false'
    if sendEmail == 'true':
        requestor = request.form['siteOwner']
        #Change the string into list for list concatanation later in function
        recipient = [requestor]
        cc = ['trevor186@msn.com']
        bcc = []
        sender = 'trevor186@msn.com'
        msg = MIMMultipart('alternative')
        msg['Subject'] = 'Website Request'
        msg['From'] = sender
        msg['To'] = ",".join(recipient)
        msg['CC'] = ",".join(cc)
        msg['BCC'] = ",".join(bcc)
        recipient += cc + bcc
        #More detail in e-mail content
        email_body = None
        email_body_header = ' '
        email_body_header += '<html><head></head><body>'
        email_body_header += '<style type="text/css"></style>'
        email_body_header += '<br><h2>Hey</h2><p>Email Header</p><br><p>Requested Info:</p><br>'
        email_body_content = ' '
        email_body_content += '<p> + requestor + </p>'
        email_body_footer = ' '
        email_body_footer += '<br>Thank you.'
        email_body_footer += '<br><p>R/</p><p>Flower Support</p><br>'
        html = str(email_body_header) + str(email_body_content) + str(email_body_footer)
        part = MIMEText(html, 'html')
        msg.attach(part)
        s = smtplib.SMTP('mailhost.afa.com')
        s.sendmail(sender, recipient, msg.as_string())
        s.quit()

    return render_template('contacts.htm', poc1 = variables.poc1, poc2 = variables.poc2, navBarEl="contactsLi", sideBarEl="sideContactsLi")

# @app.route('/about')
def about():
    return render_template('about.htm', navBarEl="aboutLi", sideBarEl="sideAboutLi")

# @app.route('/datafunction')
def datafunction():
    myVal = "myDataValue"
    return myVal

# @app.route('/unauthorized')
# TODO: next step to add pass in object that returns "hey <user> you're not auth"
def unauthorized():
    return "Hey gotta figure out how to login :)"
