import feedparser

feed = feedparser.parse('http://feeds.feedburner.com/PythonInsider')


class Entry:
    def __init__(self, title, link, published, published_parsed, author):
        self.title = title
        self.link = link
        self.published = published
        self.published_parsed = published_parsed
        self.author = author

    def csv(self):
        return "{},{},{},{}".format(self.title, self.link, self.published, self.author)


def entry_exists(entry):
    found = False
    with open("rss\entries.csv", 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line.replace('\n', '') == entry.csv():
                found = True
                break
        file.close()
    return found


def save_entry(entry):
    with open("rss\entries.csv", 'a', encoding='utf-8') as file:
        file.write("{}\n".format(entry.csv()))
        file.close()


def get_new_entries():
    new_entries = []
    entries = feed.entries
    entries.reverse()
    for entry in entries:
        _entry = Entry(entry.title, entry.link, entry.published, entry.published_parsed, entry.author)
        if not entry_exists(_entry):
            save_entry(_entry)
            new_entries.append(_entry)
    return new_entries


def get_latest_entry():
    entry = None
    with open("rss\entries.csv", 'r', encoding='utf-8') as file:
        lines = file.readlines()
        entry = lines[len(lines)-1].replace('\n', '')
        file.close()
    return entry.split(",")

if __name__ == "__main__":
    print(get_new_entries())
    print(get_latest_entry())