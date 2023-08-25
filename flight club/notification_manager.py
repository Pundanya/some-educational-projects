import smtplib

my_email = "yourmail@mail.ru"
my_pass = "yourtoken"
message = ""

class NotificationManager:

    def send_mail(self, to_adress, msg: bytes):
        with smtplib.SMTP("smtp.mail.ru") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_pass)
            connection.sendmail(
                    from_addr=my_email,
                    to_addrs=to_adress,
                    msg=msg
            )

