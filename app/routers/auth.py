from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Un pequeño esquema para definir cómo se devuelve el token
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Ruta para iniciar sesión.
    # OAuth2 estandariza que el campo se llame 'username',
    # pero nosotros ahí pediremos al usuario que meta su 'email'.

    # 1. Buscamos al usuario en la base de datos por su email
    user = await User.find_one(User.email == form_data.username)

    # 2. Si no existe, o si la contraseña no coincide con el hash no entra
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}, # Cabecera estándar de error OAuth2
        )

    # 3. Si todo es correcto, creamos el token.
    # sub es el estándar en JWT para identificar a quién pertenece el token.
    access_token = create_access_token(data={"sub": str(user.id)})

    # 4. Devolvemos el token al frontend
    return {"access_token": access_token, "token_type": "bearer"}