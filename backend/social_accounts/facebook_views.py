import json
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
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
    # For initial Facebook connection, request only valid basic login permissions.
    # Page publishing permissions require a separate app review process.
    scope = "public_profile,email"
    
    url = (
        f"https://www.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/dialog/oauth"
        f"?client_id={app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&auth_type=reauthenticate"
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

    def render_popup_message(message_type, payload):
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Facebook Login</title>
            <script>
                const data = {{
                    type: '{message_type}',
                    ...{json.dumps(payload)}
                }};

                if (window.opener) {{
                    window.opener.postMessage(data, '*');
                }}

                window.close();
            </script>
        </head>
        <body>
            <h1>Facebook Login</h1>
            <p>{payload.get('message', '')}</p>
        </body>
        </html>
        """
        return HttpResponse(html_response, content_type='text/html')

    if error:
        return render_popup_message('facebookAuthError', {
            'message': 'Access denied or cancelled',
            'error': error,
        })
    
    if not code:
        return render_popup_message('facebookAuthError', {
            'message': 'No authorization code provided',
        })

    if not facebook_settings_configured():
        return render_popup_message('facebookAuthError', {
            'message': 'Facebook login is not configured',
        })
    
    # Exchange code for access token
    access_token = exchange_code_for_token(code)
    
    if not access_token:
        return render_popup_message('facebookAuthError', {
            'message': 'Failed to get access token from Facebook',
        })
    
    # Get user info
    user_info = get_facebook_user_info(access_token)
    
    facebook_id = user_info.get('id')
    email = user_info.get('email')
    name = user_info.get('name', '')
    
    if not facebook_id:
        return render_popup_message('facebookAuthError', {
            'message': 'Failed to get Facebook user information',
        })

    # Get pages
    pages_data = get_facebook_pages(access_token)
    
    # If page access token is available, use the page token and page id
    page_access_token = None
    page_id = None
    page_name = None
    if pages_data.get('data'):
        first_page = pages_data['data'][0]
        page_access_token = first_page.get('access_token')
        page_id = first_page.get('id')
        page_name = first_page.get('name')

    if not email:
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
    account_name = page_name or name
    account_id = page_id or facebook_id
    access_token_to_store = page_access_token or access_token

    social_account, account_created = SocialAccount.objects.get_or_create(
        user=user,
        platform='facebook',
        defaults={
            'account_name': account_name,
            'account_id': account_id,
            'access_token': access_token_to_store,
            'is_connected': True,
        }
    )
    
    if not account_created:
        social_account.access_token = access_token_to_store
        social_account.account_name = account_name
        social_account.account_id = account_id
        social_account.is_connected = True
        social_account.save()
    
    # Generate JWT tokens for the user
    refresh = RefreshToken.for_user(user)
    
    # Return HTML with JavaScript to post tokens back to the opener and close the popup
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Login Success</title>
        <script>
            const data = {{
                type: 'facebookAuth',
                access: '{str(refresh.access_token)}',
                refresh: '{str(refresh)}',
                username: '{user.username}',
            }};

            if (window.opener) {{
                window.opener.postMessage(data, '*');
            }}

            window.close();
        </script>
    </head>
    <body>
        <h1>Login Successful!</h1>
        <p>You can close this window.</p>
    </body>
    </html>
    """
    
    return HttpResponse(html_response, content_type='text/html')


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

    if post.image:
        # Upload image directly to the connected Facebook Page
        photo_url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/{social_account.account_id}/photos"
        
        with open(post.image.path, 'rb') as image_file:
            files = {'source': image_file}
            photo_data = {
                'access_token': access_token,
                'message': message,
                'published': 'true',
            }
            
            photo_response = requests.post(photo_url, data=photo_data, files=files)
            result = photo_response.json()

            if 'error' in result:
                return Response(
                    {
                        'error': 'Failed to upload image to Facebook',
                        'details': result['error'],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
    else:
        # Publish a text-only post to the connected Facebook Page
        url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/{social_account.account_id}/feed"
        response = requests.post(url, data={
            'message': message,
            'access_token': access_token,
        })
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
