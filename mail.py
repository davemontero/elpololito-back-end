from operator import truediv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def recovery_mail(usermail, new_password):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "elpololitocl@gmail.com"
        password = "7*&$*9n37M3&%^863^4"
        receiver_email = usermail
        message = MIMEMultipart("alternative")
        message["Subject"] = "[El Pololito CL] - Recuperación de contraseña"
        message["From"] = sender_email
        message["To"] = receiver_email
        html = f"""\
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta http-equiv="x-ua-compatible" content="ie=edge">
                <title>Password Reset</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style type="text/css">
                    @media screen """"""{
                        @font-face {
                            font-family: 'Source Sans Pro';
                            font-style: normal;
                            font-weight: 400;
                            src: local('Source Sans Pro Regular'), local('SourceSansPro-Regular'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format('woff');
                        }

                        @font-face {
                            font-family: 'Source Sans Pro';
                            font-style: normal;
                            font-weight: 700;
                            src: local('Source Sans Pro Bold'), local('SourceSansPro-Bold'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format('woff');
                        }
                    }
                    body,
                    table,
                    td,
                    a {
                        -ms-text-size-adjust: 100%;
                        /* 1 */
                        -webkit-text-size-adjust: 100%;
                        /* 2 */
                    }
                    table,
                    td {
                        mso-table-rspace: 0pt;
                        mso-table-lspace: 0pt;
                    }
                    img {
                        -ms-interpolation-mode: bicubic;
                    }
                    a[x-apple-data-detectors] {
                        font-family: inherit !important;
                        font-size: inherit !important;
                        font-weight: inherit !important;
                        line-height: inherit !important;
                        color: inherit !important;
                        text-decoration: none !important;
                    }
                    div[style*="margin: 16px 0;"] {
                        margin: 0 !important;
                    }

                    body {
                        width: 100% !important;
                        height: 100% !important;
                        padding: 0 !important;
                        margin: 0 !important;
                    }
                    table {
                        border-collapse: collapse !important;
                    }

                    a {
                        color: #1a82e2;
                    }

                    img {
                        height: auto;
                        line-height: 100%;
                        text-decoration: none;
                        border: 0;
                        outline: none;
                    }
                </style>
            </head>
            <body style="background-color: #e9ecef;">
                <div class="preheader"
                    style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0;">
                    Sigue los siguientes pasos para reestablecer tu contraseña.
                </div>
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td align="center" bgcolor="#e9ecef">
                            <!--[if (gte mso 9)|(IE)]>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                    <tr>
                    <td align="center" valign="top" width="600">
                    <![endif]-->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                                <tr>
                                    <td align="center" valign="top" style="padding: 36px 24px;">
                                        <a href="https://localhost:3000/" target="_blank" style="display: inline-block;">
                                            <img src="./img/paste-logo-light@2x.png" alt="Logo" border="0" width="48"
                                                style="display: block; width: 48px; max-width: 48px; min-width: 48px;">
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <!--[if (gte mso 9)|(IE)]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                        </td>
                    </tr>
                    <tr>
                        <td align="center" bgcolor="#e9ecef">
                            <!--[if (gte mso 9)|(IE)]>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                    <tr>
                    <td align="center" valign="top" width="600">
                    <![endif]-->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                                <tr>
                                    <td align="left" bgcolor="#ffffff"
                                        style="padding: 36px 24px 0; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf;">
                                        <h1
                                            style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">
                                            Reestablece tu contraseña</h1>
                                    </td>
                                </tr>
                            </table>
                            <!--[if (gte mso 9)|(IE)]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                        </td>
                    </tr>
                    <tr>
                        <td align="center" bgcolor="#e9ecef">
                            <!--[if (gte mso 9)|(IE)]>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                    <tr>
                    <td align="center" valign="top" width="600">
                    <![endif]-->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                                <tr>
                                    <td align="left" bgcolor="#ffffff"
                                        style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
                                        <p style="margin: 0;">Haz clic en el boton de abajo para reestablecer tu contraseña. Si no fuiste tu quien solicito el cambio de la contraseña, puedes borrar este mensaje</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="left" bgcolor="#ffffff">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td align="center" bgcolor="#ffffff" style="padding: 12px;">
                                                    <table border="0" cellpadding="0" cellspacing="0">
                                                        <tr>
                                                            <td align="center" bgcolor="#1a82e2" style="border-radius: 6px;">
                                                                <p style="display: inline-block;padding: 26px 50px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 24px; color: #ffffff; border-radius: 6px; letter-spacing: 12px">
                                                                    """+ new_password +"""</p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="left" bgcolor="#ffffff"
                                        style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
                                        <p style="margin: 0;">Ingresa al siguiente enlace en tu navegador:</p>
                                        <p style="margin: 0;"><a href="http://localhost:5000/reset-password/"
                                                target="_blank">http://localhost:5000/reset-password/</a></p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="left" bgcolor="#ffffff"
                                        style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
                                        <p style="margin: 0;">¡Saludos!,<br> El equipo Pololito</p>
                                    </td>
                                </tr>

                            </table>
                            <!--[if (gte mso 9)|(IE)]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                        </td>
                    </tr>
                    <tr>
                        <td align="center" bgcolor="#e9ecef" style="padding: 24px;">
                            <!--[if (gte mso 9)|(IE)]>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                    <tr>
                    <td align="center" valign="top" width="600">
                    <![endif]-->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                                <tr>
                                    <td align="center" bgcolor="#e9ecef"
                                        style="padding: 12px 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666;">
                                        <p style="margin: 0;">Recibiste este correo porque recibimos una solicitud de reestablecer la contraseña de tu cuenta.
                                            Si no fuiste tu quien hizo esta solicitud, puedes eliminar este correo.</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" bgcolor="#e9ecef"
                                        style="padding: 12px 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666;">
                                        <p style="margin: 0;">Santiago, Chile</p>
                                    </td>
                                </tr>
                            </table>
                            <!--[if (gte mso 9)|(IE)]>
                    </td>
                    </tr>
                    </table>
                    <![endif]-->
                        </td>
                    </tr>
                </table>
            </body>
            </html>"""

        message.attach(MIMEText(html, 'html'))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
        return True
    except:
        return False
