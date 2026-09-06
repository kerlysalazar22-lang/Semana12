import json
import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    RUTA_DATOS = "datos"

    @classmethod
    def _obtener_ruta(cls, nombre_archivo: str) -> str:
        if not os.path.exists(cls.RUTA_DATOS):
            os.makedirs(cls.RUTA_DATOS)
        return os.path.join(cls.RUTA_DATOS, nombre_archivo)

    @classmethod
    def guardar_productos(cls, productos: list[Producto]) -> None:
        ruta = cls._obtener_ruta("productos.json")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([p.a_diccionario() for p in productos], f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("Error: No se tienen permisos para escribir en productos.json.")

    @classmethod
    def cargar_productos(cls) -> list[Producto]:
        ruta = cls._obtener_ruta("productos.json")
        productos = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    productos.append(Producto.desde_diccionario(item))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: Formato JSON inválido en productos.json.")
        except KeyError as e:
            print(f"Error: Clave faltante {e} al cargar productos.")
        except PermissionError:
            print("Error: Sin permisos para leer productos.json.")
        return productos

    @classmethod
    def guardar_usuarios(cls, usuarios: list[Usuario]) -> None:
        ruta = cls._obtener_ruta("usuarios.json")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([u.a_diccionario() for u in usuarios], f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("Error: No se tienen permisos para escribir en usuarios.json.")

    @classmethod
    def cargar_usuarios(cls) -> list[Usuario]:
        ruta = cls._obtener_ruta("usuarios.json")
        usuarios = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    usuarios.append(Usuario.desde_diccionario(item))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: Formato JSON inválido en usuarios.json.")
        except KeyError as e:
            print(f"Error: Clave faltante {e} al cargar usuarios.")
        except PermissionError:
            print("Error: Sin permisos para leer usuarios.json.")
        return usuarios

    @classmethod
    def guardar_ventas(cls, ventas: list[Venta]) -> None:
        ruta = cls._obtener_ruta("ventas.json")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump([v.a_diccionario() for v in ventas], f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("Error: No se tienen permisos para escribir en ventas.json.")

    @classmethod
    def cargar_ventas(cls) -> list[Venta]:
        ruta = cls._obtener_ruta("ventas.json")
        ventas = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for item in datos:
                    ventas.append(Venta.desde_diccionario(item))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: Formato JSON inválido en ventas.json.")
        except KeyError as e:
            print(f"Error: Clave faltante {e} al cargar ventas.")
        except PermissionError:
            print("Error: Sin permisos para leer ventas.json.")
        return ventas