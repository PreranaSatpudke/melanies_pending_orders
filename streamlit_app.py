# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col, when_matched

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders:cup_with_straw:")
st.write(
    f"""Orders that need to filled"""
)

#option = st.selectbox(
#    "What is your favourite fruit?",
#   ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favourite fruit is:", option)

#name_on_order = st.text_input("Name on Smoothie:")
#st.write("The name on your Smoothie will be ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

#st.dataframe(my_dataframe)


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
    
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])
    
            st.success('Order(s) Updated!', icon = '👍')
        except:
            st.write('Something went wrong.')

else:
    st.success('There are no pending orders right now', icon = '👍')
