import re
from app import db, bcrypt
from app.models import User



class BaseService:
    def __init__(self):
        self.email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def validate_email(self, email):
        if not re.match(self.email_regex, email):
            return False
        return True

class UserService(BaseService):
    def __init__(self):
        super().__init__()

    def register_user(self, data):
        email = data.get('email')
        password = data.get('password')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        phoneNum = data.get('phoneNum')
        confirmPassword = data.get('confirmPassword')

        if not self.validate_email(email):
            return {"error": "Invalid email address!"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "User already exists!"}, 400

        if password != confirmPassword:
            return {"error": "Passwords do not match!"}, 400

        if len(password) < 8:
            return {"error": "Password must be at least 8 characters long!"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password, firstName=firstName, lastName=lastName, phoneNum=phoneNum)
        db.session.add(new_user)
        db.session.commit()
            
        return {"message": "User registered successfully"}, 201
    
    def login_user(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not self.validate_email(email):
            return {"error": "Invalid email address!"}, 400
        
        if not user:
            return {"error": "User does not exist!"}, 400

        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Wrong password!"}, 400

        return {"message": "User logged in successfully"}, 200
    
