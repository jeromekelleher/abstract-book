"""
Process abstracts to create book.
"""
import csv
import sys
import textwrap
import dataclasses
from typing import List

import markdown_strings


def md_esc(s):
    return markdown_strings.esc_format(s)


@dataclasses.dataclass
class Abstract:
    author: str
    coauthors: str
    title: str
    text: str
    is_talk: bool
    keywords: str
    topics: str

    def as_markdown(self, out):
        print(f"# {md_esc(self.title)}", file=out)
        authors = md_esc(self.author)
        if len(self.coauthors) > 0:
            authors += f", {md_esc(self.coauthors)}"
        print(f"**Authors:** {authors}", file=out)
        print(file=out)
        keywords = md_esc(self.keywords)
        print(f"**Keywords:** {keywords}", file=out)
        print(file=out)
        topics = md_esc(self.topics)
        print(f"**Topics:** {topics}", file=out)
        print(file=out)
        text = textwrap.fill(md_esc(self.text))
        print(text, file=out)
        print(file=out)


class AbstractBook:
    def __init__(self, abstracts):
        self.abstracts = abstracts

    def as_markdown(self, out):
        for abstract in self.abstracts:
            abstract.as_markdown(out)


def main():

    infile = sys.argv[1]
    abstracts = []
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            # print(list(line.keys()))
            abstract = Abstract(
                author=line["Presenter name"],
                coauthors=line["Coauthors"],
                title=line["Title"],
                text=line["Abstract (max 1500 characters)"],
                is_talk=line["Talk or Poster?"] == "Talk",
                keywords=line["Keywords"],
                topics=line["Topics (select all that apply)"],
            )
            abstracts.append(abstract)

    talks = [ab for ab in abstracts if ab.is_talk]
    # print(len(talks))
    book = AbstractBook(talks)
    book.as_markdown(sys.stdout)


if __name__ == "__main__":
    main()
