import re
from itertools import product
from dateutil.parser import parse
from collections import defaultdict, Counter

COMMON_SPECIFIERS = [
    '%a', '%A', '%d', '%b', '%B', '%m',
    '%Y', '%H', '%p', '%M', '%S', '%Z',
]


class FormatFinder:
    def __init__(self,
                 valid_specifiers=COMMON_SPECIFIERS,
                 date_element=r'([\w]+)',
                 delimiter_element=r'([\W]+)',
                 ignore_case=False):
        self.specifiers = valid_specifiers
        joined = (r'' + date_element + r"|" + delimiter_element)
        self.pattern = re.compile(joined)
        self.ignore_case = ignore_case

    def find_candidate_patterns(self, date_string):
        date = parse(date_string)
        tokens = self.pattern.findall(date_string)

        candidate_specifiers = defaultdict(list)

        for specifier in self.specifiers:
            token = date.strftime(specifier)
            candidate_specifiers[token].append(specifier)
            if self.ignore_case:
                candidate_specifiers[token.
                                     upper()] = candidate_specifiers[token]
                candidate_specifiers[token.
                                     lower()] = candidate_specifiers[token]

        options_for_each_element = []
        for (token, delimiter) in tokens:
            if token:
                if token not in candidate_specifiers:
                    options_for_each_element.append(
                        [token])  # just use this verbatim?
                else:
                    options_for_each_element.append(
                        candidate_specifiers[token])
            else:
                options_for_each_element.append([delimiter])

        for parts in product(*options_for_each_element):
            counts = Counter(parts)
            max_count = max(counts[specifier] for specifier in self.specifiers)
            if max_count > 1:
                # this is a candidate with the same item used more than once
                continue
            yield "".join(parts)


if __name__ == '__main__':
    import unittest

    class Test(unittest.TestCase):
        def test_it_returns_value_from_question_1(self):
            s = "2014-01-01 00:12:12"
            candidates = FormatFinder().find_candidate_patterns(s)
            sut = FormatFinder()
            candidates = sut.find_candidate_patterns(s)
            assert "%Y-%m-%d %H:%M:%S" in candidates

        def test_it_returns_value_from_question_2(self):
            s = 'Jan. 04, 2017'
            sut = FormatFinder()
            candidates = sut.find_candidate_patterns(s)
            candidates = list(candidates)
            assert "%b. %d, %Y" in candidates
            assert len(candidates) == 1

        def test_it_can_ignore_case(self):
            # NB: apparently the 'AM/PM' is mean to be capitalised in my locale! 
            # News to me!
            s = "JANUARY 12, 2018 02:12 am"
            sut = FormatFinder(ignore_case=True)
            candidates = sut.find_candidate_patterns(s)
            assert "%B %d, %Y %H:%M %p" in candidates

        def test_it_returns_parts_that_have_no_date_component_verbatim(self):
            # In this string, the 'at' is considered as a 'date' element, 
            # but there is no specifier that produces a candidate for it
            s = "January 12, 2018 at 02:12 AM"
            sut = FormatFinder()
            candidates = sut.find_candidate_patterns(s)
            assert "%B %d, %Y at %H:%M %p" in candidates

    unittest.main()
