"""
This is the main script
"""
import pandas as pd

import dialog_extractor

import dialog_info

df = pd.read_csv('test_data.csv')

print('Parsing dialogs...')

features = df[df['role'] == 'manager']
features = features.reset_index()

features = dialog_extractor.get_info(features)

output_list = dialog_info.form_dialog_info(features)


for output_dict in output_list:
    print(
        "Номер диалога: " + str(output_dict['dlg_id']),
        "Менеджер поздоровался: " + output_dict['intro'],
        "Менеджер представил себя: " + output_dict['intro_replica'],
        "Имя менеджера: " + output_dict['manager_name'],
        "Название компании: " + output_dict['company_name'],
        "Менеджер попрощался: " + output_dict['outro'],
        "В каждом диалоге обязательно необходимо поздороваться и попрощаться с клиентом: " + output_dict['condition'],
        sep='\n', end='\n\n'
    )

