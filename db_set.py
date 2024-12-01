import os, django, json, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'island.settings')
django.setup()
import os
from account.models import RESOURCE, Resource, STATISTICS, Statistics, User
# from .main import userLogged


username = 'macioPikczu'
check_resources = Resource.objects.all()
_id = User.objects.get(username=username).id
# for i in range(1, len(RESOURCE)):

def setDataBase(dict, model, _id):
    """Create objects with 0 value in db's tables.
    dict - dictionary, for example: game = {(1, 'strategy'),(2, 'racing')}
    model - object model, for example Statistics:
        class Statistics(models.Model):
            name = models.IntegerField(choices=STATISTICS)
            record = models.IntegerField(default=0)"""

    for each in dict:
        if not model.objects.filter(name=each[1], user_id=_id).exists():
            model.objects.create(name=each[1], quantity=0, user_id=_id)

setDataBase(RESOURCE, Resource, _id)
setDataBase(STATISTICS, Statistics, _id)

print('---')
print(f'User id: {_id}')


print(f' in db: {check_resources}')
print(f'dict: {RESOURCE}')

# Ścieżka do bieżącego pliku
current_file_path = os.path.abspath(__file__)
print(f"Ścieżka do bieżącego pliku: {current_file_path}")

current_working_dir = os.getcwd()
print(f"Bieżący katalog roboczy: {current_working_dir}")