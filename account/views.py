from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserChangeForm # SuperUserCreationForm
from .models import User, Equipment, Tool, Resource, Statistics

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('home')

# class CreateSuperUserView(CreateView):
#     form_class = SuperUserCreationForm
#     template_name = 'superuser_create.html'
#     success_url = reverse_lazy('home')

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#
#             # tworzenie użytkownika
#             user = User.objects.create_user(username=username, email=email, password=password)
#             messages.success(request, f"Konto {user.username} zostało utworzone.")
#             return redirect('home')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'registration/user_create.html', {'form': form})

# def logout_user(request):
#     if request.method == "POST":
#         logout(request)
#         return redirect('login')
#     return redirect('home')

@login_required
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'username': request.user.username,
        })
    else:
        return JsonResponse({'error': 'Nie zalogowano użytkownika'}, status=401)

class ResourcesView(View):
    def get(self, request):
        username = get_authenticated_user(request)
        print(username)
        # _id = User.objects.filter(username=username).id
        all_resources = Resource.objects.filter()
        all_resources_list = []
        for resource in all_resources:
            all_resources_list.append(resource)

        ctx = {'all_resources': all_resources_list,
               'username': username}

        return render(request, "resources.html", ctx)

class StatisticsView(View):
    def get(self, request):
        all_statistics = Statistics.objects.all()
        all_statistics_list = []
        for statistic in all_statistics:
            all_statistics_list.append(statistic)

        ctx = {'all_statistics': all_statistics_list}

        return render(request, "statistics.html", ctx)

class EquipmentView(View):

    def get(self, request):
        all_items = Equipment.objects.all()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)

        ctx = {'all_items': all_items_list}

        return render(request, "equipment.html", ctx)

