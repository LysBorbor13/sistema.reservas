class Reserva:
    def __init__(self, id_reserva, id_cliente, fecha, hora, servicio):
        self.id = id_reserva
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.hora = hora
        self.servicio = servicio

    def __str__(self):
        return f"Reserva {self.id}: Cliente {self.id_cliente}, {self.fecha} {self.hora}, Servicio: {self.servicio}"
