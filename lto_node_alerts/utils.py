import locale


def get_number_formatted(number):
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    return locale.format_string("%d", number, grouping=True)
