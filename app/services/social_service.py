from typing import List, Tuple, Optional
from beanie.operators import Or, And
from app.models.friend import Friend
from app.models.user import User
from app.schemas.social import FriendDetailOut


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

async def get_my_friends(user_id: int) -> List[FriendDetailOut]:
    # 1. Buscamos todas las relaciones del usuario
    relationships = await Friend.find(Or(
        Friend.user_id_1 == user_id,
        Friend.user_id_2 == user_id
    )).to_list()

    if not relationships:
        return []

    # 2. Obtenemos todos los IDs de los amigos de una sola vez
    friend_ids = [r.user_id_2 if r.user_id_1 == user_id else r.user_id_1 for r in relationships]

    # 3. "Hidratamos" buscando todos los perfiles de golpe
    users = await User.find({"_id": {"$in": friend_ids}}).to_list()
    users_map = {u.id: u for u in users}

    result = []
    for rel in relationships:
        target_id = rel.user_id_2 if rel.user_id_1 == user_id else rel.user_id_1
        friend_user = users_map.get(target_id)

        if friend_user:
            result.append(FriendDetailOut(
                id=rel.id,
                friend_id=friend_user.id,
                nickname=friend_user.user_name,
                user_photo=friend_user.user_photo,
                status=rel.status
            ))
    return result

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