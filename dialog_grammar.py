from yargy import Parser, or_
from yargy.interpretation import fact
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline

import json

Dialog = fact(
    'Dialog',
    ['intro', 'outro'],
)
INTRO = morph_pipeline([
    'здравствуйте',
    'добрый день'
])

OUTRO = morph_pipeline([
    'до свидания',
    'пакеда'
])

gnc = gnc_relation()
DIALOG = or_(
    INTRO.interpretation(
        Dialog.intro
    ),
    OUTRO.interpretation(
        Dialog.outro
    )
).interpretation(
    Dialog
)

DEBUG = or_(
    INTRO,
    OUTRO
)


def join_spans(text, spans):
    spans = sorted(spans)
    return ' '.join(
        text[start:stop]
        for start, stop in spans
    )


def show_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def parse_dialog_line(line: str) -> dict:

    matches = Parser(DEBUG).findall(line)
    spans = [_.span for _ in matches]
    parsed_line = join_spans(line, spans)
    matches = Parser(DIALOG).findall(parsed_line)
    matches = sorted(matches, key=lambda _: _.span)

    dialog_info = {}
    if matches:
        dialog_info = dict(matches[0].fact.as_json)

    return dialog_info
