from rest_framework import generics
from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle
from .models import Post
from .serializers import PostSerializer


class PostRateThrottle(SimpleRateThrottle):
    scope = 'post_custom'

    def get_cache_key(self, request, view):
        
        if request.method != 'POST':
            return None

        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return f'post-throttle-{ident}'



class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'post_list'



class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    throttle_classes = [ScopedRateThrottle, PostRateThrottle]
    throttle_scope = 'post_create'