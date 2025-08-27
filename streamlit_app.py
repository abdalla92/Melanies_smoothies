# Import python packages
import streamlit as st
import requests

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredient_list = st.multiselect("Select upto 5 ingredient: ", my_dataframe, max_selections = 5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string = ''

    for fruit in ingredient_list:
        ingredients_string += fruit + ' '
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order +"""' )"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
     session.sql(my_insert_stmt).collect()
     st.success('Your Smoothie is ordered!', icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
smoothie_froot = smoothiefroot_response.json()
smoothie_froot_df = st.dataframe(data=smoothie_froot, use_container_width=True)
