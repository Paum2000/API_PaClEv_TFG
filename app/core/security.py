import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# Importamos el modelo de Usuario para poder buscarlo en la BD
from app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "clave_de_respaldo_para_desarrollo_local")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)) # El token caducará en 1 hora

# Configuramos el algoritmo bcrypt,para encriptar contraseñas de forma segura.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara la contraseña en texto plano que envía el usuario en el login
    # con el hash encriptado que tenemos guardado en MongoDB.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Recibe una contraseña en texto plano y devuelve un hash indescifrable.
    # Esta función la usaremos al REGISTRAR un nuevo usuario.
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Crea el token JWT. Recibe un diccionario (normalmente con el ID del usuario)
    # y lo firma digitalmente con nuestra SECRET_KEY.
    to_encode = data.copy()

    # Calculamos cuándo caduca el token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Añadimos la fecha de caducidad (exp) al contenido del token
    to_encode.update({"exp": expire})

    # jwt.encode crea el string final que el frontend guardará
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Esta función es el "escáner de seguridad". Intercepta la petición,
    # lee el token de la cabecera HTTP, lo desencripta y busca al usuario en MongoDB.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales (Token inválido o caducado)",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Intentamos abrir el token con la llave maestra
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 2. Extraemos el ID del usuario (el campo 'sub' que pusimos en auth.py)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        user_id = int(user_id_str)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha caducado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError: # Si el token es inventado o está corrupto
        raise credentials_exception

    # 3. Buscamos al usuario en la BD. Si fue borrado pero su token sigue vivo, lo rechazamos.
    user = await User.find_one(User.id == user_id)
    if user is None:
        raise credentials_exception

    # 4. Devolvemos el objeto Usuario completo.
    return user