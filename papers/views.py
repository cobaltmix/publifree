from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ResearchPaperForm, ProfileUpdateForm, ContactForm
from .models import User, ResearchPaper
from django.core.mail import EmailMessage
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        form = ResearchPaperForm(request.POST, request.FILES)
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

    user_papers = ResearchPaper.objects.filter(
        author=request.user, is_published=True
    )  # Fetch user's published papers

    context = {"u_form": u_form, "user_papers": user_papers}

    return render(request, "papers/profile.html", context)


@login_required
def delete_paper(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk, author=request.user)
    paper.delete()
    messages.success(request, "Your paper has been deleted!")
    return redirect("profile")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            user_email = form.cleaned_data["user_email"]
            recipient_list = ["spacedailyfacts@gmail.com"]

            email = EmailMessage(
                subject=subject,
                body=content,
                from_email=user_email,
                to=recipient_list,
            )
            email.send()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "papers/contact.html", {"form": form})


def view_papers(request):
    query = request.GET.get("q")
    papers = ResearchPaper.objects.filter(is_published=True)
    if query:
        papers = papers.filter(
            Q(title__icontains=query)
            | Q(abstract__icontains=query)
            | Q(keywords__icontains=query)
        )
    return render(request, "papers/view_papers.html", {"papers": papers})


def leaderboard_papers(request):
    leaderboard = User.objects.annotate(paper_count=Count("researchpaper")).order_by(
        "-paper_count"
    )
    return render(
        request, "papers/leaderboard_papers.html", {"leaderboard": leaderboard}
    )


def leaderboard_views(request):
    leaderboard = User.objects.annotate(
        view_count=Sum("researchpaper__views")
    ).order_by("-view_count")
    return render(
        request, "papers/leaderboard_views.html", {"leaderboard": leaderboard}
    )


@csrf_exempt
def increment_view(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    paper.views += 1
    paper.save()
    return JsonResponse({"status": "success"})


def get_paper_details(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    return JsonResponse(
        {
            "title": paper.title,
            "abstract": paper.abstract,
            "average_rating": paper.average_rating,
            "rating_count": paper.rating_count,
        }
    )


@csrf_exempt
def increment_view(request, pk):
    paper = get_object_or_404(ResearchPaper, pk=pk)
    paper.views += 1
    paper.save()
    return JsonResponse({"status": "success"})


@csrf_exempt
def rate_paper(request, pk):
    if request.method == "POST":
        paper = get_object_or_404(ResearchPaper, pk=pk)
        rating = int(request.POST.get("rating", 0))
        if 1 <= rating <= 5:
            paper.total_ratings += 1
            paper.rating_sum += rating
            paper.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})
