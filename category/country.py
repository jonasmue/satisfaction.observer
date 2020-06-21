class Country:
    def __init__(self, name: str, locale: str):
        """
        A country represented by:
        :param name: Its name
        :param locale: The locale conforming to ISO-3166, e.g. de-DE
        """
        self.name = name
        self.locale = locale
