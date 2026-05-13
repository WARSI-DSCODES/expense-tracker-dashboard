import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Expense Tracker Dashboard",
    layout="wide"
)

# ------------------------------------------------
# Title
# ------------------------------------------------

st.title("Expense Analysis & Budget Planning Dashboard")

st.write(
    "Track expenses, analyze spending, and manage monthly budgets."
)

# ------------------------------------------------
# User Login Section
# ------------------------------------------------

st.sidebar.header("User Login")

username = st.sidebar.text_input(
    "Enter Username"
)

# Create separate file for each user

FILE_NAME = f"{username}.csv"


# ------------------------------------------------
# File Handling
# ------------------------------------------------

if username != "":

    # Create CSV file if not exists

    if not os.path.exists(FILE_NAME):

        empty_df = pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Amount",
                "Description"
            ]
        )

        empty_df.to_csv(FILE_NAME, index=False)

    # Load Existing Data

    try:

        df = pd.read_csv(FILE_NAME)

    except:

        df = pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Amount",
                "Description"
            ]
        )

else:

    df = pd.DataFrame(
        columns=[
            "Date",
            "Category",
            "Amount",
            "Description"
        ]
    )


# ------------------------------------------------
# Sidebar Inputs
# ------------------------------------------------

expense_date = st.sidebar.date_input(
    "Date",
    datetime.today()
)

category = st.sidebar.selectbox(
    "Category",
    [
    "Food",
    "Transport",
    "Shopping",
    "Recharge & Bills",
    "Rent/Hostel Fee",
    "Entertainment",
    "Health",
    "Education",
    "Other"
]
)

amount = st.sidebar.number_input(
    "Amount",
    min_value=0.0,
    format="%.2f"
)

description = st.sidebar.text_input(
    "Description"
)



# ------------------------------------------------
# Add Expense Button
# ------------------------------------------------

if st.sidebar.button("Add Expense"):

    new_expense = pd.DataFrame({

        "Date": [expense_date],

        "Category": [category],

        "Amount": [amount],

        "Description": [description]
    })

    df = pd.concat(
        [df, new_expense],
        ignore_index=True
    )

    df.to_csv(FILE_NAME, index=False)

    st.sidebar.success(
        "Expense Added Successfully"
    )
    

# ------------------------------------------------
# Main Dashboard
# ------------------------------------------------

st.subheader("Expense Data")

st.dataframe(
    df,
    use_container_width=True
)
# ------------------------------------------------
# Delete Expense Entry
# ------------------------------------------------

st.subheader("Delete Expense Entry")

if not df.empty:

    # Select row number
    row_to_delete = st.number_input(
        "Enter Row Number to Delete",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="delete_row"
    )

    # Delete button
    if st.button("Delete Entry"):

        # Drop selected row
        df = df.drop(row_to_delete)

        # Reset index
        df = df.reset_index(drop=True)

        # Save updated data
        df.to_csv(FILE_NAME, index=False)

        st.success(
            "Entry Deleted Successfully"
        )

        # Refresh app
        st.rerun()
        # ------------------------------------------------
# Edit Expense Entry
# ------------------------------------------------

st.subheader("Edit Expense Entry")

if not df.empty:

    # Select row to edit
    row_to_edit = st.number_input(
        "Enter Row Number to Edit",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="edit_row"
    )

    # Current row data
    current_row = df.loc[row_to_edit]

    # Editable inputs
    new_category = st.selectbox(
        "Edit Category",
[
    "Food",
    "Transport",
    "Shopping",
    "Recharge & Bills",
    "Rent/Hostel Fee",
    "Entertainment",
    "Health",
    "Education",
    "Other"
],
        key="edit_category"
    )

    new_amount = st.number_input(
        "Edit Amount",
        min_value=0.0,
        value=float(current_row["Amount"]),
        key="edit_amount"
    )

    new_description = st.text_input(
        "Edit Description",
        value=str(current_row["Description"]),
        key="edit_description"
    )

    # Update button
    if st.button("Update Entry"):

        df.loc[row_to_edit, "Category"] = new_category

        df.loc[row_to_edit, "Amount"] = new_amount

        df.loc[row_to_edit, "Description"] = new_description

        # Save updated CSV
        df.to_csv(FILE_NAME, index=False)

        st.success(
            "Entry Updated Successfully"
        )

        # Refresh app
        st.rerun()
# ------------------------------------------------
# Analytics
# ------------------------------------------------

if not df.empty:

    # Total Expense

    total_expense = df["Amount"].sum()

    st.metric(
        "Total Expense",
        f"₹ {total_expense:.2f}"
    )

    # Category Summary

    category_summary = (

        df.groupby("Category")["Amount"]

        .sum()

        .reset_index()
    )

    # Pie Chart

    pie_chart = px.pie(

        category_summary,

        names="Category",

        values="Amount",

        title="Category-wise Expense Distribution"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    # Bar Chart

    bar_chart = px.bar(

        category_summary,

        x="Category",

        y="Amount",

        title="Expense Comparison by Category"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

    # ------------------------------------------------
    # Monthly Budget Management
    # ------------------------------------------------

    st.subheader("Monthly Budget Management")

    monthly_budget = st.number_input(
        "Enter Monthly Budget",
        min_value=0.0,
        value=10000.0,
        step=500.0
    )

    # Convert Date Column

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # Create Month Column

    df["Month"] = df["Date"].dt.strftime(
        "%B"
    )

    # Current Month

    current_month = datetime.today().strftime(
        "%B"
    )

    # Filter Current Month Data

    current_month_data = df[
        df["Month"] == current_month
    ]

    # Current Month Expense

    current_month_expense = (
        current_month_data["Amount"].sum()
    )

    # Metrics

    st.metric(
        "Current Month Expense",
        f"₹ {current_month_expense:.2f}"
    )

    st.metric(
        "Monthly Budget",
        f"₹ {monthly_budget:.2f}"
    )

    # Budget Logic

    if current_month_expense > monthly_budget:

        excess = (
            current_month_expense
            - monthly_budget
        )

        st.error(
            f"Budget Exceeded by ₹ {excess:.2f}"
        )

    elif current_month_expense >= (
        0.8 * monthly_budget
    ):

        remaining = (
            monthly_budget
            - current_month_expense
        )

        st.warning(
            f"Warning: Budget Near Limit. Remaining ₹ {remaining:.2f}"
        )

    else:

        remaining = (
            monthly_budget
            - current_month_expense
        )

        st.success(
            f"Budget Under Control. Remaining ₹ {remaining:.2f}"
        )

    # ------------------------------------------------
    # Monthly Trend Analysis
    # ------------------------------------------------

    monthly_summary = (

        df.groupby("Month")["Amount"]

        .sum()

        .reset_index()
    )

    line_chart = px.line(

        monthly_summary,

        x="Month",

        y="Amount",

        markers=True,

        title="Monthly Expense Trend"
    )

    st.plotly_chart(
        line_chart,
        use_container_width=True
    )

    # ------------------------------------------------
    # Download Report
    # ------------------------------------------------

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="Download CSV Report",

        data=csv,

        file_name="expense_report.csv",

        mime="text/csv"
    )

else:

    st.info(
        "No expenses added yet."
    )

# ------------------------------------------------
# Footer
# ------------------------------------------------

st.markdown("---")

st.caption(
    "Developed using Python, Streamlit, Pandas, and Plotly"
)