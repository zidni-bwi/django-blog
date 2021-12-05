from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, LoginForm
from accounts.models import Profile
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from posts.models import Notifications as db_notifications

def Notifications(id_user):
    get_notifications = db_notifications.objects.filter(comments_id__posts_id__author_id = id_user).values('id','comments_id','likes_id','comments_id__users_id__username','likes_id__users_id__username', 'comments_id__posts_id', 'likes_id__posts_id', 'status') | db_notifications.objects.filter(likes_id__posts_id__author_id = id_user).values('id','comments_id','likes_id','comments_id__users_id__username','likes_id__users_id__username', 'comments_id__posts_id', 'likes_id__posts_id', 'status')
    return get_notifications

def Notice(notification_id):
    query = db_notifications.objects.filter(id = notification_id).values('likes_id','comments_id','likes_id__posts_id','comments_id__posts_id').first()
    if query['likes_id'] != None:
        set_status = db_notifications(id = notification_id)
        set_status.likes_id = query['likes_id']
        set_status.status = 1
        set_status.save()
        get_post_id = query['likes_id__posts_id']
    elif query['comments_id'] != None:
        set_status = db_notifications(id = notification_id)
        set_status.comments_id = query['comments_id']
        set_status.status = 1
        set_status.save()
        get_post_id = query['comments_id__posts_id']

    return get_post_id

def Index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)
        else:
            get_notifications = Notifications(request.user.id)
            users = User.objects.filter(id = request.user.id).first()
            profile = Profile.objects.filter(users_id = request.user.id).first()
            return render(request, 'index_accounts.html', {'users': users, 'profile': profile, 'notifications': get_notifications})
    else:
        return redirect('login')

class ChangePasswordView(PasswordChangeView):
    template_name = 'edit_password.html'

def Edit(request):
    check_profile = Profile.objects.filter(users_id = request.user.id).first()

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.method == 'POST':
                if request.POST.get('action') == 'notice':
                    notice = Notice(request.POST.get('notification_id'))
                    return redirect('detail_posts', notice)
            elif check_profile:
                user_form = UpdateUserForm(request.POST, instance=request.user)
                profile = Profile.objects.filter(users_id = request.user.id).first()

                if user_form.is_valid():
                    user_form.save()
                    profile.photo = request.POST.get('thumbnail')
                    profile.updated_at = now()
                    profile.save()

                query = Profile.objects.filter(users_id = request.user.id).first()

                messages.success(request, 'Profile Berhasil Di Update!')

                return render(request, 'index_accounts.html', {'profile': query})
            else:
                profile = Profile()
                profile.users_id = request.user.id
                profile.save()

                user_form = UpdateUserForm(request.POST, instance=request.user)
                profile = Profile.objects.filter(users_id = request.user.id).first()

                if user_form.is_valid():
                    user_form.save()
                    profile.photo = request.POST.get('thumbnail')
                    profile.updated_at = now()
                    profile.save()

                query = Profile.objects.filter(users_id = request.user.id).first()

                messages.success(request, 'Profile Berhasil Di Update!')

                return render(request, 'index_accounts.html', {'profile': query})

        else:
            get_notifications = Notifications(request.user.id)

            profile = Profile.objects.filter(users_id = request.user.id).first()
            user_form = UpdateUserForm(instance=request.user)
            return render(request, 'edit_accounts.html', {'user_form': user_form, 'profile': profile, 'notifications': get_notifications} )
    else:
        return redirect('login')

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


def Register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        profile = Profile()
        if form.is_valid():
            form.save()
            users_id = getattr(User.objects.filter(username = request.POST.get('username')).first(), "id")
            profile.users_id = users_id
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun baru telah berhasil dibuat, dengan username: {username}!')
            password = form.cleaned_data.get('password1')
            return redirect("register")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
                messages.success(request,form.error_messages[msg])

            return render(request=request,
                          template_name="auth/register.html",
                          context={"form": form})

    form = SignUpForm
    return render(request=request,
                  template_name="auth/register.html",
                  context={"form": form})
