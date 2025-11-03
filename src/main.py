import os
import json
from datetime import datetime
from clientes import Cliente
from reservas import Reserva

# Rutas para datos
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CLIENTES_FILE = os.path.join(DATA_DIR, "clientes.json")
RESERVAS_FILE = os.path.join(DATA_DIR, "reservas.json")

clientes = {}     # HashMap: id_cliente -> Cliente
reservas = []     # Lista de Reserva


# =============================
#   UTILIDADES DE ARCHIVOS
# =============================
def ensure_data_dir():
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data():
    ensure_data_dir()

    # ----- CLIENTES -----
    if os.path.isfile(CLIENTES_FILE):
        try:
            with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for c in data:
                    cliente = Cliente(c["id"], c["nombre"], c["email"], c["telefono"])
                    clientes[cliente.id] = cliente
        except:
            print("⚠️ Advertencia: clientes.json está vacío o dañado.")

    # ----- RESERVAS -----
    if os.path.isfile(RESERVAS_FILE):
        try:
            with open(RESERVAS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for r in data:
                    reserva = Reserva(r["id"], r["id_cliente"], r["fecha"], r["hora"], r["servicio"])
                    reservas.append(reserva)
        except:
            print("⚠️ Advertencia: reservas.json está vacío o dañado.")


def save_data():
    ensure_data_dir()

    # Guardar CLIENTES
    with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"id": c.id, "nombre": c.nombre, "email": c.email, "telefono": c.telefono}
                for c in clientes.values()
            ],
            f,
            ensure_ascii=False,
            indent=2
        )

    # Guardar RESERVAS
    with open(RESERVAS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"id": r.id, "id_cliente": r.id_cliente, "fecha": r.fecha, "hora": r.hora, "servicio": r.servicio}
                for r in reservas
            ],
            f,
            ensure_ascii=False,
            indent=2
        )


# =============================
#        VALIDACIONES
# =============================
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except:
        return False


def validar_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except:
        return False


# =============================
#     FUNCIONES DEL SISTEMA
# =============================
def registrar_cliente():
    print("\n--- Registrar Cliente ---")
    id_cliente = input("ID del cliente: ").strip()

    if not id_cliente:
        print("❌ El ID no puede estar vacío.")
        return

    if id_cliente in clientes:
        print("❌ Ese ID de cliente ya existe.")
        return

    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()

    cliente = Cliente(id_cliente, nombre, email, telefono)
    clientes[id_cliente] = cliente
    save_data()

    print("\n✅ Cliente registrado correctamente.\n")


def editar_cliente():
    print("\n--- Editar Cliente ---")
    id_cliente = input("ID del cliente a editar: ").strip()

    if id_cliente not in clientes:
        print("\n❌ No existe un cliente con ese ID.\n")
        return

    cliente = clientes[id_cliente]

    print("\nCliente actual:")
    print(cliente)

    print("\nDeja en blanco los campos que NO quieras cambiar.\n")

    nuevo_nombre = input(f"Nombre ({cliente.nombre}): ").strip()
    nuevo_email = input(f"Email ({cliente.email}): ").strip()
    nuevo_telefono = input(f"Teléfono ({cliente.telefono}): ").strip()

    if nuevo_nombre:
        cliente.nombre = nuevo_nombre
    if nuevo_email:
        cliente.email = nuevo_email
    if nuevo_telefono:
        cliente.telefono = nuevo_telefono

    save_data()
    print("\n✅ Cliente editado correctamente.\n")

