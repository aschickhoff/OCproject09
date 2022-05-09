from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.core.exceptions import PermissionDenied
from itertools import chain
from .models import Ticket, Review
from .forms import CreateTicket, CreateReview
from followers.models import UserFollows


@login_required
def feed(request):
    # get all followed user
    f_users = []
    u_followed = UserFollows.objects.filter(user=request.user)
    for u_follow in u_followed:
        f_users.append(u_follow.followed_user)

    # to ask about
    f_user_me = f_users
    f_user_me.append(request.user)
    tickets = Ticket.objects.filter(user__in=f_users).order_by("-time_created")
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = Review.objects.filter(user__in=f_users).order_by("-time_created")
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    visible_feeds = sorted(chain(tickets, reviews), key=lambda visible_feeds: visible_feeds.time_created, reverse=True)
    context = {'visible_feeds': visible_feeds, 'f_users': f_users}
    return render(request, "reviews/home.html", context)


@login_required
def posts(request):
    own_tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    own_tickets = own_tickets.annotate(content_type=Value("TICKET", CharField()))
    own_reviews = Review.objects.filter(user=request.user).order_by("-time_created")
    own_reviews = own_reviews.annotate(content_type=Value("REVIEW", CharField()))
    own_posts = sorted(chain(own_tickets, own_reviews), key=lambda own_posts: own_posts.time_created, reverse=True)
    return render(request, 'reviews/posts.html', {'own_posts': own_posts})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        t_form = CreateTicket(request.POST, request.FILES)
        if t_form.is_valid():
            ticket = t_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('reviews:review-home')
    else:
        t_form = CreateTicket()
    context = {'t_form': t_form, 'task': 'Create'}
    return render(request, 'reviews/ticket_form.html', context)


@login_required
def create_review(request):
    if request.method == 'POST':
        t_form = CreateTicket(request.POST, request.FILES)

        if t_form.is_valid():
            ticket = t_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            r_form = CreateReview(request.POST)
            if r_form.is_valid:
                review = r_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()
            return redirect('reviews:review-home')
    else:
        t_form = CreateTicket()
        r_form = CreateReview()

    context = {'t_form': t_form, 'r_form': r_form, 'task': 'Create'}
    return render(request, 'reviews/review_form.html', context)


@login_required
def response_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        r_form = CreateReview(request.POST)

        if r_form.is_valid:
            review = r_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
        return redirect('reviews:review-home')
    else:
        r_form = CreateReview()

    context = {'r_form': r_form, 'ticket': ticket}
    return render(request, 'reviews/review_form.html', context)


@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.user != request.user:
        raise PermissionDenied()

    if request.method == "POST":
        t_form = CreateTicket(request.POST, request.FILES, instance=ticket)
        if t_form.is_valid():
            t_update = t_form.save(commit=False)
            t_update.user = request.user
            t_update.save()
            return redirect("/")
    else:
        t_form = CreateTicket(instance=ticket)
    context = {"t_form": t_form, 'task': 'Update'}
    return render(request, "reviews/ticket_form.html", context)


@login_required
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    if review.user != request.user:
        raise PermissionDenied()

    if request.method == "POST":
        r_form = CreateReview(request.POST, request.FILES, instance=review)
        if r_form.is_valid():
            r_update = r_form.save(commit=False)
            r_update.user = request.user
            r_update.save()
            return redirect("/")
    else:
        r_form = CreateReview(instance=review)
    context = {"r_form": r_form, "ticket": review.ticket, 'task': 'Update'}
    return render(request, "reviews/review_form.html", context)


@login_required
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.user == ticket.user:
        ticket.delete()
    return redirect("reviews:review-home")


@login_required
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    if request.user == review.user:
        review.delete()
    return redirect("reviews:review-home")


@login_required
def answer_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == "POST":
        r_form = CreateReview(request.POST)
        if r_form.is_valid():
            review = r_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("reviews:review-home")
    else:
        r_form = CreateReview()
    context = {"r_form": r_form, "ticket": ticket}
    return render(request, "reviews/review_form.html", context)
