from sqlalchemy import desc, Table, Column
from sqlalchemy.sql.elements import UnaryExpression


def get_ordering(table: Table, order_value: str) -> Column | UnaryExpression:
    desc_vector = order_value.startswith("-")
    if desc_vector:
        order_value = order_value[1:]
        return desc(getattr(table.c, order_value))
    return getattr(table.c, order_value)
