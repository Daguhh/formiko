# -*- coding: utf-8 -*-
from gi.repository import Gtk, WebKit

from docutils.core import publish_string
from docutils.parsers.rst import Parser as RstParser
from docutils.writers.html4css1 import Writer as Writer4css1
from docutils.writers.s5_html import Writer as WriterS5
from docutils.writers.pep_html import Writer as WriterPep

try:
    from docutils_tinyhtml import Writer as TinyWriter
except:
    TinyWriter = None

try:
    from htmlwriter import Writer as HtmlWriter
except:
    HtmlWriter = None

try:
    from docutils_html5 import Writer as Html5Writer
except:
    Html5Writer = None

try:
    from remarkdown.parser import MarkdownParser
except:
    MarkdownParser = None

try:
    from recommonmark.parser import CommonMarkParser
except:
    CommonMarkParser = None

from io import StringIO
from traceback import print_exc

PARSERS = {
    'rst': {
        'key': 'rst',
        'title': 'Docutils reStructuredText Parser',
        'class': RstParser,
        'url': 'http://docutils.sourceforge.net',
        'extension': '.rst'},
    'remarkdown': {
        'key': 'remarkdown',
        'title': 'The remarkdown Parser',
        'class': MarkdownParser,
        'url': 'https://github.com/sgenoud/remarkdown',
        'extension': '.md'},
    'recommonmark': {
        'key': 'recommonmark',
        'title': 'Common Mark Parser',
        'class': CommonMarkParser,
        'url': 'https://github.com/rtfd/recommonmark',
        'extension': '.md'}
}

WRITERS = {
    'html4': {
        'key': 'html4',
        'title': 'Docutils html4 Writer',
        'class': Writer4css1,
        'url': 'http://docutils.sourceforge.net'},
    's5': {
        'key': 's5',
        'title': 'Docutils S5/HTML Slideshow Writer',
        'class': WriterS5,
        'url': 'http://docutils.sourceforge.net'},
    'pep': {
        'key': 'pep',
        'title': 'Docutils PEP HTML Writer',
        'class': WriterPep,
        'url': 'http://docutils.sourceforge.net'},
    'tiny': {
        'key': 'tiny',
        'title': 'Tiny HTML Writer',
        'class': TinyWriter,
        'url': 'https://github.com/ondratu/docutils-tinyhtmlwriter'},
    'html': {
        'key': 'html',
        'title': 'Yet another HTML Writer',
        'class': HtmlWriter,
        'url': 'https://github.com/masayuko/docutils-htmlwriter'},
    'html5': {
        'key': 'html5',
        'title': 'HTML 5 Writer',
        'class': Html5Writer,
        'url': 'https://github.com/Kozea/docutils-html5-writer'},
}

NOT_FOUND = """
<html>
  <head></head>
  <body>
    <h1>Commponent {title} Not Found!</h1>
    <p>Component <b>{title}</b> which you want to use is not found.
       See <a href="{url}">{url}</a> for mor details and install it
       to system.
    </p>
  </body>
</html>
"""

SCROLL = """
<script>
    window.scrollTo(
        0,
        (document.documentElement.scrollHeight-window.innerHeight)*%f)
</script>
"""


class Renderer(Gtk.ScrolledWindow):
    def __init__(self, win, parser='rst', writer='html4', style=''):
        super(Renderer, self).__init__()
        self.set_policy(Gtk.PolicyType.AUTOMATIC,
                        Gtk.PolicyType.AUTOMATIC)
        self.webview = WebKit.WebView()
        self.sb = self.get_vscrollbar()
        self.add(self.webview)
        self.set_writer(writer)
        self.set_parser(parser)
        self.style = style
        self.__win = win

    def set_writer(self, writer):
        assert writer in WRITERS
        self.__writer = WRITERS[writer]
        klass = self.__writer['class']
        self.writer_instance = klass() if klass is not None else None
        self.do_render()

    def get_writer(self):
        return self.__writer['key']

    def set_parser(self, parser):
        assert parser in PARSERS
        self.__parser = PARSERS[parser]
        klass = self.__parser['class']
        self.parser_instance = klass() if klass is not None else None
        self.do_render()

    def get_parser(self):
        return self.__parser['key']

    def set_style(self, style):
        self.style = style
        self.do_render()

    def get_style(self):
        return self.style

    def do_render(self):
        if getattr(self, 'src', None) is None:
            return
        try:
            if self.__parser['class'] is None:
                html = NOT_FOUND.format(**self.__parser)
                self.webview.load_string(html, "text/html", "UTF-8",
                                         "file:///")
            elif self.__writer['class'] is None:
                html = NOT_FOUND.format(**self.__writer)
                self.webview.load_string(html, "text/html", "UTF-8",
                                         "file:///")
            else:
                a, b = len(self.src[:self.pos]), len(self.src[self.pos:])
                position = (float(a)/(a+b)) if a or b else 0
                settings = {
                    'warning_stream': StringIO(),
                    'embed_stylesheet': True
                }
                if self.style:
                    settings['stylesheet'] = self.style
                    settings['stylesheet_path'] = []
                html = publish_string(
                    source=self.src,
                    parser=self.parser_instance,
                    writer=self.writer_instance,
                    writer_name='html',
                    settings_overrides=settings).decode('utf-8')
                html += SCROLL % position
                if not self.__win.runing:
                    return
                self.webview.load_string(html, "text/html", "UTF-8",
                                         "file:///")
        except:
            print_exc()
            # TODO: return error to user dialog and confirm sending error to
            # support email by http post request :-)

    def render(self, src, pos=0):
        self.src = src
        self.pos = pos
        self.do_render()
