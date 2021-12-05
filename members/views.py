from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from posts.models import Posts, Comments, Likes, Notifications as db_notifications
from django.db.models import Avg, Count, Min, Sum, Count, Subquery, OuterRef
from sql_util.utils import SubqueryCount
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Profile as db_profile

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
    get_notifications = Notifications(request.user.id)
    page = request.GET.get('page', 1)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)

            elif request.POST.get('delete_id'):
                query = User.objects.filter(id = request.POST.get('delete_id'))
                query.delete()

                messages.success(request, 'Member Berhasil Di Hapus!')

                return redirect('members')
            else:
                return redirect('members')

        elif request.GET.get('orderby'):
            if request.GET.get('orderby') == '0':
                get_members = User.objects.filter(is_superuser = 0).annotate(total = Sum(Subquery(Posts.objects.filter(author_id = OuterRef('id')).values('author_id').annotate(count=Count('author_id')).values('count')))).values('total','username','email','id','date_joined').order_by('-date_joined')
            elif request.GET.get('orderby') == '1':
                get_members = User.objects.filter(is_superuser = 0).annotate(total = Sum(Subquery(Posts.objects.filter(author_id = OuterRef('id')).values('author_id').annotate(count=Count('author_id')).values('count')))).values('total','username','email','id','date_joined').order_by('date_joined')
            else:
                return redirect('index_posts')

        else:
            get_members = db_profile.objects.filter(users_id__is_superuser = 0).annotate(total = Sum(Subquery(Posts.objects.filter(author_id = OuterRef('users_id')).values('author_id').annotate(count=Count('author_id')).values('count')))).values('total','users_id__username','users_id__email','users_id','users_id__date_joined', 'users_id__first_name', 'users_id__last_name','updated_at').order_by('?')
            # get_members = User.objects.filter(is_superuser = 0).annotate(total = Sum(Subquery(Posts.objects.filter(author_id = OuterRef('id')).values('author_id').annotate(count=Count('author_id')).values('count')))).values('total','username','email','id','date_joined').order_by('?')

        paginator = Paginator(get_members, 10)

        try:
            list_members = paginator.page(page)
        except PageNotAnInteger:
            list_members = paginator.page(1)
        except EmptyPage:
            list_members = paginator.page(paginator.num_pages)
        return render(request, 'index_members.html', {'members': list_members})

    else:
        return redirect('login')
