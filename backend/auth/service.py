# backend/auth/service.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET")
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=120)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + self.access_token_expire
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await self._get_user(username)
        if user is None:
            raise credentials_exception
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self._get_user(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return False
        return user