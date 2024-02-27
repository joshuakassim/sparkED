from flask import redirect, request, session
from werkzeug.security import generate_password_hash
from config import app, db
from models import User, Flashcard


# Log user in
@app.route('/login', methods=['POST'])
def login():
    """Log user in"""
    
    # Get entered information and look for user
    username, password = request.get_json().values()
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()

    # Check if passwords match and log the user in if they do
    if user.passwords_match(password):
        session['user_id'] = user.id
        return {'msg': "Login succesful"}

    return {'error': 'Invalid username or password'}, 401


# Log user out
@app.route('/logout', methods=['POST'])
def logout():
    """Log user out"""
    session['user_id'] = None
    redirect('/login')
    return {'msg':'Logged out'}


# Register new user
@app.route('/register', methods=['POST'])
def register():
    """Register a new user"""

    # Get entered user information
    name, username, password = request.get_json().values()

    # Check if the user already exists
    user_exists = db.session.execute(db.select(User).filter_by(username=username)).scalar_one().count()
    if user_exists:
        return {'error':'User already exists'}, 400

    # Create a new user
    user = User(name, username, password)
    try:
        db.session.add(user)
        db.session.commit()
        return user.to_json()
    except Exception as e:
        return {'error':str(e)}, 500

    # Set session
    session['user_id'] = user.id

    return {'msg':"Registration successful"},


# Update user profile
@app.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""

    # Get entered user information
    name, username, password = request.get_json().values()

    # Look for user in the database
    user = db.session.execute(db.select(User).filter_by(id=session['user_id'])).scalar_one()
    
    # Update user
    try:
        user.__init__(name, username, password)
        db.session.commit()
    except Exception as e:
        return {'error':str(e)}, 500

    return {'msg':'Profile updated'}
    
    
# Get user profile
@app.route('/profile', methods=['GET'])
def get_profile():
    """Get logged in users profile"""

    # Look for the user in the database and return their information in JSON format
    user = db.session.execute(db.select(User).filter_by(id=session['user_id'])).scalar_one()
    return user.to_json()


# Create flashcard
@app.route('/flashcards', methods=['POST'])
def create_flashcard():
    """Create a flashcard"""

    # Get entered flashcard information
    question, answer, category = request.get_json().values()

    # Create flashcard
    try:
        flashcard = Flashcard(question, answer, category, session['user_id'])
        db.session.add(flashcard)
        db.session.commit()
    except Exception as e:
        return {'error':str(e)}

    return {'msg':'Flashcard added'}, 201


# Update flashcard
@app.route('/flashcards/<int:id>', methods=['PUT'])
def update_flashcard(id):
    """Update a flashcard"""

    # get updated flashcard information
    question, answer, category = request.get_json().values()

    # Look for the flashcard in the database
    flashcard = db.session.execute(db.select(Flashcard).filter_by(id=id)).scalar_one()

    # Update the flashcard
    try:
        flashcard.update(id, question, answer, category)
        db.session.commit()
    except Exception as e:
        return {'error':str(e)}

    return {'msg':'Flashcard updated'}, 201


# Delete a flashcard
@app.route('/flashcards/<int:id>', methods=['DELETE'])
def delete_flashcard(id):
    """Delete a flashcard"""

    # Look for the flashcard in the database
    flashcard = db.session.execute(db.select(Flashcard).filter_by(id=id)).scalar_one()

    # Delete the flashcard
    try:
        db.session.delete(flashcard)
        db.session.commit()
    except Exception as e:
        return {'error': str(e)}

    return  {'msg':'Flashcard deleted'}

# Study flashcards
@app.route('/study', methods=['GET', 'POST', 'PUT', 'DELETE'])
def study():
    """Study the flashcards that have been created buy the user"""

    # Look for all the users flashcards
    flashcards = db.session.execute(db.select(Flashcard).filter_by(user_id=session['user_id'])).scalars()

    # Convert them to JSON format
    json_flashcards = list(map(lambda x: x.to_json(), flashcards))
    return {'flashcards': json_flashcards}


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)