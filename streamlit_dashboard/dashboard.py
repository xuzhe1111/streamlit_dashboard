import streamlit as st
import pandas as pd
import numpy as np

LIST_DICTKEYS = ['2002', '2005', '2010', 
                 '2502', '2505', '2510', 
                 '3002', '3005', '3010', 
                 '4002', '4005', '4010']


#0. 计算得到3个dataframes的结果，以备后用

#0-0. initialization
df_net_value_for_portfolio = pd.DataFrame(data=None, columns=['Timestamp', 
                                                              'actual_return_for_portfolio', 
                                                              'cumulative_return_for_portfolio', 
                                                              'net_value_for_portfolio']
                                                              )
df_net_value_for_portfolio_without_switch = pd.DataFrame(data=None, columns=['Timestamp', 
                                                                             'actual_return_for_portfolio_without_switch', 
                                                                             'cumulative_return_for_portfolio_without_switch', 
                                                                             'net_value_for_portfolio_without_switch']
                                                                             )
df_net_value_baseline = pd.DataFrame(data=None, columns=['Timestamp', 
                                                         'actual_return_baseline', 
                                                         'cumulative_return_baseline', 
                                                         'net_value_baseline']
                                                         )

#0-1. calculate and get the three dataframes
for i in range(len(LIST_DICTKEYS)):
    str_key = LIST_DICTKEYS[i]
    df_results_and_net_value = pd.read_csv(f"portfolio_files/{str_key}/df_results_and_net_value.csv", index_col=0)

    if i == 0:
        sr_actual_return_for_portfolio = df_results_and_net_value['actual_return_with_switch'].iloc[48 * 60:]
        sr_actual_return_for_portfolio_without_switch = df_results_and_net_value['actual_return'].iloc[48 * 60:]
        sr_actual_return_baseline = df_results_and_net_value['log_return'].iloc[48 * 60:]
    elif i > 0:
        sr_actual_return_for_portfolio = sr_actual_return_for_portfolio + df_results_and_net_value['actual_return_with_switch'].iloc[48 * 60:]
        sr_actual_return_for_portfolio_without_switch = sr_actual_return_for_portfolio_without_switch + df_results_and_net_value['actual_return'].iloc[48 * 60:]
        sr_actual_return_baseline = sr_actual_return_baseline + df_results_and_net_value['log_return'].iloc[48 * 60:]

sr_actual_return_for_portfolio = sr_actual_return_for_portfolio / len(LIST_DICTKEYS)
sr_actual_return_for_portfolio_without_switch = sr_actual_return_for_portfolio_without_switch / len(LIST_DICTKEYS)
sr_actual_return_baseline = sr_actual_return_baseline / len(LIST_DICTKEYS)

# df_net_value_for_portfolio
df_net_value_for_portfolio['Timestamp'] = df_results_and_net_value['Timestamp'].iloc[48 * 60:].copy()
df_net_value_for_portfolio['actual_return_for_portfolio'] = sr_actual_return_for_portfolio.round(7)
df_net_value_for_portfolio['cumulative_return_for_portfolio'] = df_net_value_for_portfolio['actual_return_for_portfolio'].cumsum().round(6)
df_net_value_for_portfolio['net_value_for_portfolio'] = (np.exp(df_net_value_for_portfolio['cumulative_return_for_portfolio']) * 1000).round(3)

# df_net_value_for_portfolio_without_switch
df_net_value_for_portfolio_without_switch['Timestamp'] = df_results_and_net_value['Timestamp'].iloc[48 * 60:].copy()
df_net_value_for_portfolio_without_switch['actual_return_for_portfolio_without_switch'] = sr_actual_return_for_portfolio_without_switch.round(7)
df_net_value_for_portfolio_without_switch['cumulative_return_for_portfolio_without_switch'] = df_net_value_for_portfolio_without_switch['actual_return_for_portfolio_without_switch'].cumsum().round(6)
df_net_value_for_portfolio_without_switch['net_value_for_portfolio_without_switch'] = (np.exp(df_net_value_for_portfolio_without_switch['cumulative_return_for_portfolio_without_switch']) * 1000).round(3)

# df_net_value_baseline
df_net_value_baseline['Timestamp'] = df_results_and_net_value['Timestamp'].iloc[48 * 60:].copy()
df_net_value_baseline['actual_return_baseline'] = sr_actual_return_baseline.round(7)
df_net_value_baseline['cumulative_return_baseline'] = df_net_value_baseline['actual_return_baseline'].cumsum().round(6)
df_net_value_baseline['net_value_baseline'] = (np.exp(df_net_value_baseline['cumulative_return_baseline']) * 1000).round(3)


#1. Title
st.title('Trading Monitoring System')

#2. Selectbox
option = st.selectbox(
    'Which part of the information would you like to see?',
    ('Charts', 'Status', 'DataFrames'))

