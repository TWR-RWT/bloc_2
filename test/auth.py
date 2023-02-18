#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
import jwt
from datetime import datetime, timedelta



def test_jwt(username, secret_key):
    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(hours=24)}, secret_key)
    decode = jwt.decode(token, secret_key, algorithms=['HS256'])
    return decode['user']