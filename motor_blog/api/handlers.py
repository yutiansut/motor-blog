"""Implementation of metaWeblog XML-RPC interface. Only enough to make MarsEdit
   work.

   See http://xmlrpc.scripting.com/metaWeblogApi.html

   Based heavily on http://www.allyourpixel.com/post/metaweblog-38-django/
"""

import xmlrpc.client as xmlrpclib

from motor_blog.api import categories, media, posts, tags, users
from motor_blog.api.rsd import RSDHandler
from tornadorpc.xml import XMLRPCHandler, XMLRPCParser

__all__ = ('APIHandler', 'RSDHandler')


class WordpressParser(XMLRPCParser):
    """Special parsing.

    Dispatches names like 'wp.getRecentPosts' to wp_getRecentPosts().
    """

    def parse_request(self, request_body):
        result = super(WordpressParser, self).parse_request(request_body)
        if isinstance(result, xmlrpclib.Fault):
            raise result
        else:
            ((method_name, params),) = result
            return ((method_name.replace('.', '_'), params),)


class APIHandler(
        XMLRPCHandler, categories.Categories, posts.Posts, tags.Tags,
        media.Media, users.Users):
    _RPC_ = WordpressParser(xmlrpclib)

    def mt_supportedTextFilters(self):
        # TODO, someday: read MarsEdit's incoming mt_textFilter and handle it
        # on new and edited posts
        return [
            {'key': 'markdown', 'label': 'Markdown'},
            #            {'key': 'htmlauto', 'label': "Convert line breaks" },
        ]
