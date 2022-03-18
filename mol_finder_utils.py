import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def get_min_max_filter(user_input_col_1, user_input_col_2, label, df_col_low, df_col_high, key_name, step=None, format_type=None):

    if format_type == 'int':
        user_input_col_1.number_input(label, int(df_col_low.min()), int(df_col_low.max()), value=int(df_col_low.min()), key=f'{key_name}_min', step=step)
        user_input_col_2.number_input('', int(df_col_high.min()), int(df_col_high.max()), value=int(df_col_high.max()), key=f'{key_name}_max', step=step)

    else:
        user_input_col_1.number_input(label, df_col_low.min(), df_col_low.max(), value=df_col_low.min(), key=f'{key_name}_min', step=step)
        user_input_col_2.number_input('', df_col_high.min(), df_col_high.max(), value=df_col_high.max(), key=f'{key_name}_max', step=step)


def set_filters_val_to_default(default_values):
    for the_key in st.session_state.keys():
        if the_key in default_values:
            # st.write(the_key)
            # st.write(default_values[the_key])
            st.session_state[the_key] = default_values[the_key]


def is_atom_in_smiles_enough_times(smiles, atom, min_count):
    cur_occurrences = smiles.count(atom)
    if cur_occurrences >= min_count:
        return True
    else:
        return False


def is_param_in_range(row, param_values):
    if len(param_values) == 4: # one df column
        param_name = param_values[0]
        range_min = float(param_values[1])
        range_max = float(param_values[2])
        if range_min <= row[param_name] <= range_max:
            return True

    else:
        param_name_low = param_values[0]
        param_name_high = param_values[1]
        range_min = float(param_values[2])
        range_max = float(param_values[3])
        if range_min <= row[param_name_low] and row[param_name_high] <= range_max:
            return True

    return False


def get_list_range(default_values):
    list_range = []
    ss = st.session_state
    if ss['pws_min'] != default_values['pws_min'] or ss['pws_max'] != default_values['pws_max']:
        list_range.append(['predicted_water_solubility', ss['pws_min'], ss['pws_max'], 'Predicted Water Solubility'])
    if ss['pb_min'] != default_values['pb_min'] or ss['pb_max'] != default_values['pb_max']:
        list_range.append(['pb_low', 'pb_high', ss['hl_max'], ss['hl_max'], 'Protein Binding'])
    if ss['hl_min'] != default_values['hl_min'] or ss['pb_max'] != default_values['pb_max']:
        list_range.append(['half_life_low', 'half_life_high', ss['hl_min'], ss['hl_max'], 'Half Life'])
    if ss['logp_min'] != default_values['logp_min'] or ss['logp_max'] != default_values['logp_max']:
        list_range.append(['experimental_logP', ss['logp_min'], ss['logp_max'], 'Experimental LogP'])
    if ss['pka_min'] != default_values['pka_min'] or ss['pka_max'] != default_values['pka_max']:
        list_range.append(['pKa_strongest_acidic', ss['pka_min'], ss['pka_max'], 'pKa Strongest Acidic'])
    if ss['pkb_min'] != default_values['pkb_min'] or ss['pkb_max'] != default_values['pkb_max']:
        list_range.append(['pKa_strongest_basic', ss['pkb_min'], ss['pkb_max'], 'pKa Strongest Basic'])
    if ss['charge_min'] != default_values['charge_min'] or ss['charge_max'] != default_values['charge_max']:
        list_range.append(['total_charge', ss['charge_min'], ss['charge_max'], 'Molecule Formal Charge'])
    if ss['dose_min'] != default_values['dose_min'] or ss['dose_max'] != default_values['dose_max']:
        list_range.append(['strength_norm', ss['dose_min'], ss['dose_max'], 'Dose Normalized Strength'])
    if ss['mw_min'] != default_values['mw_min'] or ss['mw_max'] != default_values['mw_max']:
        list_range.append(['molecular_weight', ss['mw_min'], ss['mw_max'], 'Molecular Weight'])
    if ss['n_rings_min'] != default_values['n_rings_min'] or ss['n_rings_max'] != default_values['n_rings_max']:
        list_range.append(['n_rings', ss['n_rings_min'], ss['n_rings_max'], '# Rings'])
    if ss['aromatic_rings_min'] != default_values['aromatic_rings_min'] or ss['aromatic_rings_max'] != default_values['aromatic_rings_max']:
        list_range.append(['aromatic_rings', ss['aromatic_rings_min'], ss['aromatic_rings_max'], '# Aromatic Rings'])
    if ss['n_heterocycles_min'] != default_values['n_heterocycles_min'] or ss['n_heterocycles_max'] != default_values['n_heterocycles_max']:
        list_range.append(['n_heterocycles', ss['n_heterocycles_min'], ss['n_heterocycles_max'], '# Heterocycles'])
    if ss['n_aromatic_heterocycles_min'] != default_values['n_aromatic_heterocycles_min'] or ss['n_aromatic_heterocycles_max'] != default_values['n_aromatic_heterocycles_max']:
        list_range.append(['n_aromatic_heterocycles', ss['n_aromatic_heterocycles_min'], ss['n_aromatic_heterocycles_max'], '# Aromatic Heterocycles'])
    if ss['n_saturated_heterocycles_min'] != default_values['n_saturated_heterocycles_min'] or ss['n_saturated_heterocycles_max'] != default_values['n_saturated_heterocycles_max']:
        list_range.append(['n_saturated_heterocycles', ss['n_saturated_heterocycles_min'], ss['n_saturated_heterocycles_max'], '# Saturated Heterocyclesg'])
    if ss['n_aliphatic_heterocycles_min'] != default_values['n_aliphatic_heterocycles_min'] or ss['n_aliphatic_heterocycles_max'] != default_values['n_aliphatic_heterocycles_max']:
        list_range.append(['n_aliphatic_heterocycles', ss['n_aliphatic_heterocycles_min'], ss['n_aliphatic_heterocycles_max'], '# Aliphatic Heterocycles'])
    return list_range


