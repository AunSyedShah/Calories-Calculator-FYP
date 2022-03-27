from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone

from .forms import BMRForm, UserRegistrationForm, FoodItemForm
from .models import BMRDetail
from .models import FoodItem


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
                bmr_object.bmr = int(calculated_bmr)
                bmr_object.user = request.user
                bmr_object.save()
                return redirect("home")
        # in case of get request
        elif request.method == "GET":
            context = {

            }
            bmr_details = BMRDetail.objects.filter(user=request.user.id)
            if bmr_details:
                return redirect("dashboard")
            else:
                form = BMRForm()
                user = request.user
                context["form"] = form
                context["user"] = user
                context["bmr_details"] = bmr_details
                return render(request, "bmr/bmr_input.html", context)
    else:
        return redirect("sign_in")


def dashboard(request):
    if request.user.is_authenticated:
        bmr = BMRDetail.objects.get(user=request.user.id).bmr
        food_items = FoodItem.objects.filter(user=request.user.id, date_added=timezone.now())
        total_calories = 0

        for food_item in food_items:
            total_calories += food_item.calories

        calories_status = bmr - total_calories
        context = {
            "bmr": bmr,
            "food_items": food_items,
            "total_calories": total_calories,
            "calories_status": calories_status,
            "today_date": timezone.now().date()
        }
        return render(request, "bmr/dashboard.html", context)
    else:
        return redirect("sign_in")


def signup(request):
    context = {

    }
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("sign_in")
        else:
            if request.POST["password1"] != request.POST["password2"]:
                messages.error(request, "password mismatch")
            username = request.POST['username']
            user = User.objects.filter(username=username).exists()
            if user:
                messages.error(request, "Username or email already taken")
            messages.error(request, "Error in submitting form, Try again!")
            return redirect("signup")
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
            if user:  # if user is authenticated
                login(request, user)  # login and create session

                # user has to enter details for calculating BMR
                bmr_details_entered = BMRDetail.objects.filter(user=request.user.id)
                if bmr_details_entered:  # if BMR details are already entered, redirect user to dashboard
                    messages.success(request, "Login Successful ")
                    return redirect("dashboard")
                else:  # in case BMR details are not entered, redirect user to home (BMR details page)
                    messages.success(request, "Login Successful")
                    return redirect("home")
        else:
            messages.error(request, "Wrong Credentials")
            return redirect("sign_in")
    elif request.method == "GET":  # login page as GET request
        if request.user.is_authenticated:
            return redirect("home")
        form = AuthenticationForm()
        context["form"] = form
    return render(request, "bmr/login.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("sign_in")


def add_food_item(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = FoodItemForm()
            return render(request, "bmr/addItemsCalories.html", {"form": form})
        elif request.method == "POST":
            form = FoodItemForm(request.POST)
            if form.is_valid():
                if int(form.cleaned_data["calories"]) < 1:
                    messages.error(request, "Minimum calorie value should be 1")
                    return redirect("addfooditem")
                form_item_object = form.save()
                form_item_object.user = request.user
                form.save()
                messages.success(request, "Food item successfully added")
                return redirect("addfooditem")
    else:
        return redirect("sign_in")


def delete_bmr(request, delete_id):
    record_to_delete = get_object_or_404(BMRDetail, id=delete_id)
    record_to_delete.delete()
    return redirect("home")


def calories_detail(request):
    if request.user.is_authenticated:  # if user is authenticated
        if request.method == "GET":  # get request
            items = FoodItem.objects.filter(user=request.user.id)
            today_calories = items.filter(date_added=timezone.now())
            some_day_last_week = timezone.now().date() - timedelta(days=7)
            monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
            monday_of_this_week = monday_of_last_week + timedelta(days=7)
            print(monday_of_this_week)
            calories_week = items.filter(date_added__gte=monday_of_last_week, date_added__lt=monday_of_this_week)
            context = {
                "items": today_calories,
                "calories_week": calories_week
            }
            return render(request, "bmr/calories_detail.html", context)
        if request.method == "POST":  # post request
            today_calories = FoodItem.objects.filter(user=request.user.id, date_added=request.POST.get("selected_date"))
            context = {
                "items": today_calories,
            }
            return render(request, "bmr/calories_detail.html", context)
    elif not request.user.is_authenticated:  # if user is not authenticated
        return redirect("sign_in")
