import streamlit as st
import pandas as pd
import numpy as np

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


@st.cache
def get_data(file_name):
    return pd.read_csv(file_name)


## TODO:
# @st.cache
# def get_filter_range(df):
#     for col in list(df):
#


# .sidebar.sidebar - content
# {
#     background: url("url_goes_here")
# }

with title_con:
    # st.title('Mol Finder')
    st.image('title.png')

with main_con:
    df = get_data('drug_bank_database.csv')
    user_input_col_1, user_input_col_2, results_col = st.columns([1, 1, 5])
    user_input_col_1.subheader('Filters')
    smiles_str_1 = user_input_col_1.text_input('SMILES string I')
    smiles_str_2 = user_input_col_1.text_input('SMILES string II')
    smiles_str_3 = user_input_col_1.text_input('SMILES string III')
    user_input_col_2.subheader('Occurrences')
    smiles_count_1 = user_input_col_2.number_input(' ', 1, 99, key='SMILES I')
    smiles_count_2 = user_input_col_2.number_input(' ', 1, 99, key='SMILES II')
    smiles_count_3 = user_input_col_2.number_input(' ', 1, 99, key='SMILES III')

    roa_str = user_input_col_1.text_input('Route of Administration')
    user_input_col_2.markdown('#')
    user_input_col_2.markdown('#')
    user_input_col_2.markdown('###')

    user_input_col_1.markdown('##### Min')
    user_input_col_2.markdown('##### Max')

    pws_min = user_input_col_1.number_input('Predicted Water Solubility', df['predicted_water_solubility'].min(),
                                            df['predicted_water_solubility'].max(),
                                            value=df['predicted_water_solubility'].min())
    pws_max = user_input_col_2.number_input('', df['predicted_water_solubility'].min(),
                                            df['predicted_water_solubility'].max(),
                                            value=df['predicted_water_solubility'].max(), key='pws_max')
    pb_min = user_input_col_1.number_input('Protein Binding', df['pb_low'].min(), df['pb_low'].max(),
                                           value=df['pb_low'].min())
    pb_max = user_input_col_2.number_input('', df['pb_high'].min(), df['pb_high'].max(), value=df['pb_high'].max(),
                                           key='pb_max')
    hf_min = user_input_col_1.number_input('Half Life', df['half_life_low'].min(), df['half_life_low'].max(),
                                           value=df['half_life_low'].min())
    hf_max = user_input_col_2.number_input('', df['half_life_high'].min(), df['half_life_high'].max(),
                                           value=df['half_life_high'].max(), key='hl_max')

    results_col.subheader('Results')
    results_col.markdown('##')
    results_filed = results_col.code('the results will appear here...', language="markdown")
    result_str = 'the results will appear here...'

with buttons_con:
    button_col1, button_col2, button_col3, button_col4 = st.columns([1, 1, 1, 7])
    run_button = button_col1.button('Run Search')
    clear_button = button_col2.button('Clear Filters')
    if run_button:
        result_str = 'bla'
        results_filed.code(result_str, language="markdown")

    if clear_button:
        result_str = 'the results will appear here...'
        results_filed.code(result_str, language="markdown")

    save_button = button_col3.download_button('Save Results', str(result_str))
