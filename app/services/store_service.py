from beanie.odm.operators.find.comparison import In

from app.models.user import User
from app.models.theme import Theme
from app.models.inventory import UserInventory

PRECIO_COLOR = 100

async def buy_theme(current_user: User, theme_id: int):
    # 1. Buscamos el tema
    theme = await Theme.get(theme_id)
    if not theme:
        return None, "Tema no encontrado"

    # 2. Comprobamos si el tema es gratuito por defecto
    if theme.is_default:
        return None, "Este tema ya está desbloqueado por defecto"

    # 3. Comprobamos si ya lo tiene comprado
    already_owned = await UserInventory.find_one(
        UserInventory.user_id == current_user.id,
        UserInventory.item_type == "THEME",
        UserInventory.item_reference == str(theme_id)
    )
    if already_owned:
        return None, "Ya has desbloqueado este tema"

    # 4. Comprobamos puntos
    if current_user.points < theme.price:
        return None, f"Puntos insuficientes. Necesitas {theme.price} puntos."

    # 5. Cobramos y guardamos (ÉXITO)
    current_user.points -= theme.price
    await current_user.save()

    new_item = UserInventory(
        user_id=current_user.id,
        item_type="THEME",
        item_reference=str(theme_id)
    )
    await new_item.insert()

    # Devolvemos el resultado y None en el error
    return {"message": f"Tema '{theme.name}' comprado con éxito", "new_points": current_user.points}, None


async def buy_color(current_user: User, hex_color: str):
    color_code = hex_color.upper()

    # 1. Comprobamos si ya lo tiene
    already_owned = await UserInventory.find_one(
        UserInventory.user_id == current_user.id,
        UserInventory.item_type == "COLOR",
        UserInventory.item_reference == color_code
    )
    if already_owned:
        return None, "Ya tienes este color en tu inventario"

    # 2. Comprobamos puntos
    if current_user.points < PRECIO_COLOR:
        return None, f"Puntos insuficientes. Cuesta {PRECIO_COLOR} puntos."

    # 3. Cobramos y guardamos (ÉXITO)
    current_user.points -= PRECIO_COLOR
    await current_user.save()

    new_item = UserInventory(
        user_id=current_user.id,
        item_type="COLOR",
        item_reference=color_code
    )
    await new_item.insert()

    return {"message": f"Color {color_code} desbloqueado con éxito", "new_points": current_user.points}, None

async def get_user_inventory(current_user: User):
    # 1. OBTENER TEMAS
    # Temas gratuitos para todos
    default_themes = await Theme.find(Theme.is_default == True).to_list()

    # Todos los items del usuario en el inventario
    inventory_items = await UserInventory.find(UserInventory.user_id == current_user.id).to_list()

    # Filtramos los IDs de los temas que ha comprado
    purchased_theme_ids = [
        int(item.item_reference)
        for item in inventory_items
        if item.item_type == "THEME"
    ]

    purchased_themes = []
    if purchased_theme_ids:
        # Buscamos los objetos Theme completos para esos IDs
        purchased_themes = await Theme.find(In(Theme.id, purchased_theme_ids)).to_list()

    # Unimos ambos (evitando duplicados por si acaso)
    all_themes = default_themes + purchased_themes

    # 2. OBTENER COLORES
    # Filtramos las referencias de tipo COLOR
    unlocked_colors = [
        item.item_reference
        for item in inventory_items
        if item.item_type == "COLOR"
    ]

    return {
        "themes": all_themes,
        "colors": unlocked_colors
    }