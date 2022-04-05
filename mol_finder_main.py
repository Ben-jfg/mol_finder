import streamlit as st
import pandas as pd
import numpy as np

from mol_finder_utils import *
import plotly.graph_objects as go

st.set_page_config(layout="wide")

title_con = st.container()
main_con = st.container()
buttons_con = st.container()
image_con = st.container()


# st.markdown(
#     """
#     <style>
#     .main {
#     background-color: #EDFFF6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

## TODO: 2. add CAS?

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_data(data_base_file_name):
    df = pd.read_csv(data_base_file_name)
    st.write('')
    default_values= {}
    default_values['smiles_1'] = ''
    default_values['smiles_1a'] = ''
    default_values['smiles_1b'] = ''
    default_values['smiles_2'] = ''
    default_values['smiles_3'] = ''
    default_values['smiles_count_1'] = 1
    default_values['smiles_count_2'] = 1
    default_values['smiles_count_3'] = 1
    default_values['roa'] = ''
    default_values['pws_min'] = round(df['predicted_water_solubility'].min(), num_of_digits)
    default_values['pws_max'] = round(df['predicted_water_solubility'].max(), num_of_digits)
    default_values['pb_min'] = round(df['pb_low'].min(), num_of_digits)
    default_values['pb_max'] = round(df['pb_high'].max(), num_of_digits)
    default_values['hl_min'] = round(df['half_life_low'].min(), num_of_digits)
    default_values['hl_max'] = round(df['half_life_high'].max(), num_of_digits)
    default_values['logp_min'] = round(df['experimental_logP'].min(), num_of_digits)
    default_values['logp_max'] = round(df['experimental_logP'].max(), num_of_digits)
    default_values['pka_min'] = round(df['pKa_strongest_acidic'].min(), num_of_digits)
    default_values['pka_max'] = round(df['pKa_strongest_acidic'].max(), num_of_digits)
    default_values['pkb_min'] = round(df['pKa_strongest_basic'].min(), num_of_digits)
    default_values['pkb_max'] = round(df['pKa_strongest_basic'].max(), num_of_digits)
    default_values['charge_min'] = round(df['total_charge'].min(), num_of_digits)
    default_values['charge_max'] = round(df['total_charge'].max(), num_of_digits)
    default_values['dose_min'] = round(df['strength_norm'].min(), num_of_digits)
    default_values['dose_max'] = round(df['strength_norm'].max(), num_of_digits)
    default_values['mw_min'] = round(df['molecular_weight'].min(), num_of_digits)
    default_values['mw_max'] = round(df['molecular_weight'].max(), num_of_digits)
    default_values['n_rings_min'] = round(df['n_rings'].min(), num_of_digits)
    default_values['n_rings_max'] = round(df['n_rings'].max(), num_of_digits)
    default_values['aromatic_rings_min'] = round(df['aromatic_rings'].min(), num_of_digits)
    default_values['aromatic_rings_max'] = round(df['aromatic_rings'].max(), num_of_digits)
    default_values['n_heterocycles_min'] = round(df['n_heterocycles'].min(), num_of_digits)
    default_values['n_heterocycles_max'] = round(df['n_heterocycles'].max(), num_of_digits)
    default_values['n_aromatic_heterocycles_min'] = round(df['n_aromatic_heterocycles'].min(), num_of_digits)
    default_values['n_aromatic_heterocycles_max'] = round(df['n_aromatic_heterocycles'].max(), num_of_digits)
    default_values['n_saturated_heterocycles_min'] = round(df['n_saturated_heterocycles'].min(), num_of_digits)
    default_values['n_saturated_heterocycles_max'] = round(df['n_saturated_heterocycles'].max(), num_of_digits)
    default_values['n_aliphatic_heterocycles_min'] = round(df['n_aliphatic_heterocycles'].min(), num_of_digits)
    default_values['n_aliphatic_heterocycles_max'] = round(df['n_aliphatic_heterocycles'].max(), num_of_digits)
    # st.write(default_values['hl_max'])

    return df, default_values


## TODO:
# @st.cache
# def get_filter_range(df):
#     for col in list(df):
#


# .sidebar.sidebar - content
# {
#     background: url("url_goes_here")
# }

df, default_values = get_data('drug_bank_database.csv')
# "debug", st.session_state

with title_con:
    # st.title('Mol Finder')
    st.image('title.png')

with buttons_con:
    button_col1, button_col2, button_col3, button_col4 = st.columns([1, 1, 1, 5])
    clear_button = button_col1.button('Clear Filters')

    if clear_button:
        set_filters_val_to_default(default_values)

