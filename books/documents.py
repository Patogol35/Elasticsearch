from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book

# nombre del índice en ES
book_index = Index('books')

# ajustes del índice si quieres (shards/replicas)
book_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class BookDocument(Document):
    # puedes mapear campos explícitos:
    title = fields.TextField(
        attr='title',
        fields={'raw': fields.KeywordField()}
    )
    author = fields.TextField()
    description = fields.TextField()
    published_date = fields.DateField()
    tags = fields.KeywordField(multi=True)

    class Index:
        name = 'books'  # coincide con el Index creado arriba

    class Django:
        model = Book  # modelo Django que se indexa
        # Campos adicionales a indexar automáticamente
        fields = [
            'isbn',
            'created_at',
        ]
