
from snowflake.snowpark import Session
import streamlit as st
import pandas as pd
from config import conn_params
from datetime import date



def test_price():
    
    session = Session.builder.configs(conn_params).create()

    show_result = st.sidebar.checkbox("Show Result", True)
    show_graph = st.sidebar.checkbox("Show Graph", False)
    graph_type = st.sidebar.multiselect("Select graph type:", ["Bar chart","Double Bar Chart", "Line chart", "3D Scatter Plot","Scatter Plot", "Pie chart"],default="Bar chart")


    
    str="Know you Base Price"
    st.title(str)
    st.sidebar.write("")

    def calculate_age_adjustment(age):
        age = int(age)
        age_ranges = {
            (0, 3): 0.01,
            (4, 4): 0.015,
            (5, 5): 0.02,
            (6, 6): 0.025,
            (7, 7): 0.03,
            (8, 8): 0.04,
            (9, 9): 0.05,
            (10, 10): 0.06,
            (11, 14): 0.075,
            (15, 20): 0.1,
            (21, 30): 0.15,
            (31, 40): 0.2,
            (41, float('inf')): 0.3
        }
        for age_range, adjustment in age_ranges.items():
            start, end = age_range
            if start <= age <= end:
                return basic_price + basic_price * adjustment
        return 0

    colx,coly = st.columns([20,1])
    with colx:
        prods =  st.container()
    
        with prods:
            car_model = session.sql(" SELECT DISTINCT CAR_MODEL FROM SNOWIOT_DB.PUBLIC.CAR_INFO ").collect()
            car_model = pd.DataFrame(car_model)
            cm = st.selectbox("# **Car Model**", options=car_model, placeholder="Select the Car Model")

            dist_range = session.sql("SELECT DISTINCT RANGEINKM FROM SNOWIOT_DB.PUBLIC.CAR_BRIEF ").collect()
            dist_range = pd.DataFrame(dist_range)
            dr = st.selectbox("# **Distance Travelled**", options=dist_range, placeholder="Select the range")

            # year = session.sql("SELECT DISTINCT MANUFACTUR_YEAR FROM SNOWPILOT_DB.RAW.CAR_INFO ORDER BY MANUFACTUR_YEAR DESC").collect()
            # year = pd.DataFrame(year)
            #input
            number = st.text_input(" **Manufacture Year**")

            # my = st.selectbox("# **Manufacturing year**", options=year, placeholder="Select the manufacturing year of the Car")

            if st.button('Calculate'):
                error=0     
                try:
                    number = int(number)
                except ValueError:
                    st.write(f'<span style="font-size: 20px;">Please Enter Valid Year</span>', unsafe_allow_html=True)
                    number = None
                    error=1
                
                if error==0:

                    today = date.today()
                    age = today.year - int(number)
                    #button
                    basic_price = session.sql(f"select TRY_CAST(REGEXP_REPLACE(BASIC_PRICE, '\\\$', '') AS FLOAT) as baseprice from PUBLIC.car_info a join PUBLIC.car_brief b on a.MODEL_ID = b.car_id where a.car_model = '{cm}' and b.rangeinkm = '{dr}'").collect()
                    basic_price = pd.DataFrame(basic_price)
                    x=calculate_age_adjustment(age)
                    value=x.loc[0][0];
                    st.write("")
                    st.write("")
                    
                    st.markdown(f"""<div style="                        
                                text-align: center;                     
                                font-size: 22px;
                                color: #000000;">The Base Price for this Vehicle is {value}  </div>""",unsafe_allow_html=True)

                    
            else:
                pass
            
            
        
    with coly:
        st.write("")