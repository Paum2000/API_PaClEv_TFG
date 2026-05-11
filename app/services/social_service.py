from typing import List, Tuple, Optional
from beanie.operators import Or, And
from app.models.friend import Friend
from app.models.user import User

async def send_friend_request(current_user: User, friend_id: int) -> Tuple[Optional[Friend], Optional[str]]:
    # 1. No puedes ser tu propio amigo (sería raro)
    if current_user.id == friend_id:
        return None, "No puedes enviarte una solicitud a ti mismo"

    # 2. Verificar que el usuario destino existe
    target_user = await User.get(friend_id)
    if not target_user:
        return None, "El usuario no existe"

    # 3. Verificar si ya existe una relación (en cualquier sentido) usando operadores explícitos
    existing = await Friend.find_one(Or(
        And(Friend.user_id_1 == current_user.id, Friend.user_id_2 == friend_id),
        And(Friend.user_id_1 == friend_id, Friend.user_id_2 == current_user.id)
    ))

    if existing:
        return None, "Ya existe una solicitud o relación de amistad"

    # 4. Crear solicitud PENDIENTE
    new_request = Friend(
        user_id_1=current_user.id,
        user_id_2=friend_id,
        status="PENDIENTE"
    )
    await new_request.insert()
    return new_request, None

async def accept_friend_request(current_user: User, request_id: int) -> Tuple[bool, Optional[str]]:
    # 1. Buscamos la solicitud por ID
    request = await Friend.get(request_id)

    # 2. Verificamos que exista y que el usuario actual sea el receptor
    if not request or request.user_id_2 != current_user.id:
        return False, "Solicitud no encontrada o no tienes permiso"

    # 3. Actualizamos el estado a ACEPTADO
    request.status = "ACEPTADO"
    await request.save()
    return True, None

async def get_my_friends(current_user: User) -> List[Friend]:
    # 1. Buscamos relaciones donde el usuario sea parte (id_1 o id_2) y esté aceptada
    return await Friend.find(And(
        Or(Friend.user_id_1 == current_user.id, Friend.user_id_2 == current_user.id),
        Friend.status == "ACEPTADO"
    )).to_list()

async def remove_friendship(current_user: User, friend_id: int) -> Tuple[bool, Optional[str]]:
    # 1. Buscamos la relación en cualquier dirección (bidireccional)
    relationship = await Friend.find_one(Or(
        And(Friend.user_id_1 == current_user.id, Friend.user_id_2 == friend_id),
        And(Friend.user_id_1 == friend_id, Friend.user_id_2 == current_user.id)
    ))

    # 2. Si no existe, devolvemos error
    if not relationship:
        return False, "No existe una relación de amistad con este usuario"

    # 3. Eliminamos el documento de la colección (borrado físico)
    await relationship.delete()
    return True, None