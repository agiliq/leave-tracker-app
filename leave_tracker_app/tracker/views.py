from django.shortcuts import render
from forms import LeaveApplicationForm

from models import LeaveApplication, UserProfile, Leave

def index(request):
    
    return render(request, "index.html", {})

def apply(request, req_id=None):

    #import ipdb
    #ipdb.set_trace()
    req_data = None
    try:
        req_data = LeaveApplication.objects.get(id=req_id)
    except LeaveApplication.DoesNotExist:
        pass

    if request.user == "shabda":
        form = LeaveApplicationAdminForm(data=request.POST or None, instance=req_data)
    else:
        form = LeaveApplicationForm(data=request.POST or None, instance=req_data)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'index.html', {'form':form})
