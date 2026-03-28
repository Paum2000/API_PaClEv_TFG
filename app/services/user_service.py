from app.models.user import User, UserCreate, UserUpdate
from typing import Optional

async def create_user(user_in: UserCreate) -> User:
    # 1. Sacamos los datos del esquema, excluyendo el password en texto plano
    user_data = user_in.model_dump(exclude={"password"})

    # 2. Simulamos el hash
    user_data["password_hash"] = f"{user_in.password}_hashed"

    # 3. Creamos el documento Beanie
    user = User(**user_data)

    # 4. Lo guardamos en Mongo
    await user.insert()
    return user

async def get_user(user_id: int) -> Optional[User]:
    # En Beanie, .get() busca por el campo _id por defecto
    return await User.get(user_id)

async def update_user(user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = await User.get(user_id)
    if not user:
        return None

    # Solo cogemos los campos que el usuario realmente ha enviado
    update_data = user_in.model_dump(exclude_unset=True)

    # Si ha enviado una contraseña nueva, la hasheamos
    if "password" in update_data:
        update_data["password_hash"] = f"{update_data.pop('password')}_hashed"

    # Actualizamos el objeto Python
    for key, value in update_data.items():
        setattr(user, key, value)

    # Guardamos los cambios en la base de datos
    await user.save()
    return user

async def delete_user(user_id: int) -> bool:
    user = await User.get(user_id)
    if user:
        await user.delete()
        return True
    return False

async def update_user_photo(user_id: int, photo_url: str) -> Optional[User]:
    user = await User.get(user_id)
    if not user:
        return None

    # Actualizamos el campo de la foto y guardamos en la base de datos
    user.user_photo = photo_url
    await user.save()

    return user