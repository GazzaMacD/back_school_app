from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.urls import reverse


class CustomAccoutAdapter(DefaultAccountAdapter):
    """
    Overrides of the allauth DefaultAccountAdapter which give
    the behaviour required for allauth related tasks such as
    email confirmations after register etc.
    """

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        # set request to None so that site 1 url is used to construct the
        # url
        request = None
        ret = build_absolute_uri(request, url)
        return ret
