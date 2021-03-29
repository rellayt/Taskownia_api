import datetime
import jwt
import bcrypt

def createJwtToken(id):
    payload = {
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token

def hashPassword(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def comparePassword(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)