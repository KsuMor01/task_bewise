import pandas as pd
from dialog_grammar import parse_dialog_line


def write_info(features, info, i):
    for k in info:
        features.loc[i, k] = info[k]


def concat_keys(cur_key, match):
    output = ''
    for k in match[cur_key]:
        if k in ['prefix']:
            continue
        key_list = list(match[cur_key].keys())

        if 'name' in key_list:
            output += concat_keys('name', match[cur_key])
        else:
            output += match[cur_key][k] + ' '
    return output


def get_info(features: pd.DataFrame) -> pd.DataFrame:
    for i, line in enumerate(features.text):
        line_info = parse_dialog_line(line)
        if line_info:
            info = {}
            for match in line_info[0]:
                cur_key = list(match.keys())[0]
                if cur_key == 'company':
                    company = concat_keys(cur_key, match)
                    info[cur_key] = company
                elif cur_key == 'manager':
                    manager = concat_keys(cur_key, match)
                    info[cur_key] = manager
                elif cur_key in ('intro', 'outro'):
                    info[cur_key] = True
            write_info(features, info, i)

    return features
