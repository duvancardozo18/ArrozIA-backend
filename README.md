# ArrozIA-backend
Es una aplicación cliente-servidor que utiliza inteligencia artificial para ofrecer trazabilidad en la producción del cultivo de arroz, optimizando el seguimiento y la gestión del proceso agrícola.


## 🛠️   Instalación  

### Requisitos 
Tener instalado las siguientes herramientas: 
- **Python 3.11**
- **PostgreSQL 16.6**
- **Rustup.rs**  (Instalacion del software y luego instalar librerias "Opcion 1")
---

### Instrucciones  
1. **Clonar o descargar** el repositorio del proyecto.  
2. **Establecer variables de entorno.**  
   - Copiar `.env.example` y renombrar como `.env`
   - Crear una base de datos en pgadmin4 (PostgreSQL) e importar la base de datos ArrozIADBPostgreSQL.sql
   - Escribir las credenciales de la base de datos en el archivo `.env` en la seccion **DATABASE_URL** con la siguiente estructura: postgres://nombre_usuario_postgres:contraseña_postgres@localhost:5432/nombre_base_de_datos #remplazar de acuerdo a sus credenciales.
3. **Crear un entorno virtual de Python**  
   Abra una terminal en el directorio raíz del proyecto y ejecute:  
   ```bash
   python -m venv venv
4. **Permitir la ejecucion de Scripts de Python**  
    Abrir una nueva terminal en PowerShell como administrador y ejecute:  
   ```bash
   Set-ExecutionPolicy Unrestricted -Scope LocalMachine
5. **Ejecutar entorno virtual de Python**  
   En la misma terminal ejecute:  
   ```bash
   venv\Scripts\activate
3. **Instalar Dependencias**  
   En la misma terminal ejecute:  
   ```bash
   pip install -r requirements.txt
4. **Levantar servidor**  
   ```bash
   uvicorn main:app --reload

> Repositorio del Frontend ArrozIA: [Enlace](https://github.com/duvancardozo18/ArrozIA-frontend-web)
