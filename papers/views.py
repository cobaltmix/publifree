from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ResearchPaperForm, ProfileUpdateForm
from .models import ResearchPaper
from django.contrib import messages
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'papers/register.html', {'form': form})


@login_required
def submit_paper(request):
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            messages.success(request, f'Your paper has been submitted for review!')
            return redirect('view_papers')
    else:
        form = ResearchPaperForm()
    return render(request, 'papers/submit_paper.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = ProfileUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = ProfileUpdateForm(instance=request.user)

    user_papers = ResearchPaper.objects.filter(author=request.user, is_published=True)

    context = {
        'u_form': u_form,
        'user_papers': user_papers
    }

    return render(request, 'papers/profile.html', context)

@login_required
def delete_paper(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk, author=request.user)
    paper.delete()
    messages.success(request, 'Your paper has been deleted!')
    return redirect('profile')


def view_papers(request):
    query = request.GET.get('q')
    papers = ResearchPaper.objects.filter(is_published=True)
    if query:
        papers = papers.filter(Q(title__icontains=query) | Q(abstract__icontains=query))
    return render(request, 'papers/view_papers.html', {'papers': papers})