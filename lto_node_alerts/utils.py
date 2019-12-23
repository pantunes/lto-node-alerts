import locale


def get_number_formatted(number):
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.format_string("%d", number, grouping=True)
