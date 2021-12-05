from django.shortcuts import render
from posts.models import Posts as db_posts, Notifications as db_notifications
from django.shortcuts import redirect
from django.contrib import messages
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

def index(request):
    get_notifications = Notifications(request.user.id)
    page = request.GET.get('page', 1)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)

            elif request.POST.get('delete_id'):
                query = db_posts.objects.filter(id = request.POST.get('delete_id'))
                query.delete()

                return redirect('index_posts')
            else:
                return redirect('index_posts')

        elif request.GET.get('orderby'):
            if request.GET.get('orderby') == '0':
                get_posts = db_posts.objects.filter(author_id = request.user.id).order_by('-created_at')
                orderby = "0"
                paginator = Paginator(get_posts, 6)
            elif request.GET.get('orderby') == '1':
                get_posts = db_posts.objects.filter(author_id = request.user.id).order_by('created_at')
                orderby = "1"
                paginator = Paginator(get_posts, 6)
            else:
                return redirect('index_posts')

        else:
            get_posts = db_posts.objects.filter(author_id = request.user.id).order_by('?')

        paginator = Paginator(get_posts, 5)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'index_posts.html', {'posts': posts, 'notifications': get_notifications})

    else:
        return redirect('login')

def add(request):
    get_notifications = Notifications(request.user.id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)

            elif request.POST.get('title') and request.POST.get('content'):
                if request.POST.get('thumbnail') == "":
                    post = db_posts()
                    post.title = request.POST.get('title')
                    post.content = request.POST.get('content')
                    post.author_id = request.user.id
                    post.save()

                    messages.success(request, 'Postingan Berhasil Di Tambahkan!')

                    return redirect('index_posts')
                else:
                    post = db_posts()
                    post.title = request.POST.get('title')
                    post.content = request.POST.get('content')
                    post.thumbnail = request.POST.get('thumbnail')
                    post.author_id = request.user.id
                    post.save()

                    messages.success(request, 'Postingan Berhasil Di Tambahkan!')

                    return redirect('index_posts')

        else:
            return render(request,'add_posts.html', {'notifications': get_notifications})
    else:
        return redirect('login')

def edit(request, posts_id=None):
    get_notifications = Notifications(request.user.id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'notice':
                notice = Notice(request.POST.get('notification_id'))
                return redirect('detail_posts', notice)

            elif request.POST.get('title') and request.POST.get('content'):
                if request.POST.get('thumbnail') == 'None' or request.POST.get('thumbnail') == '':
                    post = db_posts(id = posts_id)
                    post.title = request.POST.get('title')
                    post.content = request.POST.get('content')
                    post.author_id = request.user.id
                    post.save()

                    messages.success(request, 'Postingan Berhasil Di Update!')

                    return redirect('index_posts')
                else:
                    post = db_posts(id = posts_id)
                    post.title = request.POST.get('title')
                    post.content = request.POST.get('content')
                    post.thumbnail = request.POST.get('thumbnail')
                    post.author_id = request.user.id
                    post.save()

                    messages.success(request, 'Postingan Berhasil Di Update!')

                    return redirect('index_posts')
        else:
            query = db_posts.objects.get(id = posts_id)
            return render(request,'edit_posts.html', {'posts': query, 'notifications': get_notifications})
    else:
        return redirect('login')
