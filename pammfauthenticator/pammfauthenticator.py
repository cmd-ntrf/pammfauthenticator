from jinja2 import Template
from jupyterhub.auth import PAMAuthenticator
from jupyterhub.handlers.login import LoginHandler
from tornado.escape import url_escape
from tornado.httputil import url_concat

class PAMMFALoginHandler(LoginHandler):
    def _render(self, login_error=None, username=None):
        context = {
            "next": url_escape(self.get_argument('next', default='')),
            "username": username,
            "login_error": login_error,
            "login_url": self.settings['login_url'],
            "authenticator_login_url": url_concat(
                self.authenticator.login_url(self.hub.base_url),
                {
                    'next': self.get_argument('next', ''),
                },
            ),
            "xsrf": self.xsrf_token.decode('ascii'),
        }
        custom_html = Template(
            self.authenticator.get_custom_html(self.hub.base_url)
        ).render(**context)
        return self.render_template(
            'login_otp.html',
            **context,
            custom_html=custom_html,
        )

class PAMMFAuthenticator(PAMAuthenticator):
    def authenticate(self, handler, data):
        """Authenticate with PAM, and return the username if login is successful.

        Return None otherwise.
        """
        username = data['username']
        password = data['password']
        if data.get('otp'):
            password = [password, data['otp']]
        data = {'username' : username, 'password' : password}
        return super().authenticate(handler, data)

    def get_handlers(self, app):
        return [('/login', PAMMFALoginHandler),]