def get_smiles_dict():
    smiles_dict = {}
    for cur_smiles_key, cur_smiles_val in zip([st.session_state['smiles_1'],st.session_state['smiles_2'],st.session_state['smiles_3']],
                                              [st.session_state['smiles_count_1'],st.session_state['smiles_count_2'],st.session_state['smiles_count_3']]):
        smiles_key = cur_smiles_key
        if smiles_key != '':
            smiles_dict[smiles_key] = int(cur_smiles_val)
    if smiles_dict == {}:
        return None
    else:
        return smiles_dict


def is_smiles_condition_met(row, smiles_dict):
    for key, min_count in smiles_dict.items():
        if not is_atom_in_smiles_enough_times(row['SMILES'], key, min_count):
            return False
    return True


def is_mol_features_in_range(row, list_range):
    for cur_param in list_range:
        if not is_param_in_range(row, cur_param):
            return False
    return True


def get_filtered_drugs(df, smiles_dict=None, list_range=None,  roa=None):
    if not smiles_dict and not list_range and not roa:
        return None
    results_df = pd.DataFrame()
    id_list = []
    name_list = []
    roa_list = []
    if list_range:
        mol_filter_lists = [[] for i in range(len(list_range))]
    if roa:
        roa = roa.lower()
        df = df[df['route'].notna()]

    for index, row in df.iterrows():
        if roa:
            if roa not in row['route'].lower():
                continue

        if smiles_dict is not None:
            if not is_smiles_condition_met(row, smiles_dict):
                continue

        if list_range:
            if not is_mol_features_in_range(row, list_range):
                continue

        ## row is valid
        if roa:
            roa_list.append(row['route'])
        if list_range:
            for ind, cur_param in zip(range(len(list_range)), list_range):
                if len(cur_param) == 4:
                    mol_filter_lists[ind].append(row[cur_param[0]])
                elif len(cur_param) == 5:
                    if row[cur_param[0]] == row[cur_param[1]]:
                        mol_filter_lists[ind].append(f'{row[cur_param[0]]}')
                    else:
                        mol_filter_lists[ind].append(f'{row[cur_param[0]]}-{row[cur_param[1]]}')

        id_list.append(row['ID'])
        name_list.append(row['name'])

    results_df['Index'] = list(range(1, len(id_list)+1))
    results_df['DrugBank ID'] = id_list
    results_df['Name'] = name_list
    if roa:
        results_df['Route of Administration'] = roa_list
    if list_range:
        for ind, cur_param in zip(range(len(list_range)), list_range):
            results_df[cur_param[-1]] = mol_filter_lists[ind]
    # st.write(results_df)
    return results_df


def plot_result_df(results_df, results_filed):
    if results_df is None:
        results_filed.code('the results will appear here...', language="markdown")
        return

    if not results_df.empty:
        fig = go.Figure(data=go.Table(
            header=dict(values=list(results_df),
                        fill_color='#CAC4FF',
                        align='center'),
            cells=dict(values=results_df.transpose().values.tolist(),
                       fill_color='#E5ECF6',
                       align='left')))
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width=135*len(list(results_df)))
        results_filed.write(fig)
    elif results_df.empty:
        results_filed.code('No results were found, please try to relax the constraints', language="markdown")


def get_data_to_save(results_df):
    temp = pd.DataFrame()
    if results_df is None:
        return temp.to_csv(index=False).encode('utf-8')
    if not results_df.empty:
        return results_df.to_csv(index=False).encode('utf-8')
    else:
        return temp.to_csv(index=False).encode('utf-8')