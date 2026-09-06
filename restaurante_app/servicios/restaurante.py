from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    """
    Servicio que administra las colecciones y las reglas de negocio del sistema.
    Semana 12 (MEJORA): conserva las listas para listar y persistir, pero agrega
    índices en memoria (dict y set) para acelerar búsquedas y consultas frecuentes.
    """

    def __init__(self) -> None:
        # Las listas se mantienen para listar, recorrer y guardar en JSON.
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []

        # MEJORA SEMANA 12: índices internos para optimizar búsquedas.
        # Los diccionarios permiten localizar productos y usuarios por clave
        # sin recorrer toda la colección. El set mantiene códigos y categorías únicas.
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._codigos_existentes: set[str] = set()
        self._categorias: set[str] = set()

        self.cargar_datos()

    def _reconstruir_indices(self) -> None:
        # MEJORA SEMANA 12: al cargar datos desde JSON llegan como listas.
        # Aquí se crean las estructuras auxiliares en memoria para acelerar consultas.
        self._productos_por_codigo = {}
        self._usuarios_por_identificacion = {}
        self._ventas_por_usuario = {}
        self._codigos_existentes = set()
        self._categorias = set()

        for producto in self.productos:
            self._productos_por_codigo[producto.codigo] = producto
            self._codigos_existentes.add(producto.codigo)
            self._categorias.add(producto.categoria)

        for usuario in self.usuarios:
            self._usuarios_por_identificacion[usuario.identificacion] = usuario

        for venta in self.ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    def _reconstruir_indice_categorias(self) -> None:
        # MEJORA SEMANA 12: reconstruye las categorías únicas cuando cambia la colección.
        self._categorias = {producto.categoria for producto in self.productos}

    def cargar_datos(self) -> None:
        self.productos = ArchivoServicio.cargar_productos()
        self.usuarios = ArchivoServicio.cargar_usuarios()
        self.ventas = ArchivoServicio.cargar_ventas()
        self._reconstruir_indices()

    def guardar_datos(self) -> None:
        ArchivoServicio.guardar_productos(self.productos)
        ArchivoServicio.guardar_usuarios(self.usuarios)
        ArchivoServicio.guardar_ventas(self.ventas)

    # ---------- Productos ----------

    def agregar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._codigos_existentes:
            return False
        self.productos.append(producto)
        # MEJORA SEMANA 12: lista e índice se sincronizan en la MISMA operación.
        self._productos_por_codigo[producto.codigo] = producto
        self._codigos_existentes.add(producto.codigo)
        self._categorias.add(producto.categoria)
        self.guardar_datos()
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        # MEJORA SEMANA 12: búsqueda directa por clave.
        # Antes se recorría toda la lista de productos. Con dict el acceso es O(1).
        return self._productos_por_codigo.get(codigo)

    def modificar_producto(
        self,
        codigo: str,
        nuevo_nombre: str = None,
        nuevo_precio: float = None,
        nuevo_stock: int = None,
        nueva_categoria: str = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if not producto:
            return False
        if nuevo_nombre:
            producto.nombre = nuevo_nombre
        if nuevo_precio is not None:
            producto.precio = float(nuevo_precio)
        if nuevo_stock is not None:
            producto.stock = int(nuevo_stock)
        if nueva_categoria:
            producto.categoria = nueva_categoria
            # Al cambiar la categoría, se reconstruye el conjunto de categorías únicas.
            self._reconstruir_indice_categorias()
        self.guardar_datos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if not producto:
            return False
        self.productos.remove(producto)
        self._productos_por_codigo.pop(producto.codigo, None)
        self._codigos_existentes.discard(producto.codigo)
        self._reconstruir_indice_categorias()
        self.guardar_datos()
        return True

    def listar_productos(self) -> list[Producto]:
        return list(self.productos)

    def contar_productos(self) -> int:
        return len(self.productos)

    # ---------- Usuarios ----------

    def agregar_usuario(self, usuario: Usuario) -> bool:
        if usuario.identificacion in self._usuarios_por_identificacion:
            return False
        self.usuarios.append(usuario)
        # MEJORA SEMANA 12: el índice se actualiza junto con la lista.
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        self.guardar_datos()
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        # MEJORA SEMANA 12: acceso directo por identificación.
        identificacion = identificacion.strip()
        return self._usuarios_por_identificacion.get(identificacion)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.usuarios)

    def contar_usuarios(self) -> int:
        return len(self.usuarios)

    # ---------- Ventas (Semana 11/12) ----------

    def registrar_venta(self, usuario_id: str, producto_id: str, cantidad: int) -> bool:
        # Se validan las reglas de negocio ANTES de modificar colecciones o stock.
        usuario = self.buscar_usuario(usuario_id)
        producto = self.buscar_producto(producto_id)

        if usuario is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario_id, producto_id, cantidad)
        self.ventas.append(venta)
        # MEJORA SEMANA 12: la venta también se agrupa por usuario en el índice.
        self._ventas_por_usuario.setdefault(usuario_id, []).append(venta)
        producto.stock -= cantidad
        self.guardar_datos()
        return True

    def vender_producto(self, producto_id: str, usuario_id: str, cantidad: int) -> bool:
        """Método helper compatible con el orden de parámetros de main.py."""
        return self.registrar_venta(usuario_id, producto_id, cantidad)

    def consultar_ventas_usuario(self, usuario_id: str) -> list[Venta]:
        # MEJORA SEMANA 12: consulta optimizada mediante el índice por usuario.
        usuario_id = usuario_id.strip()
        return list(self._ventas_por_usuario.get(usuario_id, []))

    def listar_ventas(self) -> list[Venta]:
        return list(self.ventas)

    # ---------- Categorías únicas (MEJORA SEMANA 12) ----------

    def obtener_categorias_unicas(self) -> set[str]:
        # MEJORA SEMANA 12: las categorías se mantienen en un set actualizado.
        return set(self._categorias)

    def existe_categoria(self, categoria: str) -> bool:
        # MEJORA SEMANA 12: pertenencia en set, ideal para validaciones rápidas.
        return categoria.strip() in self._categorias