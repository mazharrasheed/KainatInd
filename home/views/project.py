
from django.shortcuts import render, redirect,get_object_or_404
from home.models import Project
from home.forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.add_project', login_url='/login/')
def add_project(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
       
        mydata=Project.objects.filter(is_deleted=False)
        form = ProjectForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Project Added successfully !!")
          return redirect('project')
    else:
        mydata=Project.objects.filter(is_deleted=False)
        
        form = ProjectForm()
    data={'form': form, 'mydata':mydata,}
    return render(request, 'projects/add_project.html', data)
  else:
    return redirect('signin')
@login_required
@permission_required('home.change_project', login_url='/login/')
def edit_project(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Project.objects.get(id=id)
      form = ProjectForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Project Updated successfully !!")
        return redirect('project')
    else:
      mydata=Project.objects.get(id=id)
      form = ProjectForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True }
  return render(request, 'projects/add_project.html', data)


# @login_required
# @permission_required('home.view_delete', login_url='/login/')

# def delete_project(request,id):
 
#     mydata=Project.objects.get(id=id)
#     mydata.is_deleted=True
#     mydata.save()
#     messages.success(request,"Project Deleted successfully !!")
#     return redirect('project')

from django.db.models.deletion import ProtectedError

@login_required
@permission_required('home.view_delete', login_url='/login/')
def delete_project(request, id):
    try:
        mydata = get_object_or_404(Project, id=id)
        mydata.delete()
        messages.success(request, "Project Deleted successfully !!")
    except ProtectedError as e:
        related_objects = e.protected_objects  # Get the related objects that are blocking the delete
        messages.error(
            request, 
            f"Cannot delete '{mydata.name}' because it is referenced by: "
            f"{', '.join([str(obj) for obj in related_objects])}. Please delete the related objects first."
        )
    return redirect('project')