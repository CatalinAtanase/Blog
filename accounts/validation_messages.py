from django.utils.translation import gettext, gettext_lazy as _


class ValidationMessages:
    invalid_login = _('Numele de utilizator si parola nu se potrivesc.')
    inactive = _('Acest cont este inactiv') # Unused atm
    password_mismatch = _('Cele doua parole nu sunt identice.')
    password_incorrect = _("Parola veche a fost introdusa incorect.")
    unique_user = _('Exista deja un utilizator cu acest nume.')
    unique_email = _('Exista deja un utilizator cu acest email.')

    def get_password_min_length(self, min_length=8):
        return  _(f'Parola trebuie sa fie de cel putin {min_length} caractere.')
