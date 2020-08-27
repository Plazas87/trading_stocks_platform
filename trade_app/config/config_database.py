from enum import Enum


class DataBaseConnection(Enum):
    """Contiene los campos necesarios para establecer conexión con la base de datos"""
    user = 0
    password = 1
    address = 2
    port = 3
    database = 4