def editar_reserva():
    print("\n--- Editar Reserva ---")
    id_reserva = input("ID de la reserva a editar: ").strip()

    # Buscar la reserva
    reserva = None
    for r in reservas:
        if r.id == id_reserva:
            reserva = r
            break

    if reserva is None:
        print("\n❌ No existe una reserva con ese ID.\n")
        return

    print("\nReserva actual:")
    print(reserva)

    print("\nDeja vacío lo que NO quieras modificar.\n")

    nueva_fecha = input(f"Fecha ({reserva.fecha}): ").strip()
    nueva_hora = input(f"Hora ({reserva.hora}): ").strip()
    nuevo_servicio = input(f"Servicio ({reserva.servicio}): ").strip()

    # Validaciones
    if nueva_fecha:
        if validar_fecha(nueva_fecha):
            reserva.fecha = nueva_fecha
        else:
            print("❌ Fecha inválida. No se modificó.")
    if nueva_hora:
        if validar_hora(nueva_hora):
            reserva.hora = nueva_hora
        else:
            print("❌ Hora inválida. No se modificó.")
    if nuevo_servicio:
        reserva.servicio = nuevo_servicio

    save_data()

    print("\n✅ Reserva editada correctamente.\n")



def registrar_reserva():
    print("\n--- Registrar Reserva ---")
    id_reserva = input("ID de la reserva: ").strip()

    if any(r.id == id_reserva for r in reservas):
        print("❌ Ese ID de reserva ya existe.")
        return

    id_cliente = input("ID del cliente: ").strip()

    if id_cliente not in clientes:
        print("\n❌ Ese cliente no existe.\n")
        return

    fecha = input("Fecha (AAAA-MM-DD): ").strip()
    if not validar_fecha(fecha):
        print("❌ Formato de fecha incorrecto.")
        return

    hora = input("Hora (HH:MM): ").strip()
    if not validar_hora(hora):
        print("❌ Formato de hora incorrecto.")
        return

    servicio = input("Servicio: ").strip()

    reserva = Reserva(id_reserva, id_cliente, fecha, hora, servicio)
    reservas.append(reserva)
    save_data()

    print("\n✅ Reserva registrada correctamente.\n")


def listar_clientes():
    print("\n--- Lista de Clientes ---")
    if not clientes:
        print("No hay clientes.\n")
        return

    for c in clientes.values():
        print(c)
    print()


def listar_reservas():
    print("\n--- Lista de Reservas ---")
    if not reservas:
        print("No hay reservas.\n")
        return

    ordenadas = sorted(reservas, key=lambda r: (r.fecha, r.hora))

    for r in ordenadas:
        print(r)
    print()


def buscar_cliente_por_id():
    print("\n--- Buscar Cliente por ID ---")
    id_buscar = input("ID: ").strip()

    if id_buscar in clientes:
        print("\n✅ Encontrado:")
        print(clientes[id_buscar])
    else:
        print("\n❌ No encontrado.")
    print()


def buscar_reserva_por_id():
    print("\n--- Buscar Reserva por ID ---")
    id_buscar = input("ID: ").strip()

    res = [r for r in reservas if r.id == id_buscar]

    if res:
        for r in res:
            print(r)
    else:
        print("\n❌ No se encontró esa reserva.")
    print()


def eliminar_reserva():
    print("\n--- Eliminar Reserva ---")
    id_reserva = input("ID: ").strip()

    for i, r in enumerate(reservas):
        if r.id == id_reserva:
            del reservas[i]
            save_data()
            print("\n✅ Reserva eliminada.\n")
            return

    print("\n❌ No existe esa reserva.\n")


# =============================
#            MENÚ
# =============================
def menu():
    load_data()

    while True:
        print("\n==============================")
        print("     SISTEMA DE RESERVAS     ")
        print("==============================")
        print("1. Registrar cliente")
        print("2. Registrar reserva")
        print("3. Listar clientes")
        print("4. Listar reservas")
        print("5. Buscar cliente")
        print("6. Buscar reserva")
        print("7. Editar cliente")
        print("8. Editar reserva")
        print("9. Eliminar reserva")
        print("10. Salir")


        opcion = input("Elige una opción: ").strip()

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
            editar_cliente()
        elif opcion == "8":
            editar_reserva()
        elif opcion == "9":
            eliminar_reserva()
        elif opcion == "10":
             print("\n¡Gracias por usar el sistema!\n")
             break

        else:
            print(" Opción no válida.\n")


if __name__ == "__main__":
    menu()
