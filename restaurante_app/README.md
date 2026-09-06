# Restaurante App — Semana 12 (Optimización con Colecciones)

**Estudiante:** Kerly Salazar  
**Asignatura:** Programación Orientada a Objetos  
**Universidad:** Universidad Estatal Amazónica  

---

## Mejoras de Rendimiento Aplicadas (Semana 12)

En esta versión se incorporaron **estructuras auxiliares en memoria** dentro de `servicios/restaurante.py` para optimizar las consultas del sistema:

1. **Índices de Búsqueda Rápida (`dict`):**
   - `_indice_productos`: Permite la búsqueda directa de productos por su código en tiempo $O(1)$.
   - `_indice_usuarios`: Permite la búsqueda de usuarios por su identificación en tiempo $O(1)$.

2. **Agrupación de Ventas por Usuario (`dict`):**
   - `_ventas_por_usuario`: Asocia directamente la identificación del usuario con su historial de compras, evitando iterar toda la lista de ventas.

3. **Validación de Unicidad (`set`):**
   - `_codigos_existentes`: Conjunto de códigos de productos para verificar duplicados al instante.

4. **Sincronización y Reconstrucción Automática:**
   - Los índices se reconstruyen automáticamente al iniciar la aplicación a partir de las listas cargadas desde los archivos JSON.

---

## Ejecución del Proyecto

Para ejecutar la aplicación:
```bash
python main.py