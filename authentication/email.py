from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser.conf import default_settings
from djoser.utils import encode_uid

class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["otp"] = user.otp
        return context

class ResendCodeEmail(BaseEmailMessage):
    template_name = "email/resend_activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["otp"] = user.otp
        return context
