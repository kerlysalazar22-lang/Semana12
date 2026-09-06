# Restaurante App — Semana 12 (Optimización con Colecciones)

**Estudiante:** Kerly Salazar
**Asignatura:** Programación Orientada a Objetos
**Universidad:** Universidad Estatal Amazónica
**Semana:** 12 — Utilización de colecciones para la mejora de rendimiento

---

## 📌 Descripción

Aplicación de consola tipo restaurante que administra productos, usuarios y ventas,
manteniendo la persistencia en archivos JSON. En la **Semana 12** se incorporaron
**estructuras auxiliares en memoria** (`dict` y `set`) dentro de
`servicios/restaurante.py` para optimizar las búsquedas y consultas frecuentes,
reduciendo los recorridos innecesarios en las colecciones.

## 🚀 Mejoras de rendimiento aplicadas (Semana 12)

### 1. Índices de búsqueda rápida (`dict`)
| Índice | Clave | Uso |
|---|---|---|
| `_productos_por_codigo` | código del producto | `buscar_producto()` en O(1) con `.get()` |
| `_usuarios_por_identificacion` | identificación del usuario | `buscar_usuario()` en O(1) con `.get()` |

### 2. Agrupación de ventas por usuario (`dict`)
- `_ventas_por_usuario`: asocia la identificación del usuario con su historial
  de ventas (`list[Venta]`), evitando recorrer toda la lista de ventas.

### 3. Validación de unicidad y categorías (`set`)
- `_codigos_existentes`: verifica al instante si un código de producto ya existe.
- `_categorias`: mantiene las categorías únicas de los productos.

### 4. Sincronización y reconstrucción automática
- `_reconstruir_indices()` reconstruye los índices al iniciar la aplicación a
  partir de las listas cargadas desde los archivos JSON.
- La lista principal y los índices se sincronizan en la **misma operación**
  (registrar, modificar, eliminar y vender).

## 🖥️ Ejecución del proyecto

```bash
python main.py
```

Menú de opciones:

- **GESTIÓN DE PRODUCTOS:** 1. Agregar · 2. Consultar · 3. Modificar · 4. Eliminar · 5. Ver todos
- **GESTIÓN DE USUARIOS:** 6. Agregar · 7. Ver
- **OPERACIONES (Semana 11):** 8. Realizar venta · 9. Consultar ventas por usuario
- **CONSULTAS (MEJORA Semana 12):** 10. Listar categorías únicas
- **0.** Salir

## 🧪 Pruebas principales

Smoke test de 12 pasos ejecutado y aprobado:

1. Registrar 3 productos (índice + lista sincronizados).
2. Duplicado de código rechazado por el `set _codigos_existentes`.
3. Búsquedas `buscar_producto()` / `buscar_usuario()` en O(1).
4. Categorías únicas (`_categorias`) y `existe_categoria()`.
5. Venta exitosa: stock disminuye y la venta se agrupa por usuario.
6. Venta con stock insuficiente rechazada sin alterar datos.
7. Modificación del producto reconstruye categorías.
8. Eliminación sincroniza lista, dict, set y categorías.
9. Persistencia JSON: al reabrir la app se recuperan productos, usuarios y ventas.

## 📂 Estructura

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```