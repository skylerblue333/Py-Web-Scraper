from src.scraper import LinkParser

def test_link_parser_extracts_links():
    parser = LinkParser()
    parser.feed('<a href="https://example.com">link</a>')
    assert "https://example.com" in parser.links

def test_link_parser_title():
    parser = LinkParser()
    parser.feed("<title>Hello World</title>")
    assert parser.title == "Hello World"

def test_link_parser_ignores_relative():
    parser = LinkParser()
    parser.feed('<a href="/relative">link</a>')
    assert len(parser.links) == 0
