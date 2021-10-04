from __future__ import absolute_import, division, print_function

# from ansible.plugins.httpapi import HttpApiBase

__metaclass__ = type

from io import BytesIO

from ansible.errors import AnsibleConnectionFailure

# pylint: disable-all
# pyright: reportMissingImports=false
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url


class Connection(object):
    """Network API connection"""

    transport = "ansible.netcommon.httpapi"
    has_pipelining = True

    def __init__(self, *args, **kwargs):
        self.hostvars = {}
        self._auth = None
        self.httpapi = None
        # HttpApiBase

    def get_option(self, option):
        if self.httpapi:
            return self.httpapi.get_option(option)

        return self.hostvars.get(option)

    def set_option(self, option, value):
        self.hostvars[option] = value

    @property
    def _url(self):
        protocol = "https" if self.get_option("use_ssl") else "http"
        host = self.get_option("host")
        port = self.get_option("port") or (443 if protocol == "https" else 80)
        return "%s://%s:%s" % (protocol, host, port)

    def send(self, path, data, **kwargs):
        """
        Sends the command to the device over api
        """
        url_kwargs = dict(
            timeout=self.get_option("persistent_command_timeout"),
            validate_certs=self.get_option("validate_certs"),
            use_proxy=self.get_option("use_proxy"),
            headers={},
        )
        url_kwargs.update(kwargs)
        if self._auth:
            # Avoid modifying passed-in headers
            headers = dict(kwargs.get("headers", {}))
            headers.update(self._auth)
            url_kwargs["headers"] = headers
        else:
            url_kwargs["force_basic_auth"] = True
            url_kwargs["url_username"] = self.get_option("remote_user")
            url_kwargs["url_password"] = self.get_option("password")

        try:
            url = self._url + path
            response = open_url(url, data=data, **url_kwargs)
        except HTTPError as exc:
            is_handled = self.httpapi.handle_httperror(exc)
            if is_handled is True:
                return self.send(path, data, **kwargs)
            elif is_handled is False:
                raise
            else:
                response = is_handled
        except URLError as exc:
            raise AnsibleConnectionFailure(
                "Could not connect to {0}: {1}".format(self._url + path, exc.reason)
            )

        response_buffer = BytesIO()
        resp_data = response.read()
        response_buffer.write(resp_data)

        # Try to assign a new auth token if one is given
        self._auth = self.httpapi.update_auth(response, response_buffer) or self._auth

        response_buffer.seek(0)

        return response, response_buffer

    def queue_message(self, level, message):
        print(f"level: {level} - {message}")
