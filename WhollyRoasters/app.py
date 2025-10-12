from flask import Flask, render_template, request, jsonify
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
with app.app_context():

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), index=True, unique=True)
        password = db.Column(db.String(128))
    

    def __repr__(self):
        return f'User {self.username}'
    db.create_all()
   #User1 = User(username='testuser', password='testpass')
   #db.session.add(user1)
   #db.session.commit()

    class ShippingInfo(db.Model):
        
        ship_id = db.Column(db.Integer, primary_key=True)
        full_name = db.Column(db.String(100), nullable=False)
        address = db.Column(db.String(200), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'ShippingInfo {self.full_name} address is {self.address}'
    db.create_all()
    ShippingInfo.query.delete()  # Clear existing data


@app.route('/', methods=['GET'])
def welcome():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/shop', methods=['GET'])
def shop():
    types = ['12oz Medium Roast', '24oz French Roast', '96oz Whole Beans']
    return render_template('shop.html', types=types)

@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    user_match = User.query.filter_by(username=json_data['uname']).first()
    if user_match:
      return jsonify({'Message': 'Username already exists!'})
    new_user = User(username = json_data['uname'], password = json_data['pword'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Message': 'A new user was created!'}) 
   #message = ""
   #error = []
   #form = RegistrationForm()
   #if request.method == 'POST':
   #    # Handle registration logic here
   #    if form.validate_on_submit():
   #        user_match = User.query.filter_by(username=form.data['uname']).first()
   #        us = User(
   #            username = form.data['uname'],
   #            password = form.data['pword']
   #        )
   #                    
   #        if user_match:
   #            message = 'Username already exists'
   #        else:
   #            message = f"Successfully registered {form.data['uname']}!"
   #            # Save the user to the database
   #            db.session.add(us)
   #            db.session.commit()
   #            message = f"Successfully registered {form.data['uname']}!"
   #    else:
   #        message = 'Registration failed'
        #PREVIOUS CODE 
        #if not username:
        #    error.append("Username is required.")
        #if not password:
        #    error.append("Password is required.")
        #if not confirm:
        #    error.append("Password confirmation is required.")
        #if len(username) < 3:
        #    error.append("Username must be at least 3 characters long.")
        #if password != confirm:
        #    error.append("Passwords do not match.")
        
        #if error:
        #    message = "Registration failed"
        #else:
        #    message = f"Successfully registered {username}"
   #return render_template('register.html', message=message, error= error, form=form)

@app.route("/admin", methods=["GET"])
def admin():
    db_users = User.query.all()
    db_shippers = ShippingInfo.query.all()
    users= []
    for db_user in db_users:
        users.append({
            "username": db_user.username,
            "id": db_user.id
        })
    shippers = []
    for db_shipper in db_shippers: 
        shippers.append({
            "full_name": db_shipper.full_name,
            "address": db_shipper.address,
            "user_id": db_shipper.user_id
        })
    return jsonify({
        "users": users,
        "shippers": shippers
    })
