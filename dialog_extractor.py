import pandas as pd
from dialog_grammar import parse_dialog_line


def get_info(dialog: pd.DataFrame) -> pd.DataFrame:
    info_columns = pd.DataFrame(columns=['intro', 'manager', 'company', 'outro'])

    features = dialog.join(info_columns, how="outer")

    for i, line in enumerate(dialog.text):
        line_info = parse_dialog_line(line)

        if line_info:
            info = {}
            for match in line_info[0]:
                cur_key = list(match.keys())[0]
                if cur_key == 'company':
                    company = ''
                    for k in match[cur_key]:
                        company += match[cur_key][k] + ' '
                    info[cur_key] = company
                elif cur_key == 'manager':
                    manager = ''
                    name_key = list(match[cur_key].keys())[1]
                    for k in match[cur_key][name_key]:
                        manager += match[cur_key][name_key][k] + ' '
                    info[cur_key] = manager
                elif cur_key == 'intro' or cur_key == 'outro':
                    info[cur_key] = True
            for k in info:
                features.loc[i, k] = info[k]

    return features
