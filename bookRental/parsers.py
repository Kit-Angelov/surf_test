from rest_framework import parsers


class PlainTextParser(parsers.BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()
