from django.urls import path
from . import views


app_name='learning_logs'

urlpatterns=[
    path('',views.index,name='index'),
    # display al the topics
    path('topics/',views.topics,name='topics'),
    #individual topic
    path('topic/<int:topic_id>/',views.topic,name='topic'),
    #new topic
    path('new_topic/',views.new_topic,name='new_topic'),
    #new entry for aparticular topic
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    #edit existing entry
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
    #edit existing topic
    path('edit_topic/<int:topic_id>/',views.edit_topic,name='edit_topic'),
    # file upload
    path('upload_files/',views.upload_file,name='uploadfile'),
    # view files
    path('files/',views.file_list,name='file_list'),
    #view single file
    path('files/<int:pk>/', views.view_file, name='view_file'),
    # delete
    path('topic_delete/<int:pk>/',views.topicdeleteview.as_view(),name='topicdelete'),
     # delete
    path('file_delete/<int:pk>/',views.uploadfiledeleteview.as_view(),name='uploadfiledelete'),
    #admin only
    path('Admin/files/', views.admin_file_list, name='admin_file_list'),
]