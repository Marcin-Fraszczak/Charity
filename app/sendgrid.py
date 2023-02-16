# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import *
#
#
# def send_mail(to_email, subject, content):
#     sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("fraszczak.programming@gmail.com")
#     to_email = To(to_email)
#     content = Content("text/plain", content)
#     mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    # mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    # response = sg.client.mail.send.post(request_body=mail_json)
    # print(response.status_code)
    # print(response.headers)


"""

from app.sendgrid import send_mail

"""