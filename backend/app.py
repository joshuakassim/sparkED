from flask import request, jsonify
from werkzeug.security import generate_password_hash
from config import app, db
from models import User

# Routes

# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get entered information and look for user
    username, password = request.get_json().values()
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()

    # Check if passwords match and log the user in if they do
    if user.passwords_match(password):
        return {'msg': "Login succesful"}

    return {'error': 'Invalid username or password'}, 401

# Register route
@app.route('/register', methods=['POST'])
def register():
    # Get entered information
    name, username, password = request.get_json().values()

    # Check if the user already exists
    user_exists = User.query.filter_by(username=username).count()
    if user_exists:
        return {'error':'User already exists'}, 400

    # Create a new user
    try:
        user = User(name, username, password)
        db.session.add(user)
        db.session.commit()
        return user.to_json()
    except Exception as e:
        return {'error':str(e)}, 500



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)