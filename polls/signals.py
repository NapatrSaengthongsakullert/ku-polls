import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils.timezone import now

logger = logging.getLogger('polls')

def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username} at {now()} from IP {get_client_ip(request)}")

@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    if user is not None:
        logger.info(f"User logged out: {user.username} at {now()} from IP {get_client_ip(request)}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    logger.warning(f"Failed login attempt with username: {credentials.get('username')} at {now()} from IP {get_client_ip(request)}")