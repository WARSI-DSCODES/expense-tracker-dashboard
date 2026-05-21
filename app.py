import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
st.set_page_config(
    page_title=" FinTrack",
    page_icon="💸",
    layout="wide"
)

# Login Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
    # ------------------------------------------------
# Login / Register System
# ------------------------------------------------

if not st.session_state.logged_in:

    st.markdown("""
    <div style="
    text-align:center;
    padding:20px;
    ">

    <h1 style="
    color:#10B981;
    font-size:60px;
    font-weight:900;
    ">
    💸 FinTrack
    </h1>

    <h4 style="
    color:#94A3B8;
    ">
    Track • Save • Grow
    </h4>

    <p style="
    color:#CBD5E1;
    ">
    Smart Expense Tracking & Budget Management
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔐 Login / Register")

    tab1, tab2 = st.tabs(
        ["🔑 Login", "📝 Register"]
    )
    

    # ---------------- Login ----------------

    with tab1:

        login_user = st.text_input(
            "Username",
            key="login_user"
        )

        login_pass = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            users = pd.read_csv(
                "users.csv"
            )

            match = users[
                (users["username"] == login_user)
                &
                (users["password"] == login_pass)
            ]

            if not match.empty:

                st.session_state.logged_in = True

                st.session_state.username = (
                    login_user
                )

                st.success(
                    f"Welcome to FinTrack, {login_user}!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    # ---------------- Register ----------------

    with tab2:

        reg_user = st.text_input(
            "New Username"
        )

        reg_pass = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Register"):

            users = pd.read_csv(
                "users.csv"
            )

            if reg_user in users["username"].values:

                st.warning(
                    "Username already exists"
                )

            else:

                users.loc[len(users)] = [
                    reg_user,
                    reg_pass
                ]

                users.to_csv(
                    "users.csv",
                    index=False
                )

                st.success(
                    "FinTrack Account Created Successfully!"
                )

    st.stop()


st.markdown("""
<style>

[data-testid="stMetric"]{
background:#1e293b;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,.2);
}

.block-container{
padding-top:2rem;
}

</style>
""",
unsafe_allow_html=True)
# ------------------------------------------------
# Title
# ------------------------------------------------

st.markdown("""
<div style="
text-align:center;
padding:20px;
margin-bottom:20px;
">

<h1 style="
color:#10B981;
font-size:60px;
font-weight:900;
">
💸 FinTrack
</h1>

<h4 style="
color:#94A3B8;
">
Track • Save • Grow
</h4>

</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="
text-align:center;F
padding:10px;
margin-bottom:10px;
">

<h2 style="
color:#10B981;
font-size:32px;
font-weight:900;
margin-bottom:0px;
">
💸 FinTrack
</h2>

<p style="
color:#94A3B8;
font-size:13px;
margin-top:0px;
">
Track • Save • Grow
</p>

</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Dashboard",
        "📊 Analytics",
        "💰 Budget",
        "✏️ Manage Expenses",
        "👤 Profile"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success(
    f"👋 Welcome, {st.session_state.username}"
)

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.rerun()
# Create separate file for each user

FILE_NAME = (
    st.session_state.username
    + ".csv"
)


# ------------------------------------------------
# File Handling
# ------------------------------------------------

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

# ===== QUICK STATS START =====

if not df.empty:

    st.sidebar.markdown("---")

    st.sidebar.subheader("📊 Quick Stats")

    st.sidebar.metric(
        "Entries",
        len(df)
    )

    st.sidebar.metric(
        "Total Expense",
        f"₹{df['Amount'].sum():,.0f}"
    )

# ===== QUICK STATS END =====

st.sidebar.markdown("---")

st.sidebar.subheader("💸 Add Expense")

expense_date = st.sidebar.date_input(
    "📅 Date",
    datetime.today()
)

category = st.sidebar.selectbox(
    "🏷️ Category",
    [
        "🍔 Food",
        "🚌 Transport",
        "🛍️ Shopping",
        "📱 Recharge & Bills",
        "🏠 Rent/Hostel Fee",
        "🎬 Entertainment",
        "🏥 Health",
        "📚 Education",
        "📦 Other"
    ]
)

amount = st.sidebar.number_input(
    "💰 Amount (₹)",
    min_value=0.0,
    step=10.0,
    format="%.2f"
)

description = st.sidebar.text_area(
    "📝 Description",
    height=80
)

# ------------------------------------------------
# Add Expense Button
# ------------------------------------------------

if st.sidebar.button(
    "➕ Add Expense",
    use_container_width=True
):

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
        "Expense Added Successfully to FinTrack"
    )
    
