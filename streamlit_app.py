import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

ingredients_string = ''

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string = ingredients_string + fruit_chosen + ' '

time_to_insert = st.button('Submit Order')

if time_to_insert:
    my_insert_stmt = f"""
        insert into smoothies.public.orders (name_on_order, ingredients)
        values ('{name_on_order}', '{ingredients_string.strip()}')
    """
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
