# pammfauthenticator

Simple PAM Multifactor Authenticator Plugin for JupyterHub

## Installation

You can install it from pip with:

```
pip install https://www.github.com/cmd-ntrf/pammfauthenticator/archive/main.zip
```

## Usage

You can enable this authenticator with the following lines in your
`jupyter_config.py`:

```python
c.JupyterHub.authenticator_class = 'pammfauthenticator'
```

### Required configuration

* JupyterHub >= 4.0.0
* Pamela >= 1.1.0
