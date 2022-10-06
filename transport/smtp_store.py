import smtplib
import ssl
import collections

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from .truck import Cargo, Destination


class SmtpDestination(Destination):
    def __init__(self, address: str, server: str, port: int, user: str, password: str):
        Smtp = collections.namedtuple("Smtp", "server port user password")
        self._smtp = Smtp(
            server=server,
            port=port,
            user=user,
            password=password
        )
        self._address = address

    async def unload(self, cargo: Cargo):
        print(
            f"Sending email to {self._address} via {self._smtp.server}:{self._smtp.port} using user {self._smtp.user}")
        message = MIMEMultipart()
        message["From"] = self._smtp.user
        message["To"] = self._address
        message["Subject"] = "Kindle Book"

        with cargo.empty() as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename=book.epub")
            message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp.server, port=self._smtp.port, context=context) as server:
            server.login(self._smtp.user, self._smtp.password)
            server.sendmail(self._smtp.user, self._address, message.as_string())
            server.quit()
