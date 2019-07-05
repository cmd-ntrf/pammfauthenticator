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
        passwords = [data['password']]
        if 'otp' in data:
            passwords.append(data['otp'])
        try:
            pamela.authenticate(
                username, passwords, service=self.service, encoding=self.encoding
            )
        except pamela.PAMError as e:
            if handler is not None:
                self.log.warning(
                    "PAM Authentication failed (%s@%s): %s",
                    username,
                    handler.request.remote_ip,
                    e,
                )
            else:
                self.log.warning("PAM Authentication failed: %s", e)
            return None

        if self.check_account:
            try:
                pamela.check_account(
                    username, service=self.service, encoding=self.encoding
                )
            except pamela.PAMError as e:
                if handler is not None:
                    self.log.warning(
                        "PAM Account Check failed (%s@%s): %s",
                        username,
                        handler.request.remote_ip,
                        e,
                    )
                else:
                    self.log.warning("PAM Account Check failed: %s", e)
                return None

        return username

    def get_handlers(self, app):
        return [('/login', PAMMFALoginHandler),]