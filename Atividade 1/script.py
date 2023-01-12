import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TO = os.environ.get("TO")
FROM = os.environ.get("FROM", "")
FROM_PASS = os.environ.get("FROM_PASS")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
BACKUP_FILE = os.environ.get("BACKUP_FILE")

subprocess.call(
    f"pg_dump -h {DB_HOST} -U {DB_USER} -F t {DB_NAME} -f {BACKUP_FILE}", shell=True
)

msg = MIMEMultipart()
msg["From"] = FROM
msg["To"] = TO
msg["Subject"] = "Backup do banco de dados"

part = MIMEBase("application", "octet-stream")
part.set_payload(open(BACKUP_FILE, "rb").read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={BACKUP_FILE}")
msg.attach(part)

smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp_obj.starttls()
smtp_obj.login(FROM, FROM_PASS)
smtp_obj.sendmail(FROM, TO, msg.as_string())
smtp_obj.quit()

os.remove(BACKUP_FILE)

print("Backup realizado com sucesso e enviado por e-mail.")
