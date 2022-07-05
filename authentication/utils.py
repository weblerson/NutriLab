import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class Verify:
    @staticmethod
    def password_is_valid(request, password: str, confirm_password: str):
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, "Sua senha deve conter 6 ou mais caracteres.")
            return False

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, "As senhas passadas não coincidem!")
            return False

        if not re.search('[A-Z]', password):
            messages.add_message(request, constants.ERROR, "Sua senha deve conter caracteres maiúsculos!")
            return False

        if not re.search('[a-z]', password):
            messages.add_message(request, constants.ERROR, "Sua senha deve conter caracteres minúsculos!")
            return False

        if not re.search('[0-9]', password):
            messages.add_message(request, constants.ERROR, "Sua senha deve conter números!")
            return False

        return True

class Send:
    @staticmethod
    def email(template_path, subject, to, **kwargs):
        html_content = render_to_string(template_path, kwargs)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return {"status": 1}