from fastapi import APIRouter
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    return {"message": "Endpoint de edición listo. Lógica pendiente."}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": f"Usuario {user_id} eliminado. Lógica pendiente."}