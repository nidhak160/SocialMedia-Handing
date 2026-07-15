import json
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from posts.models import Post
from .services.linkedin_service import (
    linkedin_settings_configured,
    exchange_linkedin_code_for_token,
    get_linkedin_profile,
    get_linkedin_email,
    get_or_create_linkedin_social_account,
    publish_post_to_linkedin,
    parse_state,
)


def render_popup_message(message_type, payload):
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LinkedIn Login</title>
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
        <h1>LinkedIn Login</h1>
        <p>{payload.get('message', '')}</p>
    </body>
    </html>
    """
    return HttpResponse(html_response, content_type='text/html')


def share_post_to_linkedin_post(post):
    return publish_post_to_linkedin(post)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def share_post_to_linkedin(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    result = share_post_to_linkedin_post(post)
    if result['success']:
        post.status = 'posted'
        post.save()
        return Response({
            'message': 'Post shared to LinkedIn successfully',
            'linkedin_post_urn': result.get('provider_post_id'),
            'post_id': post.id,
        })

    return Response(
        {'error': result.get('error', 'Failed to share post to LinkedIn'), 'details': result.get('details')},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def linkedin_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return render_popup_message('linkedinAuthError', {
            'message': 'Access denied or cancelled',
            'error': error,
        })

    if not code:
        return render_popup_message('linkedinAuthError', {
            'message': 'No authorization code provided',
        })

    if not linkedin_settings_configured():
        return render_popup_message('linkedinAuthError', {
            'message': 'LinkedIn login is not configured',
        })

    try:
        access_token = exchange_linkedin_code_for_token(code)
    except Exception as exc:
        return render_popup_message('linkedinAuthError', {
            'message': f'Failed to exchange code for access token: {str(exc)}',
        })

    if not access_token:
        return render_popup_message('linkedinAuthError', {
            'message': 'Failed to get access token from LinkedIn',
        })

    try:
        profile = get_linkedin_profile(access_token)
        email = get_linkedin_email(access_token)
    except Exception as exc:
        return render_popup_message('linkedinAuthError', {
            'message': f'Failed to fetch LinkedIn profile: {str(exc)}',
        })

    linkedin_id = profile.get('id')
    name = profile.get('display_name') or f"LinkedIn {linkedin_id}"

    state = parse_state(request.GET.get('state'))
    user = None
    if state and state.get('user_id'):
        user = User.objects.filter(pk=state.get('user_id')).first()

    if not user:
        email = email or f"linkedin_{linkedin_id}@linkedin.com"
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': name.replace(' ', '_').lower(),
                'is_verified': True,
            }
        )
        if created:
            user.set_password(User.objects.make_random_password())
            user.save()

    get_or_create_linkedin_social_account(
        user=user,
        access_token=access_token,
        profile=profile,
    )

    refresh = RefreshToken.for_user(user)
    return render_popup_message('linkedinAuth', {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    })
