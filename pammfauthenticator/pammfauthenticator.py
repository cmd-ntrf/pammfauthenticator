import pamela

from jupyterhub.auth import PAMAuthenticator
from jupyterhub.handlers.login import LoginHandler
from tornado.concurrent import run_on_executor
from tornado.escape import url_escape
from tornado.httputil import url_concat

class PAMMFALoginHandler(LoginHandler):
    def _render(self, login_error=None, username=None):
        return self.render_template(
            'login_otp.html',
            next=url_escape(self.get_argument('next', default='')),
            username=username,
            login_error=login_error,
            custom_html=self.authenticator.custom_html,
            login_url=self.settings['login_url'],
            authenticator_login_url=url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {'next': self.get_argument('next', '')},
            ),
        )

class PAMMFAuthenticator(PAMAuthenticator):
    @run_on_executor
    def authenticate(self, handler, data):
        """Authenticate with PAM, and return the username if login is successful.

        Return None otherwise.
        """
        username = data['username']
        password = data['password']
        if 'otp' in data:
            password = [password, data['otp']]
        data = {'username' : username, 'password' : password}
        return super().authenticate(handler, data)

    def get_handlers(self, app):
        return [('/login', PAMMFALoginHandler),]
