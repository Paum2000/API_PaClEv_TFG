from app.models.user import User
from typing import Optional, List
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


async def create_user(user_in: UserCreate) -> User:
    # 1. Comprobamos si el email ya existe para no tener errores raros en Mongo
    usuario_existente = await User.find_one(User.email == user_in.email)
    if usuario_existente:
        raise ValueError("Este email ya está registrado.")

    # 2. Comprobamos si el nickname ya existe
    user_exists_nickname = await User.find_one(User.nickname == user_in.nickname)
    if user_exists_nickname:
        raise ValueError("Este nickname ya está registrado.")

    # 2. Convertimos la contraseña plana a un hash
    hashed_pass = get_password_hash(user_in.password)

    # 3. Truco de Pydantic V2: Extraemos los datos del usuario
    # pero EXCLUYENDO la contraseña en texto plano para que no se nos cuele.
    user_data = user_in.model_dump(exclude={"password"})

    # 4. Le inyectamos el hash que acabamos de generar
    user_data["password_hash"] = hashed_pass

    # 5. Creamos el objeto de base de datos y lo guardamos
    db_user = User(**user_data)
    await db_user.insert()

    return db_user

async def get_user(user_id: int) -> Optional[User]:
    # Buscamos directamente por el ID numérico
    return await User.get(user_id)

async def update_user(user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = await User.get(user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    await user.save()
    return user

async def delete_user(user_id: int) -> bool:
    user = await User.get(user_id)
    if user:
        await user.delete()
        return True
    return False

async def update_user_photo(user_id: int, photo_url: str):
    user = await get_user(user_id)
    if user:
        user.user_photo = photo_url
        await user.save()
    return user

async def get_all_users() -> List[User]:
    # Busca y devuelve una lista con absolutamente todos los usuarios
    return await User.find_all().to_list()