from django.shortcuts import render
from posts.models import Posts, Comments, Likes, Notifications as db_notifications
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum, Count
from django.shortcuts import redirect

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

        elif request.user.is_superuser:
            total_members = User.objects.filter(is_superuser = False).count()
            total_members_ext = User.objects.order_by('-date_joined').first()
            total_posts = Posts.objects.count()
            total_posts_ext = Posts.objects.order_by('-created_at').first()
            most_posts = Posts.objects.values('author_id__username').annotate(total = Count('id')).order_by('-total')[:5]

            most_likes = Likes.objects.values('posts_id', 'posts_id__title', 'posts_id__author_id__username').annotate(total = Count('posts_id')).order_by('-total')[:5]
            most_comments = Comments.objects.values('posts_id', 'posts_id__title', 'posts_id__author_id__username').annotate(total = Count('posts_id')).order_by('-total')[:5]
            return render(request, 'dashboard.html', {'total_members': total_members, 'total_members_ext': total_members_ext, 'total_posts': total_posts, 'total_posts_ext': total_posts_ext, 'most_posts': most_posts, 'most_likes': most_likes, 'most_comments': most_comments})
        else:
            get_notifications = Notifications(request.user.id)

            total_posts = Posts.objects.filter(author_id = request.user.id).count()
            total_posts_ext = Posts.objects.filter(author_id = request.user.id).order_by('-created_at').first()
            total_likes = Likes.objects.filter(posts_id__author_id = request.user.id).count()
            total_likes_ext = Likes.objects.filter(posts_id__author_id = request.user.id).order_by('-created_at').first()
            total_comments = Comments.objects.filter(posts_id__author_id = request.user.id).count()
            total_comments_ext = Comments.objects.filter(posts_id__author_id = request.user.id).order_by('-created_at').first()

            most_likes = Likes.objects.filter(posts_id__author_id = request.user.id).values('posts_id__title','posts_id__created_at', 'posts_id').annotate(total = Count('posts_id')).order_by('-total')[:5]
            most_comments = Comments.objects.filter(posts_id__author_id = request.user.id).values('posts_id__title','posts_id__created_at', 'posts_id').annotate(total = Count('posts_id')).order_by('-total')[:5]
            return render(request, 'dashboard.html', {'total_posts': total_posts, 'total_posts_ext': total_posts_ext, 'total_likes': total_likes, 'total_likes_ext': total_likes_ext, 'total_comments': total_comments, 'total_comments_ext': total_comments_ext, 'most_likes': most_likes, 'most_comments': most_comments, 'notifications': get_notifications})
    else:
        return redirect('login')
