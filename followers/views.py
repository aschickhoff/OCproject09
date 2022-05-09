from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import FollowerForm
from .models import UserFollows


@login_required
def following(request):
    if request.method == 'POST':
        form = FollowerForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    messages.error(request, "You can't follow yourself!")
                else:
                    try:
                        UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        messages.success(request, "Success! You are following this user now.")
                    except IntegrityError:
                        messages.error(request, "You are following this user already!")
            except User.DoesNotExist:
                messages.error(request, "This user does not exist!")
    else:
        form = FollowerForm()

    user_follows = UserFollows.objects.filter(user=request.user).order_by('followed_user')
    followed_by = UserFollows.objects.filter(followed_user=request.user).order_by('user')

    context = {'form': form, 'user_follows': user_follows, 'followed_by': followed_by}
    return render(request, 'followers/followers.html', context)


@login_required
def unfollowing(request, user):
    user = User.objects.get(username=user)
    for followed in UserFollows.objects.all():
        if (followed.user, followed.followed_user) == (request.user, user):
            followed.delete()
    return redirect("/following")
