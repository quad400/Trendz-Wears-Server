
from utils.email import BaseEmailMessage

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
