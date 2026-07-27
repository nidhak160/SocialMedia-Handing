from django.shortcuts import render
from django.http import HttpResponse


def privacy_policy(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Privacy Policy - Social Media Handler</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6;">
        <h1>Privacy Policy</h1>
        <p>Last updated: July 2026</p>

        <h2>1. Information We Collect</h2>
        <p>When you use Social Media Handler, we collect:</p>
        <ul>
            <li>Your email address and basic profile information when you register</li>
            <li>OAuth access tokens for social media accounts you connect (Facebook, Instagram, LinkedIn)</li>
            <li>Content you create (post captions, images) for the purpose of publishing to your connected accounts</li>
        </ul>

        <h2>2. How We Use Your Information</h2>
        <p>We use the information solely to:</p>
        <ul>
            <li>Authenticate you and manage your account</li>
            <li>Publish content to social media accounts you have explicitly connected and authorized</li>
            <li>Display your connected accounts and post history within the platform</li>
        </ul>

        <h2>3. Data Storage</h2>
        <p>Access tokens are stored securely and are only used to make API calls on your behalf, at your request.
        We do not sell or share your data with third parties.</p>

        <h2>4. Data Deletion</h2>
        <p>You can request deletion of your data at any time. See our
        <a href="/data-deletion/">Data Deletion Instructions</a> page.</p>

        <h2>5. Contact</h2>
        <p>For privacy questions, contact: nidhak160@gmail.com</p>
    </body>
    </html>
    """
    return HttpResponse(html)


def terms_of_service(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Terms of Service - Social Media Handler</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6;">
        <h1>Terms of Service</h1>
        <p>Last updated: July 2026</p>

        <h2>1. Acceptance of Terms</h2>
        <p>By using Social Media Handler, you agree to these terms.</p>

        <h2>2. Use of the Service</h2>
        <p>You may use this platform to connect your own social media accounts and publish content you own or
        have rights to. You are responsible for all content published through your connected accounts.</p>

        <h2>3. Account Responsibility</h2>
        <p>You are responsible for maintaining the confidentiality of your account credentials.</p>

        <h2>4. Prohibited Use</h2>
        <p>You may not use this service to publish illegal, abusive, or platform-policy-violating content.</p>

        <h2>5. Termination</h2>
        <p>We reserve the right to suspend accounts that violate these terms or applicable platform policies
        (e.g., Meta Platform Terms).</p>

        <h2>6. Contact</h2>
        <p>Questions: nidhak160@gmail.com</p>
    </body>
    </html>
    """
    return HttpResponse(html)


def data_deletion(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Data Deletion Instructions - Social Media Handler</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; line-height: 1.6;">
        <h1>Data Deletion Instructions</h1>

        <p>If you would like your data deleted from Social Media Handler, including any connected
        social media account tokens and post history, please email us at:</p>

        <p><strong>nidhak160@gmail.com</strong></p>

        <p>Include the email address associated with your account. We will process your deletion
        request within 30 days and confirm once complete.</p>

        <p>Alternatively, you can disconnect any individual social media account directly from your
        dashboard at any time, which immediately revokes our access to that account.</p>
    </body>
    </html>
    """
    return HttpResponse(html)