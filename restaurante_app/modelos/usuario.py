class Usuario:
    def __init__(self, identificacion: str, nombre: str, email: str = ""):
        self.identificacion = identificacion
        self.nombre = nombre
        self.email = email

    def a_diccionario(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "email": self.email
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            identificacion=datos.get("identificacion", ""),
            nombre=datos.get("nombre", ""),
            email=datos.get("email", "")
        )

    def __str__(self):
        return f"Usuario: {self.nombre} | ID: {self.identificacion} | Email: {self.email}"