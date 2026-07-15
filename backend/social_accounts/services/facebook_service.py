import requests
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, dumps, loads

from accounts.models import User
from social_accounts.models import SocialAccount

FACEBOOK_OAUTH_URL = "https://www.facebook.com/{}/dialog/oauth".format(
    settings.FACEBOOK_GRAPH_API_VERSION
)
FACEBOOK_ACCESS_TOKEN_URL = (
    "https://graph.facebook.com/{}/oauth/access_token".format(
        settings.FACEBOOK_GRAPH_API_VERSION
    )
)
FACEBOOK_USER_URL = "https://graph.facebook.com/{}/me".format(
    settings.FACEBOOK_GRAPH_API_VERSION
)
FACEBOOK_PAGES_URL = "https://graph.facebook.com/{}/me/accounts".format(
    settings.FACEBOOK_GRAPH_API_VERSION
)
FACEBOOK_SCOPES = [
    "public_profile",
    "email",
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_posts",
    "pages_manage_metadata",
]


def facebook_settings_configured():
    return bool(settings.FACEBOOK_APP_ID and settings.FACEBOOK_APP_SECRET)


def build_state(action="connect", user=None, platform="facebook"):
    payload = {"action": action, "platform": platform}
    if user is not None and getattr(user, "pk", None) is not None:
        payload["user_id"] = user.pk
    return dumps(payload)


def parse_state(state):
    if not state:
        return None
    try:
        return loads(state)
    except (BadSignature, SignatureExpired):
        return None


def get_facebook_login_url(user=None):
    state_value = None
    if user is not None and user.is_authenticated:
        state_value = build_state(action="connect", user=user)

    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "scope": ",".join(FACEBOOK_SCOPES),
        "response_type": "code",
        "auth_type": "reauthenticate",
    }
    if state_value:
        params["state"] = state_value

    return f"{FACEBOOK_OAUTH_URL}?{requests.compat.urlencode(params)}"


def build_facebook_oauth_url(state=None):
    base_url = FACEBOOK_OAUTH_URL
    params = {
        "client_id": settings.FACEBOOK_APP_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "scope": ",".join(FACEBOOK_SCOPES),
        "response_type": "code",
        "auth_type": "reauthenticate",
    }
    if state:
        params["state"] = state
    return f"{base_url}?{requests.compat.urlencode(params)}"


def exchange_code_for_token(code):
    response = requests.get(
        FACEBOOK_ACCESS_TOKEN_URL,
        params={
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
            "code": code,
        },
    )

    response.raise_for_status()
    data = response.json()
    return data.get("access_token")


def get_facebook_user_info(access_token):
    response = requests.get(
        FACEBOOK_USER_URL,
        params={
            "access_token": access_token,
            "fields": "id,name,email",
        },
    )
    response.raise_for_status()
    return response.json()


def get_facebook_pages(access_token):
    response = requests.get(
        FACEBOOK_PAGES_URL,
        params={"access_token": access_token},
    )
    response.raise_for_status()
    return response.json()


def get_or_create_facebook_social_account(user, access_token, user_info=None, pages_data=None):
    page_access_token = None
    page_id = None
    page_name = None

    if pages_data and isinstance(pages_data, dict):
        data_list = pages_data.get("data") or []
        if data_list:
            first_page = data_list[0]
            page_access_token = first_page.get("access_token")
            page_id = first_page.get("id")
            page_name = first_page.get("name")

    account_name = page_name or (user_info or {}).get("name") or "Facebook"
    account_id = page_id or (user_info or {}).get("id")

    defaults = {
        "account_name": account_name,
        "account_id": account_id,
        "access_token": access_token,
        "page_access_token": page_access_token,
        "page_id": page_id,
        "page_name": page_name,
        "is_connected": True,
    }

    social_account, _ = SocialAccount.objects.update_or_create(
        user=user,
        platform="facebook",
        defaults=defaults,
    )
    return social_account



def publish_post_to_facebook(post, social_account=None):
    if not social_account:
        social_account = SocialAccount.objects.filter(
            user=post.user,
            platform="facebook",
            is_connected=True,
        ).first()

    if not social_account:
        return {"success": False, "error": "No connected Facebook account found."}

    # Facebook deprecated publish_actions permission and /me/feed endpoint
    # We must use page access tokens to post to Facebook Pages
    access_token = social_account.page_access_token
    target_id = social_account.page_id
    
    # Posting to user timeline is no longer supported (publish_actions deprecated)
    # Only allow posting to Facebook Pages
    if not access_token or not target_id:
        return {
            "success": False,
            "error": "Facebook Page access token is missing. Please connect a Facebook Page with proper permissions (pages_manage_posts). User timeline posting is no longer supported.",
        }

    message = post.caption or post.title or ""

    if post.image:
        # Use the newer /photos endpoint for pages
        url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/{target_id}/photos"
        with open(post.image.path, "rb") as image_file:
            files = {"source": image_file}
            payload = {
                "access_token": access_token,
                "caption": message,
                "published": "true",
            }
            response = requests.post(url, data=payload, files=files)
    else:
        # Use the newer /feed endpoint with proper formatting
        url = f"https://graph.facebook.com/{settings.FACEBOOK_GRAPH_API_VERSION}/{target_id}/feed"
        payload = {
            "access_token": access_token,
            "message": message,
        }
        response = requests.post(url, data=payload)

    try:
        result = response.json()

    except ValueError:
        return {
            "success": False,
            "error": "Failed to parse Facebook response.",
            "details": response.text,
        }

    if response.status_code in (200, 201) and "id" in result:
        return {
            "success": True,
            "platform": "facebook",
            "provider_post_id": result["id"],
            "details": result,
        }

    return {
        "success": False,
        "error": result.get("error", {}).get("message", "Failed to share post to Facebook."),
        "details": result,
    }


def get_facebook_pages_for_user(user):
    social_account = SocialAccount.objects.filter(
        user=user,
        platform="facebook",
        is_connected=True,
    ).first()
    if not social_account:
        return None

    access_token = social_account.access_token
    if not access_token:
        return None

    return get_facebook_pages(access_token)
