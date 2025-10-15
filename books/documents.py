from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book

book_index = Index('books')
book_index.settings(number_of_shards=1, number_of_replicas=0)

@registry.register_document
class BookDocument(Document):
    title = fields.TextField(attr='title', fields={'raw': fields.KeywordField()})
    author = fields.TextField()
    description = fields.TextField()
    published_date = fields.DateField()
    tags = fields.KeywordField(multi=True, attr='tags')

    class Index:
        name = 'books'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Book
        fields = ['isbn', 'created_at']
