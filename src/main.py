import os
import json
from datetime import datetime
from clientes import Cliente
from reservas import Reserva

# Rutas para datos (se crea carpeta data en la raíz del proyecto)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CLIENTES_FILE = os.path.join(DATA_DIR, "clientes.json")
RESERVAS_FILE = os.path.join(DATA_DIR, "reservas.json")

# Estructuras en memoria
clientes = {}   # id_cliente -> Cliente
reservas = []   # lista de Reserva


# -----------------------
# Utilidades de persistencia
# -----------------------
def ensure_data_dir():
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data():
    ensure_data_dir()
    # Cargar clientes
    if os.path.isfile(CLIENTES_FILE):
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
                for item in raw:
                    c = Cliente(item["id"], item["nombre"], item["email"], item["telefono"])
                    clientes[c.id] = c
            except json.JSONDecodeError:
                print("Advertencia: clientes.json está corrupto o vacío.")
    # Cargar reservas
    if os.path.isfile(RESERVAS_FILE):
        with open(RESERVAS_FILE, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
                for item in raw:
                    r = Reserva(item["id"], item["id_cliente"], item["fecha"], item["hora"], item["servicio"])
                    reservas.append(r)
            except json.JSONDecodeError:
                print("Advertencia: reservas.json está corrupto o vacío.")


def save_data():
    ensure_data_dir()
    # Guardar clientes
    with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"id": c.id, "nombre": c.nombre, "email": c.email, "telefono": c.telefono}
                for c in clientes.values()
            ],
            f,
            ensure_ascii=False,
            indent=2,
        )
    # Guardar reservas
    with open(RESERVAS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"id": r.id, "id_cliente": r.id_cliente, "fecha": r.fecha, "hora": r.hora, "servicio": r.servicio}
                for r in reservas
            ],
            f,
            ensure_ascii=False,
            indent=2,
        )


# -----------------------
# Validaciones
# -----------------------
def validar_id_no_repetido_id_cliente(id_cliente):
    return id_cliente not in clientes


def validar_id_no_repetido_reserva(id_reserva):
    return all(r.id != id_reserva for r in reservas)


def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_hora(hora_texto):
    try:
        datetime.strptime(hora_texto, "%H:%M")
        return True
    except ValueError:
        return False


# -----------------------
# Operaciones del sistema
# -----------------------
def registrar_cliente():
    print("\n--- Registrar Cliente ---")
    id_cliente = input("ID del cliente: ").strip()
    if not id_cliente:
        print(" El ID no puede estar vacío.")
        return
    if not validar_id_no_repetido_id_cliente(id_cliente):
        print(" Error: ID de cliente ya existe.")
        return

    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()

    cliente = Cliente(id_cliente, nombre, email, telefono)
    clientes[id_cliente] = cliente
    save_data()
    print("\n Cliente registrado correctamente.\n")


def registrar_reserva():
    print("\n--- Registrar Reserva ---")
    id_reserva = input("ID de la reserva: ").strip()
    if not id_reserva:
        print(" El ID no puede estar vacío.")
        return
    if not validar_id_no_repetido_reserva(id_reserva):
        print(" Error: ID de reserva ya existe.")
        return

    id_cliente = input("ID del cliente: ").strip()
    if id_cliente not in clientes:
        print(" Error: el cliente no existe.")
        return

    fecha = input("Fecha (AAAA-MM-DD): ").strip()
    if not validar_fecha(fecha):
        print(" Formato de fecha inválido. Use AAAA-MM-DD.")
        return

    hora = input("Hora (HH:MM): ").strip()
    if not validar_hora(hora):
        print(" Formato de hora inválido. Use HH:MM (24h).")
        return

    servicio = input("Servicio: ").strip()

    reserva = Reserva(id_reserva, id_cliente, fecha, hora, servicio)
    reservas.append(reserva)
    save_data()
    print("\n Reserva registrada correctamente.\n")


def listar_clientes():
    print("\n--- Lista de Clientes ---")
    if not clientes:
        print("No hay clientes registrados.\n")
        return

    for cli in clientes.values():
        print(cli)
    print()


def listar_reservas():
    print("\n--- Lista de Reservas (ordenadas por fecha y hora) ---")
    if not reservas:
        print("No hay reservas registradas.\n")
        return

    reservas_ordenadas = sorted(reservas, key=lambda r: (r.fecha, r.hora))
    for r in reservas_ordenadas:
        print(r)
    print()


def buscar_cliente_por_id():
    print("\n--- Buscar Cliente por ID ---")
    id_buscar = input("ID del cliente: ").strip()
    c = clientes.get(id_buscar)
    if c:
        print("\nEncontrado:")
        print(c)
    else:
        print("\nNo se encontró un cliente con ese ID.")
    print()


def buscar_reserva_por_id():
    print("\n--- Buscar Reserva por ID ---")
    id_buscar = input("ID de la reserva: ").strip()
    encontrados = [r for r in reservas if r.id == id_buscar]
    if encontrados:
        for r in encontrados:
            print(r)
    else:
        print("\nNo se encontró reserva con ese ID.")
    print()


def eliminar_reserva():
    print("\n--- Eliminar Reserva ---")
    id_buscar = input("ID de la reserva a eliminar: ").strip()
    for i, r in enumerate(reservas):
        if r.id == id_buscar:
            del reservas[i]
            save_data()
            print("\n Reserva eliminada.\n")
            return
    print("\n No se encontró la reserva.\n")


# -----------------------
# Menú y UI (simple)
# -----------------------
def mostrar_encabezado():
    print("\n" + "=" * 40)
    print("   SISTEMA DE RESERVAS - Odalys")
    print("=" * 40)


def menu():
    load_data()  # Cargar datos al iniciar
    while True:
        mostrar_encabezado()
        print("1. Registrar cliente")
        print("2. Registrar reserva")
        print("3. Listar clientes")
        print("4. Listar reservas")
        print("5. Buscar cliente por ID")
        print("6. Buscar reserva por ID")
        print("7. Eliminar reserva")
        print("8. Salir")
        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_reserva()
        elif opcion == "3":
            listar_clientes()
        elif opcion == "4":
            listar_reservas()
        elif opcion == "5":
            buscar_cliente_por_id()
        elif opcion == "6":
            buscar_reserva_por_id()
        elif opcion == "7":
            eliminar_reserva()
        elif opcion == "8":
            print("\n¡Gracias por usar el sistema!\n")
            break
        else:
            print("\n Opción no válida. Intenta de nuevo.\n")


if __name__ == "__main__":
    menu()
