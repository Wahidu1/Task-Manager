import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Initialize logger
logger = logging.getLogger(__name__)

def activation_send_html_email(user, current_site):
    try:
        # Email details
        to_email = user.email
        first_name = user.first_name
        last_name = user.last_name

        subject = "Activate Your Account"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [to_email]

        # Prepare context for the email template
        context = {
            "first_name": first_name,
            "last_name": last_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # Ensure 'uid' is properly encoded
            "user_id": user.pk,  # Change 'uid' to 'user_id' to avoid key conflict
            'token': default_token_generator.make_token(user),
        }

        # Render HTML content using the template
        html_content = render_to_string("utils/welcome_email.html", context)

        # Create and send email
        email = EmailMessage(subject, html_content, from_email, recipient_list)
        email.content_subtype = "html"  # Specify that the email content is HTML
        email.send()

        logger.info(f"Welcome email sent successfully to {to_email}")
        print("Welcome email sent successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
        return False
