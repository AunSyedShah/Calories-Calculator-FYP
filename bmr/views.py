from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
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
                return render(request, "bmr_input.html", context)
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
        return render(request, "dashboard.html", context)
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
            messages.error(request, "Error in submitting form!, Your password might br too common")
            return redirect("signup")
    else:
        form = UserRegistrationForm()
        context["form"] = form
    return render(request, "signup.html", context)


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
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("sign_in")


def add_food_item(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = FoodItemForm()
            return render(request, "addItemsCalories.html", {"form": form})
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
        context = {}
        if request.method == "GET":  # get request
            return render(request, "calories_detail.html")
        if request.method == "POST":  # post request
            if "selected_date_btn" in request.POST:
                items_by_user = FoodItem.objects.filter(user=request.user.id)
                calories_range = items_by_user.filter(date_added=request.POST.get("selected_date"))
                context = {
                    "items": calories_range,
                }
                return render(request, "calories_detail.html", context)
            if "selected_month_btn" in request.POST:
                selected_month_with_year = request.POST.get("selected_month")
                year_from_string = selected_month_with_year[:4]
                month_from_string = selected_month_with_year[5:7]
                data = FoodItem.objects.filter(date_added__year=year_from_string,
                                               date_added__month=month_from_string, user=request.user.id)
                context["items"] = data
                return render(request, "calories_detail.html", context)
            if "selected_week_btn" in request.POST:
                selected_week = request.POST.get("selected_week")
                selected_week_number = selected_week[6:]
                selected_year = selected_week[:4]
                data = FoodItem.objects.filter(user=request.user.id, date_added__week=selected_week_number,
                                               date_added__year=selected_year)
                context["items"] = data
                return render(request, "calories_detail.html", context)
    elif not request.user.is_authenticated:  # if user is not authenticated
        return redirect("sign_in")


def calories_graph(request):
    if request.user.is_authenticated:
        if not BMRDetail.objects.filter(user=request.user.id):
            return redirect("home")
        context = {}
        user_bmr = BMRDetail.objects.get(user=request.user.id).bmr
        context["user_bmr"] = user_bmr
        if request.method == "GET":
            return render(request, "calories_graph.html", context)
        if request.method == "POST":
            selected_month_with_year = request.POST.get("selected_month")
            year_from_string = selected_month_with_year[:4]
            month_from_string = selected_month_with_year[5:7]
            food_items_qs = FoodItem.objects.filter(date_added__year=year_from_string,
                                                    date_added__month=month_from_string, user=request.user.id).order_by(
                'date_added')
            date_dictionary = {

            }
            for food_item in food_items_qs:
                if food_item.date_added in date_dictionary:
                    date_dictionary[food_item.date_added] += food_item.calories
                else:
                    date_dictionary[food_item.date_added] = food_item.calories
            context["items"] = date_dictionary
            calories_list_for_certain_day = []
            for item in date_dictionary.values():
                calories_list_for_certain_day.append(item)
            context["calories"] = calories_list_for_certain_day
            return render(request, "calories_graph.html", context)
    else:
        return redirect("sign_in")


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("sign_in")
    if not BMRDetail.objects.filter(user=request.user.id):
        return redirect("home")
    context = {}
    if request.method == "GET":
        user_profile_picture = BMRDetail.objects.get(user=request.user.id).user_profile_pic
        print(user_profile_picture)
        context["user_profile_picture"] = user_profile_picture
        return render(request, "edit_profile.html", context)
    if request.method == "POST":
        return render(request, "edit_profile.html", context)
