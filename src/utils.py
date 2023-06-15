import re


class CsvCleaner:
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def _str(x):
        if str(x) == "nan":
            return None
        if str(x) == "":
            return None
        if str(x) == "None":
            return None
        else:
            return str(x)        

    def stringify(self, x):
        return self._str(x)

    def inline_quote_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        x = sorted(set([y for x_ in x for y in x_.split(" / ")]))
        return x

    def inline_quote_splitter_noslash(self, x):
        x = self._str(x)
        if x is None:
            return None
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        return x

    def inline_comma_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(",")

    def inline_comma_splitter_space(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(", ")

    def inline_semicolon_splitter(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split(";")

    def inline_semicolon_splitter_space(self, x):
        x = self._str(x)
        if x is None:
            return None
        return x.split("; ")

    def inline_comma_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        x = self._str(x)
        if x is None:
            return None
        else:
            elements = re.split(r",(?!\s)", x)
            if elements is None:
                return None
            else:
                # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements

    def inline_semicolon_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        x = self._str(x)
        if x is None:
            return None
        else:
            elements = re.split(r";(?!\s)", x)
            if elements is None:
                return None
            else:
                # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements
