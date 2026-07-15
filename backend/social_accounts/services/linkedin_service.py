import requests
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.conf import settings

from social_accounts.models import SocialAccount

LINKEDIN_OAUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_ME_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_EMAIL_URL = (
    "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
)
LINKEDIN_SCOPES = ["r_liteprofile", "r_emailaddress", "w_member_social"]


def linkedin_settings_configured():
    return bool(
        settings.LINKEDIN_CLIENT_ID
        and settings.LINKEDIN_CLIENT_SECRET
        and settings.LINKEDIN_REDIRECT_URI
    )


def build_state(action="connect", user=None, platform="linkedin"):
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


def get_linkedin_login_url(user=None):
    state_value = None
    if user is not None and user.is_authenticated:
        state_value = build_state(action="connect", user=user)

    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": " ".join(LINKEDIN_SCOPES),
    }
    if state_value:
        params["state"] = state_value

    return f"{LINKEDIN_OAUTH_URL}?{requests.compat.urlencode(params)}"


def exchange_linkedin_code_for_token(code):
    response = requests.post(
        LINKEDIN_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json().get("access_token")


def get_linkedin_profile(access_token):
    response = requests.get(
        LINKEDIN_ME_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    profile = response.json()
    return {
        "id": profile.get("id"),
        "display_name": "{} {}".format(
            profile.get("localizedFirstName", ""),
            profile.get("localizedLastName", ""),
        ).strip(),
    }


def get_linkedin_email(access_token):
    response = requests.get(
        LINKEDIN_EMAIL_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    email_data = response.json().get("elements", [])
    if not email_data:
        return None
    return email_data[0].get("handle~", {}).get("emailAddress")


def get_or_create_linkedin_social_account(user, access_token, profile, email=None):
    account_name = profile.get("display_name") or "LinkedIn"
    account_id = profile.get("id")

    social_account, _ = SocialAccount.objects.update_or_create(
        user=user,
        platform="linkedin",
        defaults={
            "account_name": account_name,
            "account_id": account_id,
            "access_token": access_token,
            "is_connected": True,
        },
    )
    return social_account


def publish_post_to_linkedin(post):
    social_account = SocialAccount.objects.filter(
        user=post.user,
        platform="linkedin",
        is_connected=True,
    ).first()

    if not social_account:
        return {"success": False, "error": "No connected LinkedIn account found."}

    access_token = social_account.access_token
    author = f"urn:li:person:{social_account.account_id}"
    message = post.caption or post.title or "Shared via Social Media Platform"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": message},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=payload,
    )

    result = response.json()
    if response.status_code in (200, 201) and "serviceErrorCode" not in result:
        return {
            "success": True,
            "platform": "linkedin",
            "provider_post_id": result.get("id"),
            "details": result,
        }

    return {
        "success": False,
        "error": "Failed to share post to LinkedIn.",
        "details": result,
    }
