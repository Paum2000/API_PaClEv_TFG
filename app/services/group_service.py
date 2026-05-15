from typing import List, Tuple, Optional

from beanie.odm.operators.find.comparison import In

from app.models.event import Event
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.schedule import WeekSchedule
from app.models.task import Task
from app.models.user import User
from app.models.list import UserList
from app.schemas.social import GroupMemberDetailOut



async def create_group(current_user: User, name: str) -> Group:
    # 1. Crear el grupo
    new_group = Group(name=name, admin_id=current_user.id)
    await new_group.insert()

    # 2. El admin se convierte en el primer miembro automáticamente
    first_member = GroupMember(group_id=new_group.id, user_id=current_user.id)
    await first_member.insert()

    return new_group

async def add_member_to_group(current_user: User, group_id: int, new_user_id: int) -> Tuple[bool, Optional[str]]:
    group = await Group.get(group_id)

    # 1. Solo el admin puede añadir gente
    if not group or group.admin_id != current_user.id:
        return False, "No tienes permisos para añadir miembros"

    # 2. Verificar si ya está en el grupo
    exists = await GroupMember.find_one(
        GroupMember.group_id == group_id,
        GroupMember.user_id == new_user_id
    )
    if exists:
        return False, "El usuario ya pertenece al grupo"

    # 3. Añadir miembro
    member = GroupMember(group_id=group_id, user_id=new_user_id)
    await member.insert()
    return True, None

async def update_group(current_user: User, group_id: int, new_name: str) -> Tuple[Optional[Group], Optional[str]]:
    group = await Group.get(group_id)
    if not group or group.admin_id != current_user.id:
        return None, "No autorizado o grupo no encontrado"

    group.name = new_name
    await group.save()
    return group, None

async def delete_group(current_user: User, group_id: int) -> Tuple[bool, Optional[str]]:
    group = await Group.get(group_id)
    if not group or group.admin_id != current_user.id:
        return False, "No autorizado"

    # Borrado en cascada: Borramos todos los miembros y luego el grupo
    await GroupMember.find(GroupMember.group_id == group_id).delete()
    await group.delete()
    return True, None

async def get_group (group_id: int) -> Group:
    return await Group.get(group_id)

async def get_my_groups(user_id: int) -> List[Group]:
    # 1. Buscamos todas las membresías de este usuario
    membresias = await GroupMember.find(GroupMember.user_id == user_id).to_list()

    # Si no está en ningún grupo, devolvemos una lista vacía y nos ahorramos trabajo
    if not membresias:
        return []

    # 2. Extraemos solo los IDs de los grupos en los que participa
    group_ids = [m.group_id for m in membresias]

    # 3. Buscamos todos esos grupos de golpe en la base de datos
    mis_grupos = await Group.find(In(Group.id, group_ids)).to_list()

    return mis_grupos

async def get_group_members(group_id: int) -> List[GroupMember]:
    # Debuelbe la lista de miembros de un grupo específico.
    return await GroupMember.find(GroupMember.group_id == group_id).to_list()

async def remove_member_from_group(current_user: User, group_id: int, user_to_remove_id: int) -> Tuple[bool, Optional[str]]:
    group = await Group.get(group_id)
    if not group:
        return False, "Grupo no encontrado"

    # Lógica de permisos:
    # 1. El admin puede eliminar a cualquier miembro.
    # 2. Un usuario puede eliminarse a sí mismo (abandonar grupo).
    es_admin = group.admin_id == current_user.id
    es_uno_mismo = current_user.id == user_to_remove_id

    if not (es_admin or es_uno_mismo):
        return False, "No tienes permisos para realizar esta acción"

    # No permitimos que el admin se elimine a sí mismo si quieres que el grupo no quede huérfano
    # (Opcional: podrías obligar a borrar el grupo o ceder el admin)
    if es_uno_mismo and es_admin:
        return False, "El administrador no puede abandonar el grupo. Debes eliminar el grupo o ceder el mando."

    member_record = await GroupMember.find_one(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_to_remove_id
    )

    if not member_record:
        return False, "El usuario no pertenece a este grupo"

    await member_record.delete()
    return True, None

async def is_user_in_group(user_id: int, group_id: int) -> bool:
    # Verifica si un usuario es miembro de un grupo específico.
    from app.models.group_member import GroupMember

    member = await GroupMember.find_one(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    )
    return member is not None
async def get_hydrated_group_members(group_id: int) -> List[GroupMemberDetailOut]:
    # 1. Sacamos las membresías de la base de datos
    membresias = await GroupMember.find(GroupMember.group_id == group_id).to_list()

    if not membresias:
        return []

    # 2. Extraemos los IDs de los usuarios
    user_ids = [m.user_id for m in membresias]

    # 3. Traemos todos los perfiles de golpe (¡Optimizado!)
    users = await User.find(In(User.id, user_ids)).to_list()
    users_map = {u.id: u for u in users}

    # 4. Mezclamos los datos (Membresía + Perfil)
    return [
        GroupMemberDetailOut(
            user_id=m.user_id,
            nickname=user.nickname,
            user_photo=user.user_photo,
            role=m.role
        )
        for m in membresias
        if (user := users_map.get(m.user_id))
    ]




