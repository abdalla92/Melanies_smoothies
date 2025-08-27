# Import python packages
import streamlit as st
import requests
import pandas

# from snowflake.snowpark.context import get_active_session
cnx = st.connection("snowflake")
session = cnx.session()
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie!""")

name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be:", name_on_order)


# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df =  my_dataframe.to_pandas()
st.dataframe(data=pd_df, use_container_width=True)
st.stop()

ingredient_list = st.multiselect("Select upto 5 ingredient: ", my_dataframe, max_selections = 5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string = ''

    for fruit in ingredient_list:
        st.subheader(fruit + " Nutrition information")
        ingredients_string += fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        smoothie_froot_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order +"""' )"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
     session.sql(my_insert_stmt).collect()
     st.success('Your Smoothie is ordered!', icon="✅")
