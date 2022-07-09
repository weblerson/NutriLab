from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpRequest
import re

class Verify:
    @staticmethod
    def blank_inputs(request: HttpRequest, *args):
        for arg in args:
            if len(arg.strip()) == 0:
                messages.add_message(request, constants.WARNING, "Preencha todos os campos!")

                return True

        return False

    @staticmethod
    def is_numeric(request: HttpRequest, *args):
        for arg in args:
            if not arg.isnumeric():
                messages.add_message(request, constants.WARNING, "Digite valores numéricos")

                return False

        return True

    @staticmethod
    def phone_number(request: HttpRequest, phone: str):
        if not re.search('[0-9]', phone):
            messages.add_message(request, constants.WARNING, "Digite um número de telefone válido!")

            return False

        return True