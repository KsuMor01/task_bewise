import pandas as pd
from dialog_grammar import parse_dialog_line


def get_info(dialog: pd.DataFrame) -> pd.DataFrame:
    info = pd.DataFrame(columns=['intro', 'outro'])

    features = dialog.join(info, how="outer")

    for i, line in enumerate(dialog.text):
        line_info = parse_dialog_line(line)
        if line_info:
            features.loc[i] = line_info

    return features
