from dal import autocomplete
from .models import *

class ReuniaoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Reuniao.objects.all()

        if self.q:

            qs = qs.filter(tipoReuniao__istartswith=self.q)
        return qs

class UsuarioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Usuario.objects.filter(Situacao=True)

        if self.q:

            qs = qs.filter(Nome__istartswith=self.q)
        return qs
