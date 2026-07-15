from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from social_accounts.services.facebook_service import publish_post_to_facebook
from social_accounts.services.linkedin_service import publish_post_to_linkedin

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        
        # Get selected social accounts
        selected_accounts = post.social_accounts.all()
        
        # If no specific accounts selected, fall back to platform-based posting
        platforms = post.platforms or []
        any_success = False
        errors = []

        # Post to specifically selected accounts
        for account in selected_accounts:
            platform = account.platform
            
            if platform == "facebook":
                result = publish_post_to_facebook(post, account)
                if result.get('success'):
                    any_success = True
                else:
                    errors.append({"facebook": result})

            elif platform == "linkedin":
                result = publish_post_to_linkedin(post, account)
                if result.get('success'):
                    any_success = True
                else:
                    errors.append({"linkedin": result})

        # Fallback: if no specific accounts selected, use platform-based posting
        if not selected_accounts:
            if "facebook" in platforms:
                result = publish_post_to_facebook(post)
                if result.get('success'):
                    any_success = True
                else:
                    errors.append({"facebook": result})

            if "linkedin" in platforms:
                result = publish_post_to_linkedin(post)
                if result.get('success'):
                    any_success = True
                else:
                    errors.append({"linkedin": result})

        if any_success:
            post.status = "posted"
            post.save()
        elif errors:
            post.status = "failed"
            post.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
