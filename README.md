# 📚 Sistema de Gestión Escolar + Herramientas de Investigación

Proyecto web completo desarrollado con **Django**, pensado para la **gestión de alumnos**, generación de **reportes automatizados** y un módulo de **investigación con web scraping**.

🔗 **Deploy en Vivo:** [https://examen-prog.onrender.com](https://examen-prog.onrender.com)

---

## 🚀 Funcionalidades Principales

### 1. 🔐 Autenticación y Seguridad

* Sistema completo de **Login**, **Registro** y **Logout**.
* **Emails transaccionales** automáticos al registrarse (SendGrid API).
* **Protección de rutas:** el Dashboard solo es accesible estando logueado.

---

### 2. 🧑‍🎓 Gestión de Alumnos (CRUD)

* Panel con listado dinámico de alumnos.
* Formularios personalizados con validaciones.
* Base de datos optimizada para lectura y escritura.

---

### 3. 📄 Reportes PDF Automatizados

* Generación de **fichas técnicas en PDF** usando *ReportLab*.
* **Envío automático por correo** del PDF al docente/usuario logueado.
* Proceso 100% automatizado: un solo clic.

---

### 4. 🔎 Módulo de Investigación (Web Scraping)

* Buscador integrado conectado a **Wikipedia**.
* Extracción automática de: título, resumen e imagen del artículo.
* Implementado con **BeautifulSoup** + **Requests**.
* Opción para guardar y enviar el informe por correo.

---

## 🛠️ Tecnologías Utilizadas

### **Backend:**

* Python
* Django 5

### **Frontend:**

* HTML5, CSS3
* Bootstrap 5 (Dark Mode)

### **Base de Datos:**

* SQLite (desarrollo)
* PostgreSQL (producción)

### **Servicios Cloud:**

* Render → Deploy
* SendGrid → Emails

### **Librerías Clave:**

* `reportlab` → Generación de PDFs
* `beautifulsoup4` → Web Scraping
* `django-sendgrid-v5` → Integración SendGrid
* `gunicorn` & `whitenoise` → Servidor en producción

---

## 💻 Instalación Local

Sigue estos pasos para ejecutar el proyecto en tu máquina:

### 1. Clonar el repositorio

```bash
git clone https://github.com/LuisJimenez99/examen-prog.git
cd examen-prog
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Migrar base de datos

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

---

## 👨‍💻 Autor

Proyecto desarrollado por **Luis Jimenez** para el **Examen Final de Programación**.

---
