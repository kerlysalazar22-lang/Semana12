from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante


OPCIONES_MENU = (
    ("1", "Agregar producto"),
    ("2", "Consultar producto"),
    ("3", "Modificar producto"),
    ("4", "Eliminar producto"),
    ("5", "Ver todos los productos"),
    # Gestión de usuarios (entidad que participa en la venta).
    ("6", "Agregar usuario"),
    ("7", "Ver usuarios"),
    # Semana 11: operaciones que relacionan objetos.
    ("8", "Realizar venta"),
    ("9", "Consultar ventas por usuario"),
    # MEJORA SEMANA 12: consultas sobre categorías únicas mediante set.
    ("10", "Listar categorías únicas"),
    ("0", "Salir"),
)


def mostrar_menu() -> None:
    print("\n===== RESTAURANTE APP — Semana 12 =====")
    print("\nGESTIÓN DE PRODUCTOS")
    for numero, descripcion in OPCIONES_MENU[:5]:
        print(f"{numero}. {descripcion}")
    print("\nGESTIÓN DE USUARIOS")
    for numero, descripcion in OPCIONES_MENU[5:7]:
        print(f"{numero}. {descripcion}")
    print("\nOPERACIONES (Semana 11)")
    for numero, descripcion in OPCIONES_MENU[7:9]:
        print(f"{numero}. {descripcion}")
    print("\nCONSULTAS (MEJORA Semana 12)")
    print(f"{OPCIONES_MENU[9][0]}. {OPCIONES_MENU[9][1]}")
    print("0. Salir")


def pedir(mensaje: str) -> str:
    return input(mensaje).strip()


def main() -> None:
    restaurante = Restaurante()

    while True:
        mostrar_menu()
        opcion = pedir("Elige opción: ")

        if opcion == "1":
            codigo = pedir("Código del producto: ")
            nombre = pedir("Nombre del producto: ")
            categoria = pedir("Categoría: ")
            try:
                precio = float(pedir("Precio: "))
                stock = int(pedir("Stock inicial: "))
                producto = Producto(codigo, nombre, precio, stock, categoria)
                if restaurante.agregar_producto(producto):
                    print("¡Producto registrado exitosamente!")
                else:
                    print("Error: Ya existe un producto con ese código.")
            except ValueError as e:
                print(f"Error de validación: {e}")

        elif opcion == "2":
            codigo = pedir("Código a buscar: ")
            p = restaurante.buscar_producto(codigo)
            if p:
                print(f"Encontrado: [{p.codigo}] {p.nombre} - ${p.precio:.2f} | Stock: {p.stock} | Cat: {p.categoria}")
            else:
                print("Producto no encontrado.")

        elif opcion == "3":
            codigo = pedir("Código del producto a modificar: ")
            if restaurante.buscar_producto(codigo):
                try:
                    nombre = pedir("Nuevo nombre: ")
                    precio = float(pedir("Nuevo precio: "))
                    stock = int(pedir("Nuevo stock: "))
                    categoria = pedir("Nueva categoría (Enter para mantener): ")
                    if restaurante.modificar_producto(codigo, nombre, precio, stock, categoria or None):
                        print("Producto modificado correctamente.")
                except ValueError as e:
                    print(f"Error en los datos: {e}")
            else:
                print("El producto no existe.")

        elif opcion == "4":
            codigo = pedir("Código del producto a eliminar: ")
            if restaurante.eliminar_producto(codigo):
                print("Producto eliminado con éxito.")
            else:
                print("Producto no encontrado.")

        elif opcion == "5":
            productos = restaurante.listar_productos()
            if productos:
                print("\nLISTA DE PRODUCTOS:")
                for p in productos:
                    print(f"- [{p.codigo}] {p.nombre} - ${p.precio:.2f} | Stock: {p.stock} | Cat: {p.categoria}")
                print(f"Total de productos: {restaurante.contar_productos()}")
            else:
                print("No hay productos registrados.")

        elif opcion == "6":
            identificacion = pedir("Identificación del usuario: ")
            nombre = pedir("Nombre completo: ")
            email = pedir("Email: ")
            usuario = Usuario(identificacion, nombre, email)
            if restaurante.agregar_usuario(usuario):
                print("Usuario registrado exitosamente.")
            else:
                print("Error: El usuario ya está registrado.")

        elif opcion == "7":
            usuarios = restaurante.listar_usuarios()
            if usuarios:
                print("\nLISTA DE USUARIOS:")
                for u in usuarios:
                    print(f"- [{u.identificacion}] {u.nombre} ({u.email})")
                print(f"Total de usuarios: {restaurante.contar_usuarios()}")
            else:
                print("No hay usuarios registrados.")

        elif opcion == "8":
            id_usuario = pedir("ID del Usuario comprador: ")
            cod_producto = pedir("Código del Producto a comprar: ")
            try:
                cant = int(pedir("Cantidad: "))
                if restaurante.vender_producto(cod_producto, id_usuario, cant):
                    print("¡Venta realizada y registrada con éxito!")
                else:
                    print("Error: Usuario/Producto inexistente, cantidad inválida o stock insuficiente.")
            except ValueError:
                print("La cantidad debe ser un número entero válido.")

        elif opcion == "9":
            id_usuario = pedir("Identificación del usuario: ")
            ventas = restaurante.consultar_ventas_usuario(id_usuario)
            if ventas:
                print(f"\nVENTAS REGISTRADAS PARA EL USUARIO {id_usuario}:")
                for v in ventas:
                    prod = restaurante.buscar_producto(v.producto_codigo)
                    nombre_prod = prod.nombre if prod else v.producto_codigo
                    print(f"- Producto: {nombre_prod} (Cód: {v.producto_codigo}) | Cantidad: {v.cantidad}")
            else:
                print("No se encontraron ventas para este usuario.")

        elif opcion == "10":
            # MEJORA SEMANA 12: las categorías únicas viven en un set actualizado.
            print("\n--- Categorías únicas ---")
            categorias = restaurante.obtener_categorias_unicas()
            if len(categorias) == 0:
                print("No hay categorías registradas.")
            else:
                for categoria in sorted(categorias):
                    print(f"- {categoria}")
                categoria_consultada = pedir("\nConsultar si existe una categoría (Enter para omitir): ")
                if categoria_consultada:
                    if restaurante.existe_categoria(categoria_consultada):
                        print("La categoría existe en el restaurante.")
                    else:
                        print("La categoría no existe en el restaurante.")

        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
    main()