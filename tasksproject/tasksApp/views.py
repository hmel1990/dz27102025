from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

tasks = []

@csrf_exempt
def task_list_view(request: HttpRequest):
    if request.method == 'POST':
        new_task = request.POST.get("task")
        if new_task:
            tasks.append(new_task)
        return HttpResponseRedirect(reverse("task_list"))

    html = """
    <html><body>
    <h2>Task List</h2>
    <form method="post">
        <input type="text" name="task" placeholder="New task">
        <button type="submit">Add</button>
    </form>
    <ul>
    """
    for i, task in enumerate(tasks):
        html += f"""
        <li>
            {task}
            <form method="post" action="{reverse('delete_task', args=[i])}" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
            <form method="get" action="{reverse('edit_task', args=[i])}" style="display:inline;">
                <button type="submit">Edit</button>
            </form>
        </li>
        """
    html += "</ul></body></html>"
    return HttpResponse(html)

# Удаление задачи
@csrf_exempt
def delete_task_view(request: HttpRequest, index: int):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return HttpResponseRedirect(reverse("task_list"))



# Редактирование задачи
@csrf_exempt
def edit_task_view(request: HttpRequest, index: int):
    if request.method == 'POST':
        new_text = request.POST.get("task")
        if new_text:
            tasks[index] = new_text
        return HttpResponseRedirect(reverse("task_list"))

    html = f"""
    <html><body>
    <h2>Edit Task</h2>
    <form method="post">
        <input type="text" name="task" value="{tasks[index]}">
        <button type="submit">Save</button>
    </form>
    </body></html>
    """
    return HttpResponse(html)

def result (request: HttpRequest):
    string = "result for /data/item/42/"
    return HttpResponse(string) 

import json

@csrf_exempt
def normalize_user_data(request: HttpRequest):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Проверка обязательных полей
    if "name" not in data or "age" not in data:
        return JsonResponse({"error": "Missing 'name' or 'age'"}, status=400)

    name = data["name"]
    age = data["age"]

    # Проверка типов
    if not isinstance(name, str):
        return JsonResponse({"error": "'name' must be a string"}, status=400)

    try:
        age = int(age)
    except (ValueError, TypeError):
        return JsonResponse({"error": "'age' must be an integer or string convertible to int"}, status=400)

    # Нормализация
    normalized = {
        "name": name.capitalize(),
        "age": age
    }

    return JsonResponse(normalized)


@csrf_exempt
def user_agent_check_view(request: HttpRequest):
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()

    # Примитивная проверка на мобильные устройства
    mobile_keywords = ["iphone", "android", "ipad", "mobile"]

    if any(keyword in user_agent for keyword in mobile_keywords):
        return HttpResponseRedirect("/mobile-page/")
    
    return HttpResponse("Добро пожаловать на сайт!")

data_dict = {}
def get_data_view(request: HttpRequest, key: str):
    if key in data_dict:
        return JsonResponse({key: data_dict[key]})
    return HttpResponse("Key not found", status=404)

@csrf_exempt
def update_data_view(request: HttpRequest):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    data_dict.update(payload)
    return JsonResponse({"status": "updated", "data": data_dict})
