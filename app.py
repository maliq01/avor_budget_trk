import requests as requests
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie


import database as db
import pdatabase as pdb

from datetime import datetime
import calendar


def get_username():
    items = pdb.fetch_all_username()
    username = [item["key"] for item in items]
    return username.items

# setting variable
page_title = "Avor Budget tracker"
page_icon = Image.open("pic/avor.png")
layout = "centered"
contributions = ["Salary", "Rental income", "Business" , "Online income", "Other incomes"]
investments= ["Rent", "Savings", "Business expenses", "Other expenses"]
logo = Image.open("pic/avor.png")
currency = "ksh"

# setting page config
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)



# hiding st style css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

local_css("style/style.css")

# loading lottie files
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

budget_lottie = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_oOGQFY.json")
savings_lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_gxtah1wp.json")
data_vil = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_khwfxgwr.json")


with st.sidebar:
    choice = option_menu(
        menu_title = None,
        options = ["Home", "Log in", "Sign up"],
        orientation = "vevrticle"
    )

def logo_place_holder():
    with st.container():
        logo_column, title_column = st.columns((1, 2))
        with logo_column:
            st.image(logo)
        with title_column:
            st.header(page_title)
            st.write("where every cent makes sense")
if choice == "Home":
    logo_place_holder()
    with st.container():
        col1, col2, = st.columns((1, 2))
        with col2:
            st.subheader("Money Tracker")
            st.write(
                """
            Take the guesswork out of managing your money. Avor Tracker makes it easy to plan, spend, and track your money 
            with features you’ll love to use.
             """)
        with col1:
            st_lottie(budget_lottie)
    with st.container():
        col3, col4 =st.columns((2, 1))
        with col3:
            st.subheader("Saving goals")
            st.write(
                """
            Protect yourself from life’s little (and big) emergencies and prepare for big purchases with sinking funds 
            and savings goals.
            """)
        with col4:
            st_lottie(savings_lottie)
    with st.container():
        col5, col6 =st.columns((1, 2))
        with col6:
            st.subheader("Track transactions with one click.")
            st.write(
                """
                AvorTracker helps you track your income and expenses by offering a cutting edge and interactive grapghical
                representation of all your income and expenses
            """)
            with col5:
                st_lottie(data_vil)
    st.write("contact us")
    contact_form = """
            <form action="https://formsubmit.co/kedward.nganga@gmail.com" method="POST">
            <input type = "hidden" name ="captcha" value ="False">
            <input type="text" name="name" placeholder= "your name" required>
            <input type="email" name="email" placeholder = "your email" required>
            <textarea name= "message" placeholder = "your message" required></textarea>
            <button type="submit">Send</button>
            </form>
       """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()



if choice == "Sign up":
    logo_place_holder()
    st.subheader("Sign up")
    username = st.text_input("user name")
    password = st.text_input("password", type='password')
    if st.button("sign up"):
        pdb.insert_username(username, password)
        st.success("welcome {}".format(username))
        st.info("go to log in to continue")

if choice == "Log in":
    logo_place_holder()
    st.subheader("log in")
    st.info("click on the side bar to log in")
    username = st.sidebar.text_input("user input")
    password = st.sidebar.text_input("password", type='password')
    if st.sidebar.checkbox("log in"):
        log_in_user = pdb.get_username(username)
        if log_in_user:
            st.success("logged in as {}".format(username))

            with st.container():
                logo_column, title_column = st.columns((1, 2))
                with logo_column:
                    st.image(logo)
                with title_column:
                    st.header(page_title)
                    st.write("where every cent makes sense")

            # setting year and month

            years = (datetime.today().year, datetime.today().year +1)
            months = list(calendar.month_name[1:])

            # --------DATABASE INTERFACE-------
            def get_all_periods():
                items = db.fetch_all_periods()
                periods = [item["key"] for item in items]
                return periods

            # putting option menu
            selected = option_menu(
                menu_title=None,
                options=["data entry", "data visualization"],
                orientation="horizontal"

            )

            # setting up form
            if selected == "data entry":
                st.header(f"Data entry in {currency}")
                with st.form("entry_form", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    col1.selectbox("select month",  months,  key="month")
                    col2.selectbox("select year", years, key="year")

                    "___"

                    with st.expander("income"):
                        for contribution in contributions:
                            st.number_input(f"{contribution}", min_value=0, format="%i", step=10, key=contribution)
                    with st.expander("expenses"):
                        for investment in investments:
                            st.number_input(f"{investment}", min_value=0, format="%i",  step=10, key=investment)
                    with st.expander("comment"):
                        comment = st.text_area(" ", placeholder="enter comment")


                # setting up submit button

                    submitted = st.form_submit_button("save data")
                    if submitted:
                        period = str(st.session_state["year"]) + " -" + str(st.session_state["month"])
                        contributions = {contribution: st.session_state[contribution] for contribution in contributions}
                        investments = {investment: st.session_state[investment] for investment in investments}
                        db.insert_period(period, contributions, investments, comment)
                        st.success("data saved")

            # plotting the data
            if selected == "data visualization":
                st.header("data visualisation")
                with st.form("saved_period"):
                    period= st.selectbox("selected period", get_all_periods())
                    submitted = st.form_submit_button("plot period")
                    if submitted:
                       period_data = db.get_period(period)
                       comment = period_data.get("comment")
                       investments = period_data.get("investments")
                       contributions =period_data.get("contributions")

            # create metric
                       total_income = sum(contributions.values())
                       total_expenses = sum(investments.values())
                       remaining_budget = (total_income - total_expenses)
                       col1, col2, col3, = st.columns(3)
                       col1.metric("total income:", f"{total_income} {currency}")
                       col2.metric(f" total expenses:", f" { total_expenses} {currency}")
                       col3.metric(f" remaining budget:", f"{remaining_budget} {currency}")
                       st.text(f"comment: {comment }")

                #creating the senky chart
                label = list(contributions.keys()) + ["total income"] + list(investments.keys())
                source = list(range(len(contributions))) +[len(contributions)] * len(investments)
                target = [len(contributions)] * len(contributions) + [label.index(investment) for investment in investments]
                value = list(contributions.values()) + list(investments.values())

                #data to dictionary, dictionary to sankey
                link = dict(source=source, target=target, value=value)
                node = dict(label=label, pad=20, thickness= 30, color="#00FF00")
                data = go.Sankey(link=link, node=node)

                #ploting it
                fig = go.Figure(data)
                fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Password/ Username is incorrect")

