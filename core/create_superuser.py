from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

User = get_user_model()

try:
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "motdepasse123")
        print(" Superuser 'admin' créé avec succès !")
    else:
        print(" Superuser déjà existant.")
except OperationalError:
    print("Base de données non prête, impossible de créer le superuser.")
