import json
import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SocialAccount
from accounts.models import User

LINKEDIN_OAUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_ME_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"

LINKEDIN_SCOPE = ["r_liteprofile", "r_emailaddress"]


def linkedin_settings_configured():
    return bool(settings.LINKEDIN_CLIENT_ID and settings.LINKEDIN_CLIENT_SECRET and settings.LINKEDIN_REDIRECT_URI)


def get_linkedin_login_url():
    state = "linkedin_connect"
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": " ".join(LINKEDIN_SCOPE),
        "state": state,
    }
    return f"{LINKEDIN_OAUTH_URL}?{requests.compat.urlencode(params)}"


def exchange_linkedin_code_for_token(code):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(LINKEDIN_TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")


def get_linkedin_profile(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(LINKEDIN_ME_URL, headers=headers)
    response.raise_for_status()
    profile = response.json()
    first_name = profile.get("localizedFirstName")
    last_name = profile.get("localizedLastName")
    return {
        "id": profile.get("id"),
        "first_name": first_name,
        "last_name": last_name,
        "display_name": f"{first_name} {last_name}".strip(),
    }


def get_linkedin_email(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(LINKEDIN_EMAIL_URL, headers=headers)
    response.raise_for_status()
    email_data = response.json().get("elements", [])
    if not email_data:
        return None
    return email_data[0].get("handle~", {}).get("emailAddress")


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

    social_account, account_created = SocialAccount.objects.get_or_create(
        user=user,
        platform='linkedin',
        defaults={
            'account_name': name,
            'account_id': linkedin_id,
            'access_token': access_token,
            'is_connected': True,
        }
    )

    if not account_created:
        social_account.access_token = access_token
        social_account.account_name = name
        social_account.account_id = linkedin_id
        social_account.is_connected = True
        social_account.save()

    refresh = RefreshToken.for_user(user)
    return render_popup_message('linkedinAuth', {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username,
    })
