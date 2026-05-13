import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

from django.db import connection, reset_queries
from django.conf import settings
import time

settings.DEBUG = True

from seed_all import seed_all
from posts.models import Post

# Clear posts first
Post.objects.all().delete()

reset_queries()
start_time = time.time()

seed_all()

end_time = time.time()
queries = len(connection.queries)

print(f"Time taken: {end_time - start_time:.4f}s")
print(f"Queries executed: {queries}")
