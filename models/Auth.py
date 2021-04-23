import jwt
from fastapi import HTTPException, Security, status
from passlib.context import CryptContext
from datetime import datetime, timedelta

class AuthHandler():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    secret = "SECRET"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)  
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, payload):
        payload['exp'] = datetime.utcnow() + timedelta(days=1, minutes=0)
        payload['iat'] = datetime.utcnow()

        return jwt.encode(
            payload,
            self.secret,
            algorithm="HS256"
        )
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
