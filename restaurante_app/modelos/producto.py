class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int, categoria: str = "General"):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = str(categoria) if categoria else "General"

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            codigo=datos.get("codigo", ""),
            nombre=datos.get("nombre", ""),
            precio=datos.get("precio", 0.0),
            stock=datos.get("stock", 0),
            categoria=datos.get("categoria", "General")
        )

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - ${self.precio:.2f} | Stock: {self.stock} | Cat: {self.categoria}"
