from app.models.user import User, UserCreate, UserUpdate
from typing import Optional

async def create_user(user_in: UserCreate) -> User:
    # 1. Preparamos los datos (el ID se generará solo en el modelo)
    user_data = user_in.model_dump(exclude={"password"})
    user_data["password_hash"] = f"{user_in.password}_hashed"

    # 2. Creamos e insertamos. Beanie disparará el 'assign_id' automáticamente
    user = User(**user_data)
    await user.insert()
    return user

async def get_user(user_id: int) -> Optional[User]:
    # Buscamos directamente por el ID numérico
    return await User.get(user_id)

async def update_user(user_id: int, user_in: UserUpdate) -> Optional[User]:
    user = await User.get(user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = f"{update_data.pop('password')}_hashed"

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