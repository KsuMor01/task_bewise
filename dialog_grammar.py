from yargy import Parser, or_, rule, and_, not_
from yargy.interpretation import fact
from yargy.predicates import gram
from yargy.pipelines import morph_pipeline

Dialog = fact(
    'Dialog',
    ['intro', 'manager', 'company', 'outro'],
)
INTRO = morph_pipeline([
    "здравствуйте",
    "добрый день",
    "добрый вечер",
    "доброе утро",
    "приветствую",
    "доброго времени суток"
])

OUTRO = morph_pipeline([
    "до свидания",
    "всего доброго",
    "всего хорошего",
    "прощайте"
])

Name = fact(
    'Name',
    ['first', 'last'],
)

Manager = fact(
    'Manager',
    ['prefix', 'name']
)

LAST = and_(
    gram('Surn'),
    not_(gram('Abbr')),
)

FIRST = and_(
    gram('Name'),
    not_(gram('Abbr')),
)

PREFIX = morph_pipeline([
    "меня зовут",
    "меня звать",
    "мое имя",
    "моё имя",
    "меня",
    "это"
])

NAME = or_(
    FIRST.interpretation(
        Name.first.custom(str.capitalize)
    ),
    LAST.interpretation(
        Name.last.custom(str.capitalize)
    )
).interpretation(
    Name
)

MANAGER = rule(
    PREFIX.interpretation(
        Manager.prefix
    ),
    NAME.interpretation(
        Manager.name
    )
).interpretation(
    Manager
)

Company = fact(
    'Company',
    ['orgform', 'abbr', 'orgprefix', 'orgname'])

ORGFORM = morph_pipeline([
    "компания",
    "организация",
    "предприятие",
    "фирма",
    "холдинг"
]).interpretation(
    Company.orgform.normalized()
)

ABBR = morph_pipeline([
    "ООО",
    "ИП",
    "ЗАО",
    "ПАО"

]).interpretation(
    Company.abbr
)

ORGNAME = (gram('NOUN')).interpretation(
    Company.orgname.custom(str.capitalize))
ORG_PREFIX = or_(
    gram('ADJF'),
    gram('ADJS')
).interpretation(Company.orgprefix.custom(str.capitalize))

COMPANY = or_(
    rule(ORGFORM, ORG_PREFIX, ORGNAME),
    rule(ABBR, ORG_PREFIX, ORGNAME),
    rule(ABBR, ORGNAME),
    rule(ORGFORM, ORGNAME)

).interpretation(
    Company
)

DIALOG = or_(
    INTRO.interpretation(
        Dialog.intro
    ),
    MANAGER.interpretation(
        Dialog.manager
    ),
    COMPANY.interpretation(
        Dialog.company
    ),
    OUTRO.interpretation(
        Dialog.outro
    )
).interpretation(
    Dialog
)

DEBUG = or_(
    INTRO,
    MANAGER,
    COMPANY,
    OUTRO
)


def join_spans(text, spans):
    spans = sorted(spans)
    return ' '.join(
        text[start:stop]
        for start, stop in spans
    )


def parse_dialog_line(line: str) -> list:
    matches = Parser(DEBUG).findall(line)
    spans = [_.span for _ in matches]

    parsed_line = join_spans(line, spans)
    matches = Parser(DIALOG).findall(parsed_line)
    matches = sorted(matches, key=lambda _: _.span)

    dialog_info = []
    if matches:
        dialog_info.append([match.fact.as_json for match in matches])

    return dialog_info
