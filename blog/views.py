from django.shortcuts import render
from blog.models import Comment, Post, Tag
from django.db.models import Count


def get_related_posts_count(tag):
    return tag.posts.count()


def serialize_post(post):
        return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
        return {
        'title': tag.title,
        'posts_with_tag': tag.tags_count,
    }

def get_likes_count(post):
    return post.likes.count()

def index(request):

    posts = Post.objects.popular()
    
    most_popular_posts = Post.objects.fetch_with_comments_count()[:5]

    fresh_posts = posts.order_by('-published_at')
    most_fresh_posts = fresh_posts[:5]
    most_fresh_posts_id = [fresh_post.id for fresh_post in most_fresh_posts]
    fresh_posts_with_comment = Post.objects.filter(id__in=most_fresh_posts_id).annotate(comments_count=Count('comments'))
    ids_and_comments = fresh_posts_with_comment.values_list('id','comments_count')
    count_for_id = dict(ids_and_comments)

    for post in most_fresh_posts:
        post.comments_count = count_for_id[post.id]
    
    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.fetch_comments(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment['text'],
            'published_at': comment['published_at'],
            'author': comment['author'],
        })

    likes = post.likes.all()

    related_tags = post.tags.popular()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': len(likes),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.fetch_with_comments_count()[:5]  # TODO. Как это посчитать?

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):

    tag = Tag.objects.get(title=tag_title)
    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.fetch_with_comments_count()[:5]

    related_posts = tag.posts.fetch_with_comments_count()[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
