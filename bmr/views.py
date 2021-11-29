from django.shortcuts import render
from .forms import BMRForm, UserRegistrationForm, FoodItemForm
from .models import BMRDetail

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def calculate_bmr_gender_based(gender, weight, height, age):
    male_formula = (10 * weight) + (6.25 * height) - (5 * age) + 5
    female_formula = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return male_formula if gender == "m" else female_formula


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BMRForm(request.POST)
            if form.is_valid():
                gender = form.cleaned_data['gender']
                weight = form.cleaned_data['weight']
                height = form.cleaned_data['height']
                age = form.cleaned_data['age']
                life_style = form.cleaned_data['life_style']
                bmr_object = form.save()

                calculated_bmr = calculate_bmr_gender_based(gender, weight, height, age)
                if life_style == 1:
                    calculated_bmr = calculated_bmr * 1.2
                if life_style == 2:
                    calculated_bmr = calculated_bmr * 1.375
                if life_style == 3:
                    calculated_bmr = calculated_bmr * 1.55
                if life_style == 4:
                    calculated_bmr = calculated_bmr * 1.725
                if life_style == 5:
                    calculated_bmr = calculated_bmr * 1.9
                bmr_object.bmr = calculated_bmr
                bmr_object.user = request.user
                bmr_object.save()
                return redirect("home")
        # in case of get request
        else:
            form = BMRForm()
            user = request.user
            bmr_details = BMRDetail.objects.filter(user=request.user.id)
            context = {
                "form": form,
                "user": user,
                "bmr_details": bmr_details,
            }
            return render(request, "bmr/bmr_input.html", context)
    else:
        return redirect("sign_in")


def signup(request):
    context = {

    }
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")
    else:
        form = UserRegistrationForm()
        context["form"] = form
    return render(request, "bmr/signup.html", context)


def sign_in(request):
    context = {

    }
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
        context["form"] = form
    return render(request, "bmr/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("sign_in")


def add_food_item(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = FoodItemForm()
            return render(request, "bmr/addItemsCalories.html", {"form": form})
        elif request.method == "POST":
            pass
    else:
        return redirect("sign_in")
