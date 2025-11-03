class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono):
        self.id = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.email}, {self.telefono})"
