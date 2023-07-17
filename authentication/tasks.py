from django.core.mail import EmailMessage
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.core.mail import EmailMessage


@shared_task()
def send_email(data):
    email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
    email.send(fail_silently=False)

"""@shared_task()
def send_email(data):
    # Generate the plain text version of the email (optional)
    text_content = strip_tags(data['email_body'])

    # Create the EmailMultiAlternatives object
    email = EmailMultiAlternatives(
        subject=data['email_subject'],
        body=text_content,
        to=[data['to_email']]
    )

    # Attach the HTML content
    html_content = render_to_string('email_template.html', data['template_context'])
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send(fail_silently=False)"""