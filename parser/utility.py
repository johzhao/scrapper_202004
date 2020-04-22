# noinspection PyProtectedMember
from lxml.etree import _Element


def get_element_str(html: _Element) -> str:
    result = []
    if html.text:
        result.append(html.text)

    for child in html.getchildren():
        if child.text:
            result.append(child.text)

        if child.tail:
            result.append(child.tail)

    if html.tail:
        result.append(html.tail)

    return ''.join(result).strip()
