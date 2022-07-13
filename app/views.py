from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from app.models import Card, Activity


class CardsListView(ListView):
    queryset = Card.objects.all()
    template_name = "card_list.html"
    paginate_by = 10

    # def get_queryset(self):
    #     query = self.request.GET.get('q', '')
    #     print(query)
    #     object_list = self.queryset.all()
    #     if query:
    #         object_list = object_list.filter(number__icontains=query)
    #         print(object_list)
    #     return object_list


class CardsDetailView(DetailView, MultipleObjectMixin):
    queryset = Card.objects.all()
    template_name = "card.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Activity.objects.filter(card=self.get_object())
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context



