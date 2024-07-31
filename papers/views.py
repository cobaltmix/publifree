from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ResearchPaperForm, ProfileUpdateForm
from .models import ResearchPaper
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "papers/register.html", {"form": form})


@login_required
def submit_paper(request):
    if request.method == "POST":
        form = ResearchPaperForm(request.POST)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            messages.success(request, f"Your paper has been submitted for review!")
            return redirect("view_papers")
    else:
        form = ResearchPaperForm()
    return render(request, "papers/submit_paper.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = ProfileUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")
    else:
        u_form = ProfileUpdateForm(instance=request.user)

    context = {"u_form": u_form}

    return render(request, "papers/profile.html", context)


def view_papers(request):
    query = request.GET.get("q")
    papers = ResearchPaper.objects.filter(is_published=True)
    if query:
        papers = papers.filter(title__icontains=query)
    return render(request, "papers/view_papers.html", {"papers": papers})
