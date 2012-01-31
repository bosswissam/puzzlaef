from puzzlaef.registration.backends.default import DefaultBackend
from puzzlaef.registration.forms import ReCaptchaRegistrationForm

class RecaptchaRegistrationBackend(DefaultBackend):
    def get_form_class(self, request):
        return ReCaptchaRegistrationForm
