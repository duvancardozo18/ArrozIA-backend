# ArrozIA-backend
La trazabilidad en el cultivo de arroz es un factor clave para garantizar la calidad, seguridad y eficiencia en la producción agrícola. Sin embargo, el monitoreo manual de enfermedades, plagas, malezas y deficiencias nutricionales presenta limitaciones en precisión y tiempo de respuesta.

Este proyecto propone el desarrollo de una plataforma de trazabilidad basada en inteligencia artificial, que permita a los agricultores monitorear y gestionar en tiempo real la evolución de sus cultivos, optimizando la toma de decisiones y reduciendo pérdidas.

**Metodología**
El desarrollo del sistema sigue la metodología ágil Scrum y los estándares de requerimientos ISO/IEC/IEEE 29148:2018. Se diseña una arquitectura basada en FastAPI y React, con pruebas bajo la normativa ISO 25010. 

**Tecnologías Utilizadas**
El sistema está compuesto por un backend y un frontend independientes, lo que permite una arquitectura escalable y eficiente.

🖥️ Backend – ArrozIA-backend
- Desarrollado con FastAPI, garantizando un rendimiento rápido y eficiente.
- Implementación de modelos de inteligencia artificial para la detección de enfermedades y plagas en los cultivos.
- Base de datos en PostgreSQL, optimizada para el almacenamiento de registros agrícolas.

📌 Frontend – ArrozIA-frontend
- Desarrollado con React, proporcionando una interfaz intuitiva y dinámica.
- Uso de Redux para la gestión del estado y optimización del rendimiento.
- Integración con el backend a través de APIs REST para una experiencia fluida.
- Diseño responsive para acceso desde dispositivos móviles y computadoras.
> Enlace del Repositorio: [Click aqui](https://github.com/duvancardozo18/ArrozIA-frontend-web)

## 🛠️   Instalación  

### Requisitos 
Tener instalado las siguientes herramientas: 
- **Python 3.11**
- **PostgreSQL 16.6**
- **Rustup.rs**  (Después de instalar el software, se procede a instalar las librerías de Cargo y Rustc utilizando la Opción 1)
---

### Instrucciones  
1. **Clonar o descargar** el repositorio del proyecto.  
2. **Establecer variables de entorno.**  
   - Copiar `.env.example` y renombrar como `.env`
   - Crear una base de datos en pgadmin4 (PostgreSQL) e importar la base de datos ArrozIADBPostgreSQL.sql
   - Escribir las credenciales de la base de datos en el archivo `.env` en la seccion **DATABASE_URL** - estructura de ejemplo: 
   DATABASE_URL="postgresql+psycopg2://nombre_usuario_postgresql:contraseña_postgres@localhost:5432/nombre_base_de_datos" #remplazar de acuerdo a sus credenciales.
3. **Permitir la ejecucion de Scripts de Python**  
    Abrir una nueva terminal en PowerShell como administrador y ejecute:  
   ```bash
   Set-ExecutionPolicy Unrestricted -Scope LocalMachine
4. **Crear un entorno virtual de Python**  
   Abrir una nueva terminal en el directorio raíz del proyecto y ejecute:  
   ```bash
   python -m venv venv
5. **Ejecutar entorno virtual de Python**   
   ```bash
   venv\Scripts\activate
3. **Instalar Dependencias**   
   ```bash
   pip install -r requirements.txt
4. **Levantar servidor**  
   ```bash
   uvicorn main:app --reload
---

### Documentación - Postman
![Documentación - Postman](<#>)
> Docuementación completa: [Click aqui](https://www.postman.com/mission-explorer-5726823/arrozia-backend/collection/u3c2byc/arrozia-backend)

## 🚀 Credenciales
 
- **Correo:** `juan.perez@example.com`  
- **Contraseña:** `Usco2024.` 


