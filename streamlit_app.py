# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """
)

#option=st.selectbox(
#    'How would you like to be contacted?',
#    ('Email', 'Home Phone', 'Mobile Phone')
#   )
#st.write('You selected:', option)

#option=st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana', 'Strawberries', 'Peaches', 'Apple', 'Grapes', 'Mango')
#)
#st.write('Your favorite fruit is:', option)
#title=st.text_input('Movie Title','Life of Brian')
#st.write('The Current Movie Title is', title)

name_on_order=st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)

#session=get_active_session()
cnx=st.connection('snowflake')
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col(SEAARCH_ON))
st.dataframe(data=my_dataframe,use_container_width=True)
st.stop()
ingredients_list=st.multiselect('Choose up to 5 ingredients:'
                                , my_dataframe
                                , max_selections=5)
if ingredients_list:
    ingredients_string=''
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string +"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")



