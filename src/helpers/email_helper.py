import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def send_email(recipient: str, token: str, user_name: str):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    # URL de restablecimiento de contraseña desde variable de entorno
    reset_password_url = f"{os.getenv('RESET_PASSWORD_URL')}/{token}"

    # Configuración del mensaje con un enlace HTML
    subject = "Solicitud de Restablecimiento de Contraseña"
    body = (
        f"Hola {user_name},<br><br>"
        "Has solicitado restablecer tu contraseña. Por favor, utiliza el siguiente enlace para restablecer tu contraseña:<br><br>"
        f"<a href='{reset_password_url}'>Restablecer contraseña</a><br><br>"
        "Si no solicitaste el restablecimiento de contraseña, por favor ignora este correo.<br><br>"
        "Gracias,<br>"
        "El equipo de Tu Empresa"
    )

    # Asegurarse de que el mensaje esté completamente codificado en UTF-8
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "html", "utf-8"))

    try:
        # Conectar al servidor SMTP de Outlook
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)
        server.starttls()  # Asegurar la conexión
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
