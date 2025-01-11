from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from task.forms import TaskForm
from task.models import Task, Files
from django.contrib import messages

@login_required
def home(request):
    form = TaskForm()
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            # Save the uploaded files
            files = request.FILES.getlist('files')
            for file in files:
                Files.objects.create(task=task, file=file)
            
            form.save()
            messages.success(request, "Task created successfully!")
            return redirect("task:home")
        
    else:
        form = TaskForm()
    context = {'form': form, "user": request.user,
        'page_title': "Home",}
    return render(request, 'task/home.html', context)

