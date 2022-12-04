import plotly as plt
import streamlit as st
import pandas as pd


df = pd.read_csv('./crimedata.csv')

crime_types = ["murders", "rapes", "robberies", "assaults", "burglaries", "larcenies", "autoTheft", "arsons"]
per_pop = {"murders": "murdPerPop", "rapes": "rapesPerPop", "robberies": "robbbPerPop", "assaults": "assaultPerPop",
           "burglaries": "burglPerPop", "larcenies": "larcPerPop", "autoTheft": "autoTheftPerPop",
           "arsons": "arsonsPerPop"}

definition = {"murders": "Murder is the unlawful killing of another human without justification or valid excuse, especially the unlawful killing of another human with malice aforethought.",
              "rapes": "Rape is a type of sexual assault usually involving sexual intercourse or other forms of sexual penetration carried out against a person without their consent.",
              "robberies": "Robbery is the crime of taking or attempting to take anything of value by force, threat of force, or by use of fear.",
              "assaults": "An assault is the act of committing physical harm or unwanted physical contact upon a person or, in some specific legal definitions, a threat or attempt to commit such an action.",
              "burglaries": "Burglary, also called breaking and entering and sometimes housebreaking, is the act of entering a building or other areas without permission, with the intention of committing a criminal offence.",
              "larcenies": "Larceny is a crime involving the unlawful taking or theft of the personal property of another person or business.",
              "autoTheft": "Autotheft is an is the act of taking another person's car without that person's permission or consent with the intent to deprive the rightful owner of it.",
              "arsons": "Arson is the crime of willfully and deliberately setting fire to or charring property."}

st.set_page_config(
    page_title="Crimes in US Communities",
    page_icon="🐍",
    layout="wide",
)

st.title("Crimes in US Communities")
st.write("This site presents statistical information about crimes in the US by state. "
         "Please, use the sidebar on the left to choose the data you want to see. "
         "Several options are available.")


####################################################################################################

opt1 = st.sidebar.subheader("Option 1")
st.sidebar.write("Analyse the type of the crime by state")

crime_type_selectbox = st.sidebar.selectbox(
    'Сhoose the type of the crime',
    crime_types
)
button1 = st.sidebar.button("Apply", key=1)

if button1:
    st.subheader(definition[crime_type_selectbox])
    sub_df = df[["state", crime_type_selectbox]]
    sub_df = sub_df.groupby("state").sum()
    st.dataframe(sub_df.transpose())
    st.bar_chart(sub_df.reset_index(), x="state", y=crime_type_selectbox)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("5 best states by "+crime_type_selectbox)
        sub_df_1 = sub_df.sort_values(crime_type_selectbox, ascending=True)[:5]
        st.dataframe(sub_df_1, use_container_width=True)

    with col2:
        st.subheader("5 worst states by " + crime_type_selectbox)
        sub_df_2 = (sub_df.sort_values(crime_type_selectbox, ascending=False))[:5]
        st.dataframe(sub_df_2, use_container_width=True)



####################################################################################################

opt2 = st.sidebar.subheader("Option 2")
st.sidebar.write("Analyse one state by the crime types")

state_selectbox = st.sidebar.selectbox(
    'Сhoose the state',
    pd.unique(df["state"])
)

button2 = st.sidebar.button("Apply", key=2)

if button2:
    df_cols = ["state"]
    df_cols_1 = ["state"]
    for i in crime_types:
        df_cols.append(i)
        df_cols_1.append(per_pop[i])

    column1, column2 = st.columns(2)
    with column1:
        st.subheader("Total number of crimes")
        sub_df_1 = df[df_cols].groupby("state").sum().loc[state_selectbox].transpose()
        st.dataframe(sub_df_1, use_container_width=True)

    with column2:
        st.subheader("Number of crimes per population")
        sub_df_2 = df[df_cols_1].groupby("state").sum().loc[state_selectbox].transpose()
        st.dataframe(sub_df_2, use_container_width=True)

    st.bar_chart(sub_df_1)

####################################################################################################


opt3 = st.sidebar.subheader("Option 3")
st.sidebar.write("See relation between the total number of crimes and other factors")

factors = ["Percentage of black people", "Median income", "Percentage of people from 12 to 21 y.o.", "Unemployment level"]

factors_dict = {"Percentage of black people": "racepctblack", "Median income": "medIncome",
                "Percentage of people from 12 to 21 y.o.": "agePct12t21", "Unemployment level": "PctUnemployed"}

factor_selectbox = st.sidebar.selectbox(
    'Сhoose the factor',
    factors
)

df["all_crimes"] = df["murders"] + df["rapes"] + df["robberies"] + df["assaults"] + df["burglaries"] + df["larcenies"] +\
                   df["autoTheft"] + df["arsons"]

button3 = st.sidebar.button("Apply", key=3)

if button3:
    factor = factor_selectbox
    factor_name = factors_dict[factor]
    st.subheader("This linechart shows the relation between " + factor.lower() + " and the total number of crimes")
    sub_df_3 = df[[factor_name, "all_crimes"]]
    st.line_chart(sub_df_3, y="all_crimes", x=factor_name)

