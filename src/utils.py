import re

class CsvCleaner:
    def __init__(self) -> None:
        super().__init__()

    def stringify(self, x):
        if str(x) == "nan":
            return None
        else:
            return str(x)

    def inline_quote_splitter(self, x):
        if str(x) == "nan":
            return None
        x = str(x)
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        x = sorted(set([y for x_ in x for y in x_.split(" / ")]))
        return x

    def inline_quote_splitter_noslash(self, x):
        if str(x) == "nan":
            return None
        x = str(x)
        x = [x_ for x_ in x.split('"') if len(x_) > 1]
        x = [x_.rstrip(",") for x_ in x]
        return x

    def inline_comma_splitter(self, x):
        if str(x) == "nan":
            return None
        return x.split(",")

    def inline_comma_splitter_space(self, x):
        if str(x) == "nan":
            return None
        return x.split(", ")

    def inline_semicolon_splitter(self, x):
        if x == None:
            return "nan"
        return x.split(";")

    def inline_semicolon_splitter_space(self, x):
        if str(x) == "nan":
            return None
        if x is None:
            return None
        return x.split("; ")

    def inline_comma_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        if str(x)== "nan":
            return None
        else:
            elements = re.split(r',(?!\s)', x)
            if elements is None:
                return None
            else:
            # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements
    
    def inline_semicolon_splitter_nospace(self, x):
        # Split the string based on commas not followed by a space
        if str(x)== "nan":
            return None
        else:
            elements = re.split(r';(?!\s)', x)
            if elements is None:
                return None
            else:
            # Remove leading and trailing whitespace from each element
                elements = [elem.strip() for elem in elements]
                return elements


