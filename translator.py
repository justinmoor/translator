import argparse
from requests_html import HTMLSession
from prettytable import PrettyTable

available_langs = {
    "nl": "Dutch",
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portugese",
    "da": "Danish",
    "sv": "Swedish"
}

description = "Translate a word (vertalen.nu).\
                Available languages: \
                nl (Nederlands)\
                en (English)\
                fr (Français)\
                de (Deutsch)\
                es (Español)\
                it (Italiano)\
                pt (Português)\
                da (Dansk)\
                sv (Svenska)"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=description)

    parser.add_argument("word", type=str,
                        help="Word that needs to be translated.")

    parser.add_argument("source", type=str,
                        help="Soure language.")

    parser.add_argument("target", type=str,
                        help="Target language.")

    args = parser.parse_args()

    if args.source == args.target:
        print("\nCannot use source language as target language.\n")
        exit()

    if args.source not in available_langs.keys() or args.target not in available_langs.keys():
        print("\nLanguage not supported.\n")
        parser.print_help()
        exit()

    return args


def get_result(payload):
    session = HTMLSession()
    r = session.get("https://www.vertalen.nu/vertaal?", params=payload)

    synonyms = r.html.find(".result-item-source")
    translations = r.html.find(".result-item-target")

    if not translations:
        print("No translations found.")
        exit()

    return {"synonyms": [word.text for word in synonyms],
            "translations": [word.text for word in translations]}


def setup_table(result, src, target):
    table = PrettyTable()

    source_header = available_langs[src] + " (" + src + ")"
    target_header = available_langs[target] + " (" + target + ")"

    table.field_names = [source_header,
                         target_header]

    table.align[source_header] = "l"
    table.align[target_header] = "l"

    for i, r in enumerate(result["synonyms"]):
        table.add_row([r, result["translations"][i]])
        table.add_row(["\n", "\n"])

    return table


def main():
    args = parse_arguments()
    src = args.source
    target = args.target

    payload = {"vertaal": args.word, "van": src, "naar": target}
    result = get_result(payload)

    print()
    print(setup_table(result, src, target))
    print()


if __name__ == "__main__":
    main()
