import json
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SocialAccount
from posts.models import Post
from accounts.models import User


def get_facebook_login_url():
    """Generate Facebook OAuth login URL"""
    app_id = settings.FACEBOOK_APP_ID
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    scope = "pages_show_list,pages_read_engagement,pages_manage_posts,public_profile,email"
    
    url = (
        f"https://www.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/dialog/oauth"
        f"?client_id={app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
    )
    return url


def facebook_settings_configured():
    return bool(settings.FACEBOOK_APP_ID and settings.FACEBOOK_APP_SECRET)


def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/oauth/access_token"
    
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
        'code': code,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'access_token' in data:
        return data['access_token']
    return None


def get_facebook_user_info(access_token):
    """Get Facebook user information"""
    url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/me"
    
    params = {
        'access_token': access_token,
        'fields': 'id,name,email,picture'
    }
    
    response = requests.get(url, params=params)
    return response.json()


def get_facebook_pages(access_token):
    """Get list of Facebook pages the user manages"""
    url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/me/accounts"
    
    params = {
        'access_token': access_token,
    }
    
    response = requests.get(url, params=params)
    return response.json()


@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_login(request):
    """Initiate Facebook OAuth login"""
    if not facebook_settings_configured():
        return Response(
            {
                "error": (
                    "Facebook login is not configured. Set FACEBOOK_APP_ID "
                    "and FACEBOOK_APP_SECRET in your environment or settings."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    login_url = get_facebook_login_url()
    return JsonResponse({'login_url': login_url})


@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_callback(request):
    """Handle Facebook OAuth callback"""
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return JsonResponse({'error': 'Access denied or cancelled'}, status=400)
    
    if not code:
        return JsonResponse({'error': 'No authorization code provided'}, status=400)

    if not facebook_settings_configured():
        return JsonResponse(
            {'error': 'Facebook login is not configured'},
            status=400
        )
    
    # Exchange code for access token
    access_token = exchange_code_for_token(code)
    
    if not access_token:
        return JsonResponse({'error': 'Failed to get access token'}, status=400)
    
    # Get user info
    user_info = get_facebook_user_info(access_token)
    
    if 'id' not in user_info:
        return JsonResponse({'error': 'Failed to get user information'}, status=400)
    
    # Get pages
    pages_data = get_facebook_pages(access_token)
    
    # Get or create user based on Facebook email
    email = user_info.get('email', '')
    facebook_id = user_info.get('id', '')
    name = user_info.get('name', '')
    
    if not email:
        # If no email provided, use facebook_id as username
        email = f"facebook_{facebook_id}@facebook.com"
    
    # Try to find user by email
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': name.replace(' ', '_').lower(),
            'is_verified': True,  # Facebook verified the email
        }
    )
    
    # If user was created, set a random password (they can reset it later)
    if created:
        user.set_password(User.objects.make_random_password())
        user.save()
    
    # Store or update social account
    social_account, account_created = SocialAccount.objects.get_or_create(
        user=user,
        platform='facebook',
        defaults={
            'account_name': name,
            'account_id': facebook_id,
            'access_token': access_token,
            'is_connected': True,
        }
    )
    
    if not account_created:
        social_account.access_token = access_token
        social_account.is_connected = True
        social_account.save()
    
    # Generate JWT tokens for the user
    refresh = RefreshToken.for_user(user)
    
    # Return HTML with JavaScript to close popup and store tokens
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Login Success</title>
        <script>
            // Store tokens in localStorage
            localStorage.setItem('access', '{str(refresh.access_token)}');
            localStorage.setItem('refresh', '{str(refresh)}');
            localStorage.setItem('username', '{user.username}');
            
            // Close popup and reload parent window
            window.close();
            if (window.opener) {{
                window.opener.location.reload();
            }}
        </script>
    </head>
    <body>
        <h1>Login Successful!</h1>
        <p>You can close this window.</p>
    </body>
    </html>
    """
    
    return Response(html_response, content_type='text/html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_post_to_facebook(request, post_id):
    """Share a post to Facebook"""
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get the Facebook social account
    try:
        social_account = SocialAccount.objects.get(
            user=request.user,
            platform='facebook',
            is_connected=True
        )
    except SocialAccount.DoesNotExist:
        return Response(
            {'error': 'No connected Facebook account found'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    access_token = social_account.access_token
    
    # Prepare post content
    message = post.caption
    
    # Post to Facebook
    url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/me/feed"
    
    data = {
        'message': message,
        'access_token': access_token,
    }
    
    # If post has an image, upload it first
    if post.image:
        # Upload image to Facebook
        photo_url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/me/photos"
        
        with open(post.image.path, 'rb') as image_file:
            files = {'source': image_file}
            photo_data = {
                'access_token': access_token,
                'published': 'false',  # Don't publish yet, just upload
            }
            
            photo_response = requests.post(photo_url, data=photo_data, files=files)
            photo_result = photo_response.json()
            
            if 'id' in photo_result:
                data['attached_media'] = [{'media_fbid': photo_result['id']}]
    
    # Post to feed
    response = requests.post(url, data=data)
    result = response.json()
    
    if 'id' in result:
        # Update post status to published
        post.status = 'posted'
        post.save()
        
        return Response({
            'message': 'Post shared to Facebook successfully',
            'facebook_post_id': result['id'],
            'post_id': post.id
        })
    else:
        return Response(
            {'error': 'Failed to share post to Facebook', 'details': result},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facebook_status(request):
    """Check Facebook connection status"""
    try:
        social_account = SocialAccount.objects.get(
            user=request.user,
            platform='facebook',
            is_connected=True
        )
        return Response({
            'is_connected': True,
            'account_name': social_account.account_name,
            'account_id': social_account.account_id,
        })
    except SocialAccount.DoesNotExist:
        return Response({
            'is_connected': False,
        })
