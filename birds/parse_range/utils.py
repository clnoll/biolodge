import os


def oneOfKeywords(iterable):
    return Or(imap(Keyword, iterable))


def oneOfKeywordsInFile(path):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        path)
    with open(path) as fp:
        lines = ifilter(None, imap(process_line, fp))
        return oneOfKeywords(lines)


def process_line(line):
    line = line.strip()
    line = line.decode('utf8')
    # Strip inline comments
    line = re.sub(r'\s*#.*', '', line)
    return line
