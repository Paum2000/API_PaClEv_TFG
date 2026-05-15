from beanie.odm.operators.find.comparison import In
from beanie.odm.operators.find.logical import Or

from app.models.group_member import GroupMember
from app.models.list import UserList
from app.schemas.list import ListCreate, ListUpdate

async def create_list(list_in: ListCreate, user_id: int) -> UserList:
    new_list = UserList(**list_in.model_dump(), user_id=user_id)
    return await new_list.insert()

async def get_user_lists(user_id: int) -> list[UserList]:
    membresias = await GroupMember.find(GroupMember.user_id == user_id).to_list()
    group_ids = [m.group_id for m in membresias]
    if not group_ids:
        return await UserList.find(UserList.user_id == user_id).to_list()
    return await UserList.find(Or(UserList.user_id == user_id, In(UserList.group_id, group_ids))).to_list()

async def get_list(list_id: int) -> UserList | None:
    return await UserList.get(list_id)

async def update_list(list_id: int, list_in: ListUpdate) -> UserList | None:
    db_list = await UserList.get(list_id)
    if not db_list:
        return None

    update_data = list_in.model_dump(exclude_unset=True)
    await db_list.set(update_data)
    return db_list

async def delete_list(list_id: int) -> bool:
    db_list = await UserList.get(list_id)
    if db_list:
        await db_list.delete()
        return True
    return False

async def get_lists_by_group(group_id: int):
    return await UserList.find(UserList.group_id == group_id).to_list()