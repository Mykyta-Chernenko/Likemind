import re


def _string_type(self):
    name = self._meta.object_name
    words_from_capital = re.findall('[A-Z][^A-Z]*', name)
    return '-'.join([word.lower() for word in words_from_capital])