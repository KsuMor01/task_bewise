import pandas as pd

non_str = 'не указано'


def add_name(dlg: pd.DataFrame, json, label):
    name = dlg[label].unique()
    name = [_ for _ in name if type(_) == str]

    if name:
        json[label] = name[0]
        if label == 'manager':
            json['intro_replica'] = \
                dlg[dlg[label] == json[label]].text.values[0]
    else:
        json[label] = non_str
        if label == 'manager':
            json['intro_replica'] = non_str


def form_dialog_info(features: pd.DataFrame) -> list:
    dialog_info = []

    for dialog_id in features.dlg_id.unique():
        output_json = dict()
        output_json["dlg_id"] = dialog_id

        current_dialog = features[features.dlg_id == dialog_id]

        add_name(current_dialog, output_json, 'manager')
        add_name(current_dialog, output_json, 'company')

        outro = current_dialog[current_dialog.outro == True].text.values

        if outro.any():
            output_json['outro'] = outro[-1]
        else:
            output_json['outro'] = non_str

        intro = current_dialog[current_dialog.intro == True].text.values

        if intro:
            output_json['intro'] = intro[0]
        else:
            output_json['intro'] = non_str

        if output_json['intro'] != non_str and output_json['outro'] != non_str:
            output_json['condition'] = 'выполняется'
        else:
            output_json['condition'] = 'не выполняется'

        dialog_info.append(output_json)

    return dialog_info
