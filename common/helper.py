
def lightbool(thing):
    if thing:
        return 'ON'
    return "OFF"


def codeblock(s):
    return '```\n' + s + '```'


def convert_to_table(dictionary, headers=None):
    strout = ''

    if headers:
        strout = "{:<20} | {:<35}\n".format(headers[0], headers[1])

    strout += '-' * 40 + '\n'
    for k, v in dictionary.items():
        strout += "{:<20} | {:<35}\n".format(k, v)

    return strout
