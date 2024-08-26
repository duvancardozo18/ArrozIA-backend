import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient: str, token: str, user_name: str):
    sender_email = "arrozia@outlook.com"  # Reemplaza con tu correo de Outlook
    sender_password = "pachito15"  # Reemplaza con tu contraseña de Outlook

    # URL de restablecimiento de contraseña
    reset_password_url = f"http://127.0.0.1:8000/Reset_Password/{token}"

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
    message.attach(MIMEText(body, "html", "utf-8"))  # Cambia el tipo a 'html'

    try:
        # Conectar al servidor SMTP de Outlook
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()  # Asegurar la conexión
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())  # No se necesita .encode('utf-8') aquí
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
