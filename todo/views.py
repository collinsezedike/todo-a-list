from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Todo
from datetime import datetime, date

DATE_FORMAT = "%Y-%m-%d"


def sort_todos_by_deadline(todos_list):
    deadlines = sorted([todo.deadline for todo in todos_list], reverse=True)
    # sorted_todos = {}
    # for deadline in deadlines:
    #     sorted_todos[deadline] = [todo for todo in todos_list if todo.deadline == date]
    
    # using dictionary comprehension
    sorted_todos = {deadline: [todo for todo in todos_list if todo.deadline == deadline] for deadline in deadlines}    
    return sorted_todos
    
        
# Create your views here.
def authenticate_user(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"]
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username, email=email)
            auth.login(request, user)
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            return redirect("/authenticate")
        else:
            new_user = User.objects.create(username=username, email=email)
            new_user.save()
            auth.login(request, new_user)
        return redirect("/")
    return render(request, "authenticate.html")


@login_required(login_url="/authenticate")
def logout_user(request):
    auth.logout(request)
    return redirect("/authenticate")


@login_required(login_url="/authenticate")
def get_all_todos(request):
    current_user = auth.get_user(request)
    todos = sort_todos_by_deadline(Todo.objects.filter(user=current_user).all())
    context = {
        "page_title": "Todo List",
        "todos": todos
    }   
    return render(request, "index.html", context=context)


@login_required(login_url="/authenticate")
def get_todo_by_id(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if date.today() > todo.deadline:
        todo.is_overdue = True
        todo.save()
    return render(request, "todo.html", {"todo": todo} )


@login_required(login_url="/authenticate")
def complete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if todo.is_complete:
        todo.is_complete = False
    else:
        todo.is_complete = True
    todo.save()
    return redirect(f"/todo/{todo_id}")


@login_required(login_url="/authenticate")
def add_todo(request):
    if request.method == "POST":
        current_user = auth.get_user(request)
        new_todo_task = request.POST["task"]
        new_todo_deadline = request.POST["deadline"]
        new_todo = Todo.objects.create(user=current_user, task=new_todo_task, deadline=new_todo_deadline)
        new_todo.save()
        return redirect("/")
    else:
        context = {
            "page_title": "Add todo",
            "deadline": datetime.now().strftime(DATE_FORMAT),
            "button_text": "Add task",
        }
        return render(request, "todoform.html", context=context)
    

@login_required(login_url="/authenticate")  
def edit_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    
    if request.method == "POST":
        todo.task = request.POST["task"]
        todo.deadline = request.POST["deadline"]
        todo.save()
        return redirect(f"/todo/{todo_id}")
    else:
        context = {
            "page_title": "Edit todo",
            "task": todo.task,
            "deadline": todo.deadline.strftime(DATE_FORMAT),
            "button_text": "Edit task",
        }
        return render(request, "todoform.html", context=context)


@login_required(login_url="/authenticate")
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect("/")


@login_required(login_url="/authenticate")
def search_todo(request):
    current_user = auth.get_user(request)
    search_term = request.GET["search_term"].lower()
    all_todos = Todo.objects.filter(user=current_user).all()
    matching_todos = [todo for todo in all_todos if search_term in todo.task.lower()]
    context = { 
        "matching_todos": matching_todos,
        "search_term": search_term,
    }
    return render(request, "search.html", context)