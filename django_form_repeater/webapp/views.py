from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView, UpdateView, TemplateView
from .models import *
from .forms import *


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        grandparents = GrandParent.objects.all()
        context["grandparents"] = grandparents
        return context


class GrandParentCreate(View):
    template_name = 'grandparent.html'

    def get(self, request):
        grand_parent = GrandParentForm()
        parentformset = parent_formset(prefix="parent")
        context = {"grand_parent": grand_parent, "parent_formset": parentformset}
        return render(request, self.template_name, context)

    def post(self, request):
        grand_parent = GrandParentForm(request.POST, request.FILES)
        parentformset = parent_formset(request.POST, request.FILES, prefix="parent")
        context = {"grand_parent": grand_parent, "parent_formset": parentformset}
        if grand_parent.is_valid():
            instance = grand_parent.save(commit=False)
            parentformset = parent_formset(request.POST, request.FILES, prefix="parent", instance=instance)
            if parentformset.is_valid():
                instance.save()
                parentformset.save()
            else:
                return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)

        return redirect("home")
