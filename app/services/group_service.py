from typing import List, Tuple, Optional
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User

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