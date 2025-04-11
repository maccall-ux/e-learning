from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.http import FileResponse,HttpResponseForbidden
from .models import Topic,Entry,UploadedFile
from .forms import TopicForm,EntryForm,FileUploadForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import Http404
import os
from django.views.generic import DeleteView
from django.db import models

# Create your views here.
def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    #post data submitted
    if request.method == 'POST':
        form=TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    else:
        #post data not submitted
        form=TopicForm()
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('learning_logs:topic',topic.id)
    else:
        form=EntryForm()

    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method=='POST':
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic.id)
    else:
        form=EntryForm(instance=entry)
    context={'entry':entry,'topic':topic,"form":form}
    return render(request,'learning_logs/edit_entry.html',context)

@login_required
def edit_topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method=='POST':
        form=TopicForm(instance=topic,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    else:
        form=TopicForm(instance=topic)
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/edit_topic.html',context)


"""def files(request):
    files=uploadfiles.objects.all()
    context={'files':files}
    return render(request,'learning_logs/files.html',context)


def uploadfile(request):
    if request.method=='POST':
        form=UploadFileForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:files')
    else:
        form=UploadFileForm()
    context={'form':form}
    return render(request,'learning_logs/uploadfile.html',context)

def view_file(request, pk):
    file_obj = get_object_or_404(uploadfiles, pk=pk)
    
    # Open the file in binary mode
    file = file_obj.file.open('rb')
    
    # Determine content type more robustly
    filename = file_obj.file.name
    extension = os.path.splitext(filename)[1].lower()
    
    content_types = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
    }
    
    content_type = content_types.get(extension, 'application/octet-stream')
    
    response = FileResponse(file, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(filename)}"'
    return response"""


@login_required
def file_list(request):
    files = UploadedFile.objects.filter(
        models.Q(is_private=False) | 
        models.Q(owner=request.user) |
        models.Q(owner__is_superuser=True)
    ).distinct().order_by('-uploaded_at')
    return render(request, 'learning_logs/file_list.html', {'files': files})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return redirect('learning_logs:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'learning_logs/upload.html', {'form': form})


@login_required
def view_file(request, pk):
    file_obj = get_object_or_404(UploadedFile, pk=pk)
    
    # Check permissions
    if file_obj.is_private and not request.user.is_superuser and file_obj.owner != request.user:
        return HttpResponseForbidden("You don't have permission to access this file")
    
    # File serving logic remains the same
    file = file_obj.file.open('rb')
    filename = file_obj.file.name
    extension = os.path.splitext(filename)[1].lower()
    
    content_types = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
    }
    
    content_type = content_types.get(extension, 'application/octet-stream')
    
    response = FileResponse(file, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(filename)}"'
    return response

@login_required
def admin_file_list(request):
    if request.user.is_superuser:
          files = UploadedFile.objects.all().order_by('-uploaded_at')
          return render(request, 'learning_logs/admin_file_list.html', {'files': files})
    else:
          return HttpResponseForbidden("<h4>You don't have permission to access this link</h4>")
    


class topicdeleteview(DeleteView):
    model=Topic
    template_name = "learning_logs/delete.html"
    success_url= reverse_lazy('learning_logs:topics')

#@user_passes_test(lambda u: u.is_superuser)
class uploadfiledeleteview(DeleteView):
    model=UploadedFile
    template_name = "learning_logs/delete.html"
    success_url= reverse_lazy('learning_logs:file_list')