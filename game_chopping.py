import os
import django
import json
# import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'island.settings')
django.setup()

from account.models import User, RESOURCE, Resource
all_usernames = User.objects.all()
user_logged = 'macius'

# def saveToDB(request):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#     u = Resource(**body)
#     u.save()

resources_list=[]
for each in RESOURCE:
    resources_list.append(each[1])

# Python object (dict)
resource1 = Resource(resource_name='stone_ore', resource_amount=75)
resource2 = Resource(resource_name='sulfur_ore', resource_amount=20)
resource1_dict = {
    "resource_name": resource1.resource_name,
    "resource_amount": resource1.resource_amount,
}
resource2_dict = {
    "resource_name": resource2.resource_name,
    "resource_amount": resource2.resource_amount,
}

resource_json = json.dumps([resource1_dict, resource2_dict])

# json_str = resource_json.toString()

# print(user_logged)
# print(all_usernames[0])
# print(User)

print(f'resources dict: {resource1_dict}')
print(f'resources json: {resource_json}')
# new_res = Resource.objects.create(resource_name='sulfur_ore', resource_amount='14')
x = json.loads(resource_json)
print(x[0])
print(len(RESOURCE))
print(resources_list)