#3. Main Page

#3-1. 和Charts有关的代码
if option == 'Charts':
    st.header('The Charts: ')

    option_charts = st.selectbox(
        'Which chart(s) do you want to see?', 
        ('All', 'Portfolio (with switch)', 'Portfolio (without switch)', 'Baseline'))

    if option_charts == 'All':

        st.subheader('All actual returns plotted together: ')
        df_actual_return_all_together = pd.concat([
            df_net_value_for_portfolio[['Timestamp', 'actual_return_for_portfolio']], 
            df_net_value_for_portfolio_without_switch['actual_return_for_portfolio_without_switch'], 
            df_net_value_baseline['actual_return_baseline']
        ], axis=1)
        df_actual_return_all_together.columns = ['Timestamp', 'Portfolio (with switch)', 'Portfolio (without switch)', 'Baseline']
        st.line_chart(data=df_actual_return_all_together, x='Timestamp', y=['Portfolio (with switch)', 
                                                                                'Portfolio (without switch)', 
                                                                                'Baseline']
                                                                                )
        
        st.subheader('All cumulative returns plotted together: ')
        df_cumulative_return_all_together = pd.concat([
            df_net_value_for_portfolio[['Timestamp', 'cumulative_return_for_portfolio']], 
            df_net_value_for_portfolio_without_switch['cumulative_return_for_portfolio_without_switch'], 
            df_net_value_baseline['cumulative_return_baseline']
        ], axis=1)
        df_cumulative_return_all_together.columns = ['Timestamp', 'Portfolio (with switch)', 'Portfolio (without switch)', 'Baseline']
        st.line_chart(data=df_cumulative_return_all_together, x='Timestamp', y=['Portfolio (with switch)', 
                                                                                'Portfolio (without switch)', 
                                                                                'Baseline']
                                                                                )

    elif option_charts == 'Portfolio (with switch)':
        st.subheader('Portfolio (with switch): ')
        st.line_chart(data=df_net_value_for_portfolio[['Timestamp', 'actual_return_for_portfolio']], x='Timestamp', y='actual_return_for_portfolio')
        st.line_chart(data=df_net_value_for_portfolio[['Timestamp', 'cumulative_return_for_portfolio']], x='Timestamp', y='cumulative_return_for_portfolio')
        #st.line_chart(data=df_net_value_for_portfolio[['Timestamp', 'net_value_for_portfolio']], x='Timestamp', y='net_value_for_portfolio')

    elif option_charts == 'Portfolio (without switch)':
        st.subheader('Portfolio (without switch): ')
        st.line_chart(data=df_net_value_for_portfolio_without_switch[['Timestamp', 'actual_return_for_portfolio_without_switch']], x='Timestamp', y='actual_return_for_portfolio_without_switch')
        st.line_chart(data=df_net_value_for_portfolio_without_switch[['Timestamp', 'cumulative_return_for_portfolio_without_switch']], x='Timestamp', y='cumulative_return_for_portfolio_without_switch')
        #st.line_chart(data=df_net_value_for_portfolio_without_switch[['Timestamp', 'net_value_for_portfolio_without_switch']], x='Timestamp', y='net_value_for_portfolio_without_switch')

    elif option_charts == 'Baseline':
        st.subheader('Baseline: ')
        st.line_chart(data=df_net_value_baseline[['Timestamp', 'actual_return_baseline']], x='Timestamp', y='actual_return_baseline')
        st.line_chart(data=df_net_value_baseline[['Timestamp', 'cumulative_return_baseline']], x='Timestamp', y='cumulative_return_baseline')
        #st.line_chart(data=df_net_value_baseline[['Timestamp', 'net_value_baseline']], x='Timestamp', y='net_value_baseline')


#3-2. 和Status有关的代码
elif option == 'Status':
    st.header('Real-time Status of The 12 Subsystems: ')

    df_status = pd.DataFrame(data=None, index=LIST_DICTKEYS, columns=['actual_position_status', 
                                                                      'n_of_transactions', 
                                                                      'position_status', 
                                                                      'switch_status']
                                                                      )
    for i in range(len(LIST_DICTKEYS)):
        str_key = LIST_DICTKEYS[i]
        sr_status = pd.read_csv(f"portfolio_files/{str_key}/sr_status.csv", index_col=0)
        df_status.loc[str_key] = sr_status.values.reshape(-1)
    
    st.dataframe(df_status, height=455)


#3-3. 和DataFrames有关的代码
elif option == 'DataFrames':
    st.header('The Three Dataframes: ')

    st.subheader('Portfolio (with switch): ')
    st.dataframe(df_net_value_for_portfolio)

    st.subheader('Portfolio (without switch): ')
    st.dataframe(df_net_value_for_portfolio_without_switch)

    st.subheader('Baseline: ')
    st.dataframe(df_net_value_baseline)



