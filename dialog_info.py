import pandas as pd

def form_dialog_info(features: pd.DataFrame) -> list:
    dialog_info = []

    for dialog_id in features.dlg_id.unique():

        output_json = {}
        output_json["dlg_id"] = dialog_id

        current_dialog = features[features.dlg_id == dialog_id]

        manager_name = current_dialog.manager.unique()
        manager_name = [name for name in manager_name if type(name) == str]

        non_str = 'не указано'

        if manager_name:
            output_json['manager_name'] = manager_name[0]
            output_json['intro_replica'] = \
                current_dialog[current_dialog.manager == output_json['manager_name']].text.values[-1]
        else:
            output_json['manager_name'] = non_str
            output_json['intro_replica'] = non_str

        company_name = current_dialog.company.unique()
        company_name = [name for name in company_name if type(name) == str]

        if company_name:
            output_json['company_name'] = company_name[0]
        else:
            output_json['company_name'] = non_str

        outro = current_dialog[current_dialog.outro == True].text.values
        print(outro)

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