with main_con:
    user_input_col_1, user_input_col_2, results_col = st.columns([1, 1, 5])

    result_str = 'the results will appear here...'
    user_input_col_1.subheader('Filters')
    smiles_str_1 = user_input_col_1.text_input('SMILES string I', key='smiles_1')
    smiles_str_1a = user_input_col_1.text_input('SMILES string I A (or)', key='smiles_1a')
    smiles_str_1b = user_input_col_1.text_input('SMILES string I B (or)', key='smiles_1b')
    smiles_str_2 = user_input_col_1.text_input('SMILES string II (and)', key='smiles_2')
    smiles_str_3 = user_input_col_1.text_input('SMILES string III (and)', key='smiles_3')
    user_input_col_2.subheader('Occurrences')
    smiles_count_1 = user_input_col_2.number_input(' ', 1, 99, key='smiles_count_1')
    user_input_col_2.text_input('-', key='hold1', disabled=True)
    user_input_col_2.text_input('-', key='hold2', disabled=True)

    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    # user_input_col_2.markdown('#####')
    smiles_count_2 = user_input_col_2.number_input(' ', 1, 99, key='smiles_count_2')
    smiles_count_3 = user_input_col_2.number_input(' ', 1, 99, key='smiles_count_3')

    roa_str = user_input_col_1.text_input('Route of Administration', key='roa')
    user_input_col_2.text_input('-', key='hold3', disabled=True)

    # user_input_col_2.markdown('#')
    # user_input_col_2.markdown('#')
    # user_input_col_2.markdown('###')

    user_input_col_1.markdown('##### Min')
    user_input_col_2.markdown('##### Max')

    get_min_max_filter(user_input_col_1, user_input_col_2, 'Predicted Water Solubility [mg/mL]',
                                   df['predicted_water_solubility'], df['predicted_water_solubility'], 'pws', step=0.5)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Protein Binding [%]', df['pb_low'], df['pb_high'],
                                  'pb', step=0.1)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Half Life [hours]', df['half_life_low'],
                                  df['half_life_high'], 'hl', step=1.0)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Experimental LogP', df['experimental_logP'],
                                    df['experimental_logP'], 'logp', step=0.5)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'pKa Strongest Acidic',
                                   df['pKa_strongest_acidic'], df['pKa_strongest_acidic'], 'pka', step=0.5)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'pKa Strongest Basic', df['pKa_strongest_basic'],
                                   df['pKa_strongest_basic'], 'pkb', step=0.5)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Molecule Formal Charge', df['total_charge'],
                                      df['total_charge'], 'charge', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Dose Normalized Strength [mg]', df['strength_norm'],
                                   df['strength_norm'], 'dose', step=10.0)
    get_min_max_filter(user_input_col_1, user_input_col_2, 'Molecular Weight [g/mol]', df['molecular_weight'],
                                  df['molecular_weight'], 'mw', step=10.0)
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Rings', df['n_rings'], df['n_rings'],
                                       'n_rings', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Aromatic Rings',
                                              df['aromatic_rings'],
                                              df['aromatic_rings'], 'aromatic_rings', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Heterocycles',
                                              df['n_heterocycles'],
                                              df['n_heterocycles'], 'n_heterocycles', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Aromatic Heterocycles',
                                                       df['n_aromatic_heterocycles'], df['n_aromatic_heterocycles'],
                                                       'n_aromatic_heterocycles', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Saturated Heterocycles',
                                                       df['n_saturated_heterocycles'], df['n_saturated_heterocycles'],
                                                       'n_saturated_heterocycles', format_type='int')
    get_min_max_filter(user_input_col_1, user_input_col_2, '# Aliphatic Heterocycles',
                                                        df['n_aliphatic_heterocycles'], df['n_aliphatic_heterocycles'],
                                                        'n_aliphatic_heterocycles', format_type='int')

    results_col.subheader('Results')
    results_col.markdown('##')
    results_filed = results_col.code('the results will appear here...', language="markdown")


results_df = get_filtered_drugs(df, smiles_dict=get_smiles_dict(), list_range=get_list_range(default_values),
                                roa=st.session_state['roa'])
plot_result_df(results_df, results_filed)

with buttons_con:
    df_to_save = get_data_to_save(results_df)
    save_button = button_col2.download_button(
        label="Download Results",
        data=df_to_save,
        file_name='mol_finder_search_results.csv',
        mime='text/csv',
    )

# import streamlit.components.v1 as components
#
# components.html(
#     """
# <script>
# const elements = window.parent.document.querySelectorAll('.stNumberInput div[data-baseweb="input"] > div')
# console.log(elements)
# elements[16].style.backgroundColor = 'red'
# </script>
# """,
#     height=0,
#     width=0,
# )