import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from posts.models import Post
from .models import SocialAccount
from .services.facebook_service import (
    facebook_settings_configured,
    get_facebook_login_url,
    parse_state,
    exchange_code_for_token,
    get_facebook_user_info,
    get_facebook_pages,
    get_or_create_facebook_social_account,
    publish_post_to_facebook,
)


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


@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_login(request):
    """Initiate Facebook OAuth login."""
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

    login_url = get_facebook_login_url(
        request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
    )
    return JsonResponse({'login_url': login_url})


@api_view(['GET'])
@permission_classes([AllowAny])
def facebook_callback(request):
    """Handle Facebook OAuth callback."""
    code = request.GET.get('code')
    error = request.GET.get('error')

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

    access_token = exchange_code_for_token(code)
    if not access_token:
        return render_popup_message('facebookAuthError', {
            'message': 'Failed to get access token from Facebook',
        })

    try:
        user_info = get_facebook_user_info(access_token)
    except Exception as exc:
        return render_popup_message('facebookAuthError', {
            'message': f'Failed to fetch Facebook user information: {str(exc)}',
        })

    facebook_id = user_info.get('id')
    email = user_info.get('email')
    name = user_info.get('name', '')

    if not facebook_id:
        return render_popup_message('facebookAuthError', {
            'message': 'Failed to get Facebook user information',
        })

    try:
        pages_data = get_facebook_pages(access_token)
    except Exception:
        pages_data = {}

    state = parse_state(request.GET.get('state'))
    user = None
    if state and state.get('user_id'):
        user = User.objects.filter(pk=state.get('user_id')).first()

    if not user:
        if not email:
            email = f"facebook_{facebook_id}@facebook.com"
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': name.replace(' ', '_').lower(),
                'is_verified': True,
            },
        )
        if created:
            user.set_password(User.objects.make_random_password())
            user.save()

    social_account = get_or_create_facebook_social_account(
        user=user,
        access_token=access_token,
        user_info=user_info,
        pages_data=pages_data,
    )

    refresh = RefreshToken.for_user(user)
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


def share_post_to_facebook_post(post):
    # Check if post has specific social accounts selected
    social_account = post.social_accounts.filter(
        platform="facebook",
        is_connected=True
    ).first()
    
    # If specific account is selected, use it; otherwise use default behavior
    if social_account:
        return publish_post_to_facebook(post, social_account)
    
    return publish_post_to_facebook(post)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_post_to_facebook(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    result = share_post_to_facebook_post(post)
    if result['success']:
        post.status = 'posted'
        post.save()
        return Response({
            'message': 'Post shared to Facebook successfully',
            'facebook_post_id': result['provider_post_id'],
            'post_id': post.id,
        })

    return Response(
        {'error': result.get('error', 'Failed to share post to Facebook'), 'details': result.get('details')},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facebook_status(request):
    try:
        social_account = SocialAccount.objects.get(
            user=request.user,
            platform='facebook',
            is_connected=True,
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
