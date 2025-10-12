@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    error = []
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.data['uname']
            password = form.data['pword']
            confirm = form.data['confirm']
            user_match = User.query.filter_by(username=username).first()
            if user_match:
                message = 'User already exists!'
            else:
                us = User(username=username, password=password)
                db.session.add(us)
                db.session.commit()
                message = f"Successfully registered {username}!"
        else:
            message = 'Registration failed'
    return render_template('register.html', message=message, error=error, form=form)