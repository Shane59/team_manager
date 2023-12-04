from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from .models import Member

class MemberView(generic.ListView):
    template_name = "teammanager/index.html"
    context_object_name = "existing_members"

    def get_queryset(self):
        return Member.objects.order_by("id")

class EditView(generic.DetailView):
    model = Member
    template_name = "teammanager/edit.html"

class AddView(CreateView):
    model = Member
    template_name = "teammanager/add.html"
    fields = ["first_name"]

def add_member(request):
    try:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        location = request.POST['location']
        role = request.POST['role']
        admin = False
        if (role == "admin"):
            admin = True
        newMember = Member(first_name=first_name, last_name=last_name, email=email, location=location, is_admin=admin)
        newMember.save()
    except (KeyError, Member.DoesNotExist):
        return render(
            request,
            "teammanager/add.html", {
                "error_message": "Please input all the required field."
            }
        )
    return HttpResponseRedirect("/teammanager")

def edit_member(request, pk):
    member = Member.objects.get(id=pk)
    try:
        member.first_name = request.POST['first_name']
        member.last_name = request.POST['last_name']
        member.email = request.POST['email']
        member.location = request.POST['location']
        role = request.POST['role']
        member.is_admin = False
        if (role == "admin"):
            member.is_admin = True
        member.save()
    except (KeyError, Member.DoesNotExist):
        return render(
            request,
            "teammanager/edit.html", {
                "error_message": "Please input all the required field."
            }
        )
    return HttpResponseRedirect("/teammanager")

def delete_member(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except (KeyError, Member.DoesNotExist):
        return render(
            request,
            "teammanager/index.html", {
                "error_message": "The member does not exist."
            }
        )
    member.delete()
    return HttpResponseRedirect("/teammanager")