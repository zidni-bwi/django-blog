from django.shortcuts import render, redirect, HttpResponseRedirect
from posts.models import Posts as db_posts, Comments as db_comments, Likes as db_likes, Notifications as db_notifications
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def Home(request):
    get_notifications = Notifications(request.user.id)
    page = request.GET.get('page', 1)
    author = request.GET.get('author', None)
    orderby = request.GET.get('orderby', None)

    if request.user.is_authenticated and request.method == 'POST':
        if request.POST.get('action') == 'notice':
            notice = Notice(request.POST.get('notification_id'))
            return redirect('detail_posts', notice)

    elif request.GET.get('author') and request.GET.get('orderby'):
        if request.GET.get('orderby') == '0':
            get_author = db_posts.objects.filter(author_id = author).values('author_id__username').first()
            get_posts = db_posts.objects.filter(author_id = author).order_by('-created_at')
            paginator = Paginator(get_posts, 6)

        elif request.GET.get('orderby') == '1':
            get_author = db_posts.objects.values('author_id__username').filter(author_id = author).first()
            get_posts = db_posts.objects.filter(author_id = author).order_by('created_at')
            paginator = Paginator(get_posts, 6)

        else:
            return redirect('home')

    elif request.GET.get('author'):
        get_author = db_posts.objects.values('author_id__username').filter(author_id = author).first()
        get_posts = db_posts.objects.filter(author_id = author).order_by('?')
        paginator = Paginator(get_posts, 6)

    elif request.GET.get('orderby'):
        if request.GET.get('orderby') == '0':
            get_posts = db_posts.objects.order_by('-created_at')
            paginator = Paginator(get_posts, 6)
        elif request.GET.get('orderby') == '1':
            get_posts = db_posts.objects.order_by('created_at')
            paginator = Paginator(get_posts, 6)

        else:
            return redirect('home')

    else:
        get_posts = db_posts.objects.order_by('?')
        paginator = Paginator(get_posts, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.GET.get('author'):
        return render(request, 'home.html', {'posts': posts, 'author': get_author, 'notifications': get_notifications})
    else:
        return render(request, 'home.html', {'posts': posts, 'notifications': get_notifications})

def Detail_Posts(request, id_post = None):
    get_notifications = Notifications(request.user.id)
    get_post = db_posts.objects.filter(id = id_post).values('title', 'content', 'thumbnail', 'created_at', 'author__username', 'author_id').first()

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)

            elif request.POST.get('action') == 'comment':
                add_comment = db_comments()
                add_comment.content = request.POST.get('content')
                add_comment.posts_id = id_post
                add_comment.users_id = request.user.id
                add_comment.save()

                get_comment_id = db_comments.objects.filter(users_id = request.user.id).filter(posts_id = id_post).first()

                if getattr(db_posts.objects.filter(id = id_post).first(), 'author_id') != request.user.id:
                    add_notifications = db_notifications()
                    add_notifications.comments_id = get_comment_id.id
                    add_notifications.save()

                return redirect('detail_posts', id_post=id_post)

            elif request.POST.get('action') == 'upcomment':
                update_comment = db_comments(id = request.POST.get('comment_id'))
                update_comment.content = request.POST.get('content')
                update_comment.updated_at = now()
                update_comment.posts_id = id_post
                update_comment.users_id = request.user.id
                update_comment.save()

                return redirect('detail_posts', id_post=id_post)

            elif request.POST.get('action') == 'uncomment':
                delete_comment = db_comments.objects.filter(posts_id = id_post).filter(users_id = request.user.id)
                delete_comment.delete()

                return redirect('detail_posts', id_post=id_post)

            elif request.POST.get('action') == 'like':
                add_like = db_likes()
                add_like.posts_id = id_post
                add_like.users_id = request.user.id
                add_like.save()

                get_like_id = db_likes.objects.filter(users_id = request.user.id).filter(posts_id = id_post).first()

                if getattr(db_posts.objects.filter(id = id_post).first(), 'author_id') != request.user.id:
                    add_notifications = db_notifications()
                    add_notifications.likes_id = get_like_id.id
                    add_notifications.save()

                return redirect('detail_posts', id_post=id_post)

            elif request.POST.get('action') == 'unlike':
                delete_like = db_likes.objects.filter(posts_id = id_post).filter(users_id = request.user.id)
                delete_like.delete()

                return redirect('detail_posts', id_post=id_post)

            elif request.POST.get('action') == 'notice':
                set_status = db_notifications.objects.filter(id = request.POST.get('id'))
                set_status.status = 1
                set_status.save()

            else:
                get_posts = db_posts.objects.order_by('?')
                return render(request, 'home.html', {'posts': get_posts, 'notifications': get_notifications})
        else:
            get_comments = db_comments.objects.filter(posts_id = id_post).extra(select={'is_top': "users_id = " + str(request.user.id)}).order_by('-is_top','-created_at').values('id','content','created_at','updated_at','users_id','users__username')
            count_comment = db_comments.objects.filter(posts_id = id_post).filter(users_id = request.user.id).count()
            count_like = db_likes.objects.filter(posts_id = id_post).filter(users_id = request.user.id).count()
            return render(request, 'posts.html', {'post': get_post, 'comments': get_comments, 'c_comment': count_comment, 'c_like': count_like, 'notifications': get_notifications})
    else:
        get_comments = db_comments.objects.filter(posts_id = id_post).order_by('-created_at').values('id','content','created_at','updated_at','users_id','users__username')
        return render(request, 'posts.html', {'post': get_post, 'comments': get_comments})
