from app.models.theme import Theme, ThemeCreate, ThemeUpdate
from typing import List, Optional

async def create_theme(theme_in: ThemeCreate) -> Theme:
    theme = Theme(**theme_in.model_dump())
    await theme.insert()
    return theme

async def get_all_themes() -> List[Theme]:
    # Para traer toda la colección en Beanie usamos .find_all()
    return await Theme.find_all().to_list()

async def update_theme(theme_id: int, theme_in: ThemeUpdate) -> Optional[Theme]:
    theme = await Theme.get(theme_id)
    if not theme:
        return None

    update_data = theme_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(theme, key, value)

    await theme.save()
    return theme

async def delete_theme(theme_id: int) -> bool:
    theme = await Theme.get(theme_id)
    if theme:
        await theme.delete()
        return True
    return False