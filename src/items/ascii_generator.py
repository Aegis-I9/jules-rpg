def generate_ascii_for_item(item) -> str:
    """
    Gera uma representação de arte ASCII para um item.

    Por enquanto, retorna uma arte pré-definida baseada no tipo do item.
    No futuro, isso poderia ser mais procedural.
    """
    # Importa as classes de item aqui para evitar importação circular
    from .item import Potion, Equipment, Herb, ItemSlot

    if not item.is_identified:
        return """
.-----------.
|           |
|     ?     |
|           |
'-----------'
"""

    if isinstance(item, Potion):
        return """
  .-.
  | |
  | |
  | |
.'   '.
'-----'
"""
    elif isinstance(item, Equipment):
        if item.slot in [ItemSlot.WEAPON]:
            return """
      /\\
     //
    //
O==<)
    \\\\
     \\\\
      \\/
"""
        elif item.slot in [ItemSlot.CHEST, ItemSlot.LEGS, ItemSlot.GLOVES, ItemSlot.BOOTS, ItemSlot.HEAD]:
            return """
.---------.
| H H H H |
| H H H H |
'---------'
"""
    elif isinstance(item, Herb):
        return """
  ,
 / \\
(   )
 \\ /
  '
"""

    # Item genérico
    return """
.-------.
|  o o  |
|   -   |
'-------'
"""