def create_pdf_report(df, username):

    pdf_file = "FinTrack_Report.pdf"

    c = canvas.Canvas(
        pdf_file,
        pagesize=letter
    )

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawString(
        50,
        750,
        "FinTrack Expense Report"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        50,
        720,
        f"User: {username}"
    )

    c.drawString(
        50,
        700,
        f"Total Expense: ₹{df['Amount'].sum():,.2f}"
    )

    y = 660

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawString(50, y, "Date")
    c.drawString(130, y, "Category")
    c.drawString(260, y, "Amount")
    c.drawString(340, y, "Description")

    y -= 20

    c.setFont(
        "Helvetica",
        10
    )

    for _, row in df.iterrows():

        c.drawString(
            50,
            y,
            str(row["Date"])
        )

        c.drawString(
            130,
            y,
            str(row["Category"])
        )

        c.drawString(
            260,
            y,
            str(row["Amount"])
        )

        c.drawString(
            340,
            y,
            str(row["Description"])[:25]
        )

        y -= 18

        if y < 50:

            c.showPage()

            y = 750

    c.save()

    return pdf_file  
# ------------------------------------------------
# Main Dashboard
# ------------------------------------------------

if page == "🏠 Dashboard":

    if not df.empty:

        total_expense = df["Amount"].sum()

        current_month = datetime.today().strftime("%B")

        temp_df = df.copy()

        temp_df["Date"] = pd.to_datetime(
            temp_df["Date"]
        )

        temp_df["Month"] = (
            temp_df["Date"]
            .dt.strftime("%B")
        )

        current_month_expense = (
            temp_df[
                temp_df["Month"] == current_month
            ]["Amount"].sum()
        )

        top_category = (
            df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(f"""
            <div style="
            background:#2563EB;
            padding:20px;
            border-radius:15px;
            text-align:center;
            ">
            <h4 style="color:white;">
            💰 Total Expense
            </h4>
            <h2 style="color:white;">
            ₹{total_expense:,.0f}
            </h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div style="
            background:#10B981;
            padding:20px;
            border-radius:15px;
            text-align:center;
            ">
            <h4 style="color:white;">
            📅 This Month
            </h4>
            <h2 style="color:white;">
            ₹{current_month_expense:,.0f}
            </h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown(f"""
            <div style="
            background:#F59E0B;
            padding:20px;
            border-radius:15px;
            text-align:center;
            ">
            <h4 style="color:white;">
            🧾 Entries
            </h4>
            <h2 style="color:white;">
            {len(df)}
            </h2>
            </div>
            """, unsafe_allow_html=True)

        with col4:

            st.markdown(f"""
            <div style="
            background:#8B5CF6;
            padding:20px;
            border-radius:15px;
            text-align:center;
            ">
            <h4 style="color:white;">
            👤 User
            </h4>
            <h2 style="color:white;">
            {st.session_state.username}
            </h2>
            </div>
            """, unsafe_allow_html=True)

        # Top Category Card

        st.markdown(f"""
        <div style="
        background:#1E293B;
        padding:25px;
        border-radius:20px;
        margin-top:20px;
        margin-bottom:20px;
        ">
        <h4 style="color:#FBBF24;">
        🏆 Top Category
        </h4>
        <h1 style="color:white;">
        🍔 {top_category}
        </h1>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Expense Data")

        search_term = st.text_input(
            "🔍 Search Expense"
        )

        filtered_df = df.copy()

        if search_term:

            filtered_df = df[
                df.astype(str)
                .apply(
                    lambda row:
                    row.str.contains(
                        search_term,
                        case=False
                    ).any(),
                    axis=1
                )
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        # PDF Report Download

        pdf_file = create_pdf_report(
            df,
            st.session_state.username
        )

        with open(
            pdf_file,
            "rb"
        ) as pdf:

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name="FinTrack_Report.pdf",
                mime="application/pdf"
            )

    else:

        st.info(
            "No expenses recorded in FinTrack yet."
        )
if page == "✏️ Manage Expenses":

    st.header("✏️ Manage Expenses")

    # ==========================
    # Delete Expense Entry
    # ==========================

    st.subheader("🗑️ Delete Expense Entry")

    if not df.empty:

        row_to_delete = st.number_input(
            "Select Row Number",
            min_value=0,
            max_value=len(df)-1,
            step=1,
            key="delete_row"
        )

        if st.button("🗑️ Delete Entry"):

            df = df.drop(row_to_delete)

            df = df.reset_index(drop=True)

            df.to_csv(FILE_NAME, index=False)

            st.success(
                "Entry Deleted Successfully"
            )

            st.rerun()

    # ==========================
    # ==========================

    # Edit Section

    st.subheader("✏️ Edit Expense Entry")

    if not df.empty:

        row_to_edit = st.number_input(
        "Select Row To Edit",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="edit_row"
    )

    current_row = df.loc[row_to_edit]

    # Date

    new_date = st.date_input(
        "Date",
        value=pd.to_datetime(
            current_row["Date"]
        ),
        key="edit_date"
    )

    # Category

    categories = [
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

    new_category = st.selectbox(
        "Category",
        categories,
        index=(
            categories.index(
                current_row["Category"]
            )
            if current_row["Category"] in categories
            else 0
        ),
        key="edit_category"
    )

    # Amount

    new_amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        value=float(
            current_row["Amount"]
        ),
        key="edit_amount"
    )

    # Description

    new_description = st.text_input(
        "Description",
        value=str(
            current_row["Description"]
        ),
        key="edit_description"
    )

    # Update Button

    if st.button("💾 Update Entry"):

        df.loc[
    row_to_edit,
    "Date"
] = str(new_date)

        df.loc[
            row_to_edit,
            "Category"
        ] = new_category

        df.loc[
            row_to_edit,
            "Amount"
        ] = new_amount

        df.loc[
            row_to_edit,
            "Description"
        ] = new_description

        df.to_csv(
            FILE_NAME,
            index=False
        )

        st.success(
            "✅ Expense Updated Successfully in FinTrack"
        )

        st.rerun()

else:

    st.info(
        "No expense records available."
    )
# ------------------------------------------------
# Analytics
# ------------------------------------------------

if page == "📊 Analytics":

    st.header("📊 Analytics Dashboard")

    if not df.empty:

        temp_df = df.copy()

        temp_df["Date"] = pd.to_datetime(
            temp_df["Date"]
        )

        temp_df["Month"] = (
            temp_df["Date"]
            .dt.strftime("%B")
        )

        months = list(
            temp_df["Month"].unique()
        )

        selected_month = st.selectbox(
            "📅 Select Month",
            months,
            index=len(months)-1
        )

        filtered_df = temp_df[
            temp_df["Month"] == selected_month
        ]

        # Metrics

        total_expense = (
            filtered_df["Amount"].sum()
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💰 Total Expense",
                f"₹{total_expense:,.2f}"
            )

        with col2:
            st.metric(
                "🧾 Entries This Month",
                len(filtered_df)
            )

        # Category Summary

        category_summary = (
            filtered_df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        # Top Category

        if not category_summary.empty:

            highest = category_summary.loc[
                category_summary["Amount"].idxmax()
            ]

            st.success(
                f"🏆 Top Category: {highest['Category']} (₹{highest['Amount']:.0f})"
            )

        # Pie Chart

        pie_chart = px.pie(
            category_summary,
            names="Category",
            values="Amount",
            title=f"{selected_month} Expense Distribution"
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True,
            key="pie_chart_1"
        )

        # Bar Chart

        bar_chart = px.bar(
            category_summary,
            x="Category",
            y="Amount",
            title=f"{selected_month} Category Comparison"
        )

        st.plotly_chart(
            bar_chart,
            use_container_width=True,
            key="bar_chart_1"
        )

        # Monthly Trend

        monthly_summary = (
            temp_df.groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        # Month Comparison

        if len(monthly_summary) >= 2:

            current = monthly_summary.iloc[-1]["Amount"]

            previous = monthly_summary.iloc[-2]["Amount"]

            difference = (
                current - previous
            )

            st.metric(
                "📈 Month Change",
                f"₹{current:,.0f}",
                delta=f"₹{difference:,.0f}"
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
            use_container_width=True,
            key="line_chart_1"
        )

    else:

        st.info(
            "No expense data available."
        )
    
# ------------------------------------------------
# Monthly Budget Management
# ------------------------------------------------

if page == "💰 Budget":

    if not df.empty:

        temp_df = df.copy()

        temp_df["Date"] = pd.to_datetime(
            temp_df["Date"]
        )

        current_month = datetime.today().strftime(
            "%B"
        )

        temp_df["Month"] = (
            temp_df["Date"]
            .dt.strftime("%B")
        )

        current_month_expense = (
            temp_df[
                temp_df["Month"] == current_month
            ]["Amount"].sum()
        )

        st.subheader(
            "💰 Monthly Budget Management"
        )

        monthly_budget = st.number_input(
            "Enter Monthly Budget",
            min_value=0.0,
            value=10000.0,
            step=500.0
        )

        st.metric(
            "Current Month Expense",
            f"₹ {current_month_expense:.2f}"
        )

        st.metric(
            "Monthly Budget",
            f"₹ {monthly_budget:.2f}"
        )

        # Finance Score

        score = max(
            0,
            int(
                100 -
                (
                    current_month_expense /
                    max(monthly_budget, 1)
                ) * 100
            )
        )

        st.markdown(f"""
        <div style="
        background:linear-gradient(
        135deg,
        #10B981,
        #059669
        );
        padding:25px;
        border-radius:20px;
        text-align:center;
        margin-bottom:20px;
        ">

        <h3 style="color:white;">
        🏆 Financial Health Score
        </h3>

        <h1 style="
        color:white;
        font-size:50px;
        font-weight:900;
        ">
        {score}/100
        </h1>

        </div>
        """, unsafe_allow_html=True)

        health = min(
            100,
            int(
                (
                    current_month_expense /
                    max(monthly_budget, 1)
                ) * 100
            )
        )

        st.progress(
            health / 100
        )

        st.write(
            f"Budget Utilized: {health}%"
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

    else:

        st.info(
            "No expenses added yet."
        )
        # Smart Insights

        st.subheader("🤖 Smart Insights")

        category_summary = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        if not category_summary.empty:

            highest = category_summary.loc[
                category_summary["Amount"].idxmax()
            ]

            st.info(
                f"""
Highest Spending Category:
{highest['Category']}

Amount:
₹{highest['Amount']:.2f}
"""
            )

            if highest["Category"] == "Food":

                st.warning(
                    "🍔 Food expenses are relatively high."
                )

        # Monthly Trend Analysis

        if "Month" in temp_df.columns:

            monthly_summary = (
                temp_df.groupby("Month")["Amount"]
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
                use_container_width=True,
                key="budget_line_chart"
            )
            # Achievements

        st.subheader("🏆 Achievements")

        if len(df) >= 10:
            st.success("🥉 Expense Beginner")

        if len(df) >= 25:
            st.success("🥈 Consistent Tracker")

        if len(df) >= 50:
            st.success("🥇 Expense Master")

        if current_month_expense <= monthly_budget:
            st.success("💰 Budget Master")
        # Expense Prediction

        st.subheader("📈 Expense Prediction")

        predicted = (
            current_month_expense * 1.10
        )

        st.metric(
            "Next Month Prediction",
            f"₹{predicted:.2f}"
        )

        # Download Report

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="FinTrack_Report.csv",
            mime="text/csv"
        )


# ------------------------------------------------
# Profile
# ------------------------------------------------

if page == "👤 Profile":

    st.header("👤 User Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Lifetime Expense",
            f"₹{df['Amount'].sum():,.0f}"
        )

    with col2:
        st.metric(
            "🧾 Total Entries",
            len(df)
        )

    if not df.empty:

        top_category = (
            df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
        )

        st.metric(
            "🏆 Top Category",
            top_category
        )

    st.success(
        f"Welcome to FinTrack, {st.session_state.username}"
    )
# ------------------------------------------------
# Footer
# ------------------------------------------------

st.markdown("""
<hr>

<div style="
text-align:center;
padding:15px;
color:#94a3b8;
font-size:15px;
line-height:1.8;
">

<h3 style="color:#10B981;">
💸 FinTrack
</h3>

<p>
<b>Capstone Project - I</b>
</p>

<p>
🎓 Developed by IIT Patna BS Students
</p>

<p>
<b>Md Nafis Warsi</b><br>
<b>Saman Naaz</b><br>
<b>Ankur Namdev</b><br>
<b>Sayan Nandy</b>
</p>

<p style="font-size:13px;">
© 2026 FinTrack | Smart Expense Analysis & Budget Planning System
</p>

</div>
""", unsafe_allow_html=True)