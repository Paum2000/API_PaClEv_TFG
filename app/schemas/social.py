from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# --- GRUPOS ---

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: Optional[str] = None

class GroupOut(BaseModel):
    # Usamos id: int para que Pydantic lo lea directamente de Beanie
    id: int
    name: str
    admin_id: int
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


# --- MIEMBROS DE GRUPO ---

class GroupMemberAdd(BaseModel):
    # 💡 ESTA ES LA CLASE QUE FALTABA
    user_id: int

class GroupMemberOut(BaseModel):
    id: int
    group_id: int
    user_id: int
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class GroupMemberDetailOut(BaseModel):
    user_id: int
    nickname: str
    user_photo: Optional[str] = None
    role: str  # "admin" o "member"


# --- AMIGOS ---

class FriendRequest(BaseModel):
    friend_id: int

class FriendOut(BaseModel):
    id: int
    user_id_1: int
    user_id_2: int
    status: str
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class FriendUpdate(BaseModel):
    status: str

class FriendDetailOut(BaseModel):
    id: int
    friend_id: int
    nickname: str
    user_photo: Optional[str]
    status: str
    sender_id: int