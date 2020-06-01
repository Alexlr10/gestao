from dal import autocomplete
from .models import *

class ReuniaoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Reuniao.objects.all()
        print(qs)

        if self.q:

            qs = qs.filter(tipoReuniao__istartswith=self.q)
            print(qs)
        return qs
