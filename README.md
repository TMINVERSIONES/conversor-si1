# Conversor Excel a .si1 (API + Web UI)

Este proyecto permite convertir archivos Excel (`.xlsx`) a archivos `.si1` válidos para carga masiva de transferencias internacionales, usando una API FastAPI y una interfaz web simple, desplegable en Vercel.

---

## 🚀 Despliegue rápido con Vercel

1. Subí este repositorio a GitHub.
2. Iniciá sesión en [vercel.com](https://vercel.com) y hacé clic en **"Import Project"**.
3. Seleccioná el repo, confirmá la configuración y hacé clic en **Deploy**.

---

## 📁 Estructura del proyecto

```
├── api/
│   └── convertir.py         # Lógica del conversor
├── public/
│   └── index.html           # Interfaz web
├── requirements.txt         # Dependencias de Python
├── vercel.json              # Configuración de despliegue en Vercel
```

---

## 💡 ¿Cómo funciona?

- `convertir.py` es una función serverless (FastAPI) que recibe un archivo `.xlsx`, lo procesa y devuelve un archivo `.si1`.
- `index.html` es una interfaz web básica donde se puede subir un archivo Excel y descargar el resultado.

### Ejemplo de Excel esperado:
| Comitente | Instrumento            | Disponible |
|-----------|-------------------------|------------|
| 999       | (8527) CEDEAR VISTA     | 6          |

---

## ⚙️ Requisitos locales (si querés correrlo en tu PC)

```bash
pip install fastapi uvicorn pandas openpyxl
uvicorn api.convertir:app --reload
```

Y accedé a la API en `http://localhost:8000/convertir`

---

## ✨ Créditos
Este proyecto fue creado con el objetivo de facilitar la generación de archivos `.si1` cumpliendo los requerimientos del sistema NSC.

---

📫 ¿Mejoras o ideas? ¡Abrí un issue o mandá un pull request!
