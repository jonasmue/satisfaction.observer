class Country:
    def __init__(self, name: str, locale: str, flag: str):
        """
        A country represented by:
        :param name: Its name
        :param locale: The locale conforming to ISO-3166, e.g. de-DE
        :param flag: Link to a flag (preferably an .svg)
        """
        self.name = name
        self.locale = locale
        self.flag = flag
