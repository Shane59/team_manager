from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from .models import Member, MemberForm
from django.shortcuts import get_object_or_404

class MemberView(ListView):
	context_object_name = "existing_members"
	queryset = Member.objects.order_by("id")
	template_name = "teammanager/index.html"

class EditView(UpdateView):
	model = Member
	form_model = MemberForm
	fields = '__all__'
	template_name = "teammanager/edit.html"
	success_url = ("/teammanager")
	
	def get_object(self, queryset=None):
		return get_object_or_404(Member, pk=self.kwargs['pk'])

class AddView(FormView):
	model = Member
	template_name = "teammanager/add.html"
	form_model = MemberForm
    
	def get(self, request):
		form = self.form_model()
		return render(request, self.template_name, {'form': form})
	
	def post(self, request):
		form = MemberForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			return render(
				request,
				"teammanager/add.html", {
					"error_message": "Please input all the required field."
				}
			)
		return HttpResponseRedirect("/teammanager")

class DeleteMember(DeleteView):
	model = Member
	success_url = ("/teammanager")
