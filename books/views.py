# books/views.py
from django.http import JsonResponse
from django.views import View
from .documents import BookDocument
from elasticsearch_dsl import Q

class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        if not q:
            return JsonResponse({'results': []})
        # búsqueda multi-campo con fuzziness
        query = Q("multi_match", query=q, fields=['title', 'author', 'description', 'tags'], fuzziness='AUTO')
        s = BookDocument.search().query(query)[:50]  # top 50
        results = []
        for hit in s.execute():
            results.append({
                'id': hit.meta.id,
                'title': hit.title,
                'author': getattr(hit, 'author', ''),
                'description': getattr(hit, 'description', ''),
                'score': hit.meta.score,
            })
        return JsonResponse({'results': results})
