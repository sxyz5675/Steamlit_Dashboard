import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
churn_mapping = {"No": 0, "Yes": 1}
df['ChurnVal'] = df['Churn'].map(churn_mapping)
tmp_df = df[~df.TotalCharges.str.contains(" ")]
tmp_df['TotalCharges'] = pd.to_numeric(tmp_df['TotalCharges'])

# Calculate tenure as described
tenure_calc = tmp_df.TotalCharges / tmp_df.MonthlyCharges


# Set page configuration
st.set_page_config(
    page_title='Customer Churn Analysis Dashboard',
    page_icon='✅',
    layout='wide'
)



# Dashboard title
st.title("Customer Churn Analysis Dashboard 📊")

# Create two card containers
col1, col2 = st.columns(2)

# Plot 1: Distribution of Gender %
with col1:
    with st.container():
        fig1, axes1 = plt.subplots(figsize=(8, 6))
        data1 = df["gender"].value_counts(normalize=True)
        axes1.bar(data1.index, data1 * 100, color=['green', 'red'])
        axes1.set_ylabel('Percentage')
        axes1.set_ylim(0, 100)
        st.pyplot(fig1)

# Plot 2: Tenure comparison plot
with col2:
    with st.container():
        fig2, axes2 = plt.subplots(figsize=(8, 6))
        sns.kdeplot(df.tenure, marker='o', c='b', label="Actual", ax=axes2)
        sns.kdeplot(tenure_calc, marker='+', c='r', label="Calculated", ax=axes2)
        axes2.set_xlabel('Tenure')
        axes2.legend()
        st.pyplot(fig2)


# Plot 3: Churn rates based on monthly charges (smaller size)
with st.container():
    fig3, axes3 = plt.subplots(figsize=(15, 5))  # Reduce height
    # Categorize MonthlyCharges into bins and plot
    df['MonthlyChargesCategory'] = pd.cut(df["MonthlyCharges"], bins=10)
    # Define colors for the bars
    colors = sns.color_palette("pastel", 10)
    sns.barplot(x='MonthlyChargesCategory', y='ChurnVal', data=df, ci=None, ax=axes3, palette=colors)
    axes3.set_title('Churn rates based on monthly charges')
    # Customize background color
    axes3.set_facecolor('#2e2e2e')  # Dark background
    # Customize grid color
    axes3.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)  # Light gray grid
    st.pyplot(fig3)


# Data View
st.subheader("Data View")
st.dataframe(df.head(10))

# Create two columns layout for plots 4 and 5
col3, col4 = st.columns(2)

# Plot 4: Distribution of Monthly Charges
with col3:
    with st.container():
        fig4, axes4 = plt.subplots(figsize=(6, 3))
        sns.distplot(df.MonthlyCharges, color='lightblue', ax=axes4)
        axes4.set_title('Distribution of Monthly Charges')
        axes4.set_xlim(0, 140)
        axes4.set_facecolor('#2e2e2e')
        st.pyplot(fig4)

# Plot 5: % of Customers by Tenure
with col4:
    with st.container():
        fig5, axes5 = plt.subplots(figsize=(6, 3))
        sns.distplot(df.tenure, color='pink', ax=axes5)
        axes5.set_title('% of Customers by Tenure')
        axes5.set_xticks(np.arange(0, 100, 10))
        axes5.set_xlim(0, 140)
        axes5.set_facecolor('#2e2e2e')
        st.pyplot(fig5)