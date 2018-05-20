from django.contrib.syndication.views import Feed
from django.utils import timezone
from .models import Comentario
class myFeed(Feed):
    title = 'Canal RSS Comentarios'
    description = 'Todos los comentarios de Bosco'
    link = '/rss/'
    date = timezone.now()

    def items(self):
        return Comentario.objects.all()

    def item_link(self, item):
        return '/' + item.autor

    def item_decription(self, item):
        return item.texto

    def item_title(self, item):
        return item.autor + ', ' + str(item.fecha) + ': '
