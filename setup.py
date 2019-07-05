from setuptools import setup

setup(
    name='jupyterhub-pammfauthenticator',
    version='1.0.0',
    description='PAM Multifactor Authenticator for JupyterHub',
    url='https://github.com/cmd-ntrf/pammfauthenticator',
    author='Félix-Antoine Fortin',
    author_email='felix-antoine.fortin@calculquebec.ca',
    license='MIT',
    packages=['pammfauthenticator'],
    data_files=[
        ('share/jupyterhub/templates', ('share/jupyterhub/templates/login_otp.html',))
    ],
    install_requires=[
        'jupyterhub >= 1.0.0',
        'pamela',
        'tornado'
    ],
    entry_points={
        'jupyterhub.authenticators': [
            'pammfauthenticator = pammfauthenticator:PAMMFAuthenticator',
        ],
    },
)