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