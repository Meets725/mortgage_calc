import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import math

st.title('હોમ લોન કેલ્ક્યુલેટર - મિત સુથાર')

st.write('### માહિતી આપો')
col1, col2 = st.columns(2)
home_value = col1.number_input('ઘરની કિંમત', min_value=0, value=500000)
deposit = col1.number_input('એડવાન્સ ', min_value=0, value=100000)
interest_rate = col2.number_input('ઇન્ટરેસ્ટ રેટ (%)', min_value=0.0, value=5.5)
loan_term = col2.number_input('મુદત (વર્ષ)', min_value=0, value=30)


# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount *
    (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) /
    ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write('### કેટલા ભરવાના')
col1, col2, col3 = st.columns(3)
col1.metric(label="માસિક હપ્તો", value=f"Rs. {monthly_payment:.2f}")
col2.metric(label="કુલ ચુકવણી", value=f"Rs. {total_payments:.2f}")
col3.metric(label="કુલ વ્યાજ", value=f"Rs. {total_interest:.2f}")

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payments", "Principle", "Interst", "Remaining Balance", "Year"],
)

#display the data frame as a chart.
st.write('### ચુકવણી સમયપત્રક')
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df, x_label="વર્ષ", y_label="બાકી રહેલી રકમ")
