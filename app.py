"""
Local Food Wastage Management System
A professional Streamlit application for managing and analyzing food wastage data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Food Wastage Management System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit menu and footer only – NOT the header, to keep sidebar toggle accessible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Keep sidebar permanently expanded and visible */
    [data-testid="stSidebar"] {
        min-width: 270px !important;
        max-width: 270px !important;
        width: 270px !important;
        transform: none !important;
        visibility: visible !important;
        display: block !important;
    }
    /* Hide the collapse/expand arrow button so users cannot accidentally hide the sidebar */
    [data-testid="collapsedControl"],
    button[kind="header"],
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Main background */
    .stApp {
        background: #f0f7f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3d2b 0%, #2d6a4f 60%, #40916c 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #d8f3dc !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.9rem;
        font-weight: 500;
        padding: 6px 10px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.12);
    }

    /* Page title */
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1b4332;
        font-weight: 700;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .page-subtitle {
        color: #52796f;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 22px 24px;
        border-left: 5px solid;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.10);
    }
    .kpi-card.green  { border-color: #40916c; }
    .kpi-card.teal   { border-color: #52b788; }
    .kpi-card.lime   { border-color: #74c69d; }
    .kpi-card.olive  { border-color: #95d5b2; }
    .kpi-icon  { font-size: 2rem; margin-bottom: 6px; }
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: #1b4332; line-height: 1; }
    .kpi-label { font-size: 0.8rem; color: #74c69d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
    .kpi-delta { font-size: 0.82rem; color: #52796f; margin-top: 6px; }

    /* Section headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1b4332;
        margin: 1.5rem 0 0.8rem;
        padding-bottom: 8px;
        border-bottom: 2px solid #d8f3dc;
    }

    /* Data table styling */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* Success / Error banners */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #d8f3dc;
        border-radius: 8px;
        font-weight: 600;
        color: #1b4332;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #40916c, #2d6a4f);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #52b788, #40916c);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(64,145,108,0.35);
    }
    .stButton > button[kind="secondary"] {
        background: white;
        color: #40916c;
        border: 2px solid #40916c;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #74c69d;
        font-size: 0.78rem;
        border-top: 1px solid #d8f3dc;
    }

    /* Sidebar refresh button – high-visibility action button */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #f4a261, #e76f51) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 0.65rem 1.2rem !important;
        width: 100% !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 3px 10px rgba(231,111,81,0.45) !important;
        transition: all 0.22s ease !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #e9c46a, #f4a261) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(231,111,81,0.55) !important;
        color: #1a3d2b !important;
    }
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 6px rgba(231,111,81,0.4) !important;
    }


    .sidebar-logo {
        text-align: center;
        padding: 20px 10px 10px;
    }
    .sidebar-logo .logo-icon { font-size: 2.8rem; }
    .sidebar-logo .logo-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #d8f3dc;
        line-height: 1.2;
        margin-top: 6px;
    }
    .sidebar-logo .logo-sub {
        font-size: 0.7rem;
        color: #95d5b2;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 4px;
    }
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.15);
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    """Create and cache MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="amey",
            database="food_wastage_management",
            autocommit=True
        )
        return conn
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


def get_conn():
    """Get connection, reconnecting if needed."""
    conn = get_connection()
    if conn and not conn.is_connected():
        conn.reconnect(attempts=3, delay=1)
    return conn


def run_query(query, params=None):
    """Execute a SELECT query and return a DataFrame."""
    conn = get_conn()
    if conn is None:
        return pd.DataFrame()
    try:
        return pd.read_sql(query, conn, params=params)
    except Exception as e:
        st.error(f"Query error: {e}")
        return pd.DataFrame()


def execute_dml(query, params=None):
    """Execute INSERT / UPDATE / DELETE and return success flag."""
    conn = get_conn()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"Database error: {e}")
        return False


def get_distinct(table, column):
    """Return sorted distinct non-null values for a column as a list."""
    df = run_query(f"SELECT DISTINCT `{column}` FROM `{table}` WHERE `{column}` IS NOT NULL ORDER BY `{column}`")
    if df.empty:
        return []
    return df[column].tolist()


def get_provider_ids():
    """Return list of (Provider_ID, Name) tuples for dropdown."""
    df = run_query("SELECT Provider_ID, Name FROM providers ORDER BY Provider_ID")
    if df.empty:
        return []
    return [(int(r["Provider_ID"]), str(r["Name"])) for _, r in df.iterrows()]


def check_food_id_autoincrement():
    """Return True if Food_ID column is AUTO_INCREMENT."""
    df = run_query("""
        SELECT EXTRA FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'food_listings'
          AND COLUMN_NAME = 'Food_ID'
    """)
    if df.empty:
        return True  # assume auto-increment if can't check
    return "auto_increment" in str(df["EXTRA"].iloc[0]).lower()


# ─────────────────────────────────────────────
# HELPER – PLOTLY THEME
# ─────────────────────────────────────────────
GREEN_PALETTE = [
    "#1b4332", "#2d6a4f", "#40916c", "#52b788",
    "#74c69d", "#95d5b2", "#b7e4c7", "#d8f3dc"
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1b4332"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="#d8f3dc", borderwidth=1),
)


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">🌿</div>
        <div class="logo-title">Food Wastage<br>Management</div>
        <div class="logo-sub">Sustainability Platform</div>
    </div>
    <hr class="sidebar-divider">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "🥗 Food Listings",
            "📋 Claims Analysis",
            "📈 EDA Visualizations",
            "🔍 SQL Analysis",
            "✏️ CRUD Operations",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data"):
        st.cache_resource.clear()
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
    <div style="padding:12px 8px; font-size:0.72rem; color:#95d5b2; line-height:1.6;">
        🌱 Reducing food waste,<br>one connection at a time.<br><br>
        <b style="color:#d8f3dc;">LABMENTIX Internship</b><br>
        Data Analytics Project
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UTILITY: KPI CARD
# ─────────────────────────────────────────────
def kpi_card(icon, value, label, color="green", delta=""):
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE 1: DASHBOARD
# ─────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown('<div class="page-title">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time overview of the food wastage management network</div>', unsafe_allow_html=True)

    with st.spinner("Loading dashboard metrics..."):
        df_providers = run_query("SELECT COUNT(*) AS cnt FROM providers")
        df_receivers = run_query("SELECT COUNT(*) AS cnt FROM receivers")
        df_listings  = run_query("SELECT COUNT(*) AS cnt FROM food_listings")
        df_claims    = run_query("SELECT COUNT(*) AS cnt FROM claims")
        df_qty       = run_query("SELECT COALESCE(SUM(Quantity), 0) AS total FROM food_listings")
        df_pending   = run_query("SELECT COUNT(*) AS cnt FROM claims WHERE Status='Pending'")
        df_completed = run_query("SELECT COUNT(*) AS cnt FROM claims WHERE Status='Completed'")

    total_providers = int(df_providers["cnt"].iloc[0]) if not df_providers.empty else 0
    total_receivers = int(df_receivers["cnt"].iloc[0]) if not df_receivers.empty else 0
    total_listings  = int(df_listings["cnt"].iloc[0])  if not df_listings.empty  else 0
    total_claims    = int(df_claims["cnt"].iloc[0])    if not df_claims.empty    else 0
    total_qty       = int(df_qty["total"].iloc[0])     if not df_qty.empty       else 0
    pending_claims  = int(df_pending["cnt"].iloc[0])   if not df_pending.empty   else 0
    completed_claims= int(df_completed["cnt"].iloc[0]) if not df_completed.empty else 0

    # KPI row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("🏪", total_providers, "Total Providers", "green", "Restaurants, Hotels & More")
    with c2: kpi_card("🤝", total_receivers, "Total Receivers", "teal",  "NGOs, Shelters & Individuals")
    with c3: kpi_card("🥘", total_listings,  "Food Listings",   "lime",  "Active food available")
    with c4: kpi_card("📋", total_claims,    "Total Claims",    "olive", "All claim requests")

    st.markdown("")

    # KPI row 2
    c5, c6, c7, _ = st.columns(4)
    with c5: kpi_card("⚖️", f"{total_qty:,}", "Total Quantity (kg/units)", "green", "Cumulative food tracked")
    with c6: kpi_card("⏳", pending_claims,   "Pending Claims",            "teal",  "Awaiting action")
    with c7: kpi_card("✅", completed_claims, "Completed Claims",          "lime",  "Successfully fulfilled")

    # Charts row
    st.markdown('<div class="section-header">Overview Charts</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        df_city = run_query("""
            SELECT Location AS City, COUNT(*) AS Listings
            FROM food_listings GROUP BY Location ORDER BY Listings DESC LIMIT 8
        """)
        if not df_city.empty:
            fig = px.bar(df_city, x="Listings", y="City", orientation="h",
                         title="Top Cities by Food Listings",
                         color="Listings", color_continuous_scale=GREEN_PALETTE[::-1])
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        df_status = run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")
        if not df_status.empty:
            fig2 = px.pie(df_status, names="Status", values="Count",
                          title="Claim Status Breakdown",
                          color_discrete_sequence=GREEN_PALETTE)
            fig2.update_traces(textposition="inside", textinfo="percent+label")
            fig2.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

    # Recent listings
    st.markdown('<div class="section-header">Recent Food Listings</div>', unsafe_allow_html=True)
    df_recent = run_query("""
        SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type,
               Location, Food_Type, Meal_Type
        FROM food_listings ORDER BY Food_ID DESC LIMIT 10
    """)
    if not df_recent.empty:
        st.dataframe(df_recent, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# PAGE 2: FOOD LISTINGS
# ─────────────────────────────────────────────
elif page == "🥗 Food Listings":
    st.markdown('<div class="page-title">🥗 Food Listings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Browse, filter and export available food donations</div>', unsafe_allow_html=True)

    with st.spinner("Fetching food listings..."):
        df_all = run_query("""
            SELECT fl.Food_ID, fl.Food_Name, fl.Quantity, fl.Expiry_Date,
                   fl.Provider_ID, p.Name AS Provider_Name,
                   fl.Provider_Type, fl.Location, fl.Food_Type, fl.Meal_Type
            FROM food_listings fl
            LEFT JOIN providers p ON fl.Provider_ID = p.Provider_ID
        """)

    if df_all.empty:
        st.warning("No food listings found in the database.")
        st.stop()

    # Filter bar
    with st.container():
        fc1, fc2, fc3, fc4, fc5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
        with fc1:
            search = st.text_input("🔎 Search food name", placeholder="e.g. Rice, Bread...")
        with fc2:
            locations = ["All"] + sorted(df_all["Location"].dropna().unique().tolist())
            sel_loc = st.selectbox("📍 Location", locations)
        with fc3:
            food_types = ["All"] + sorted(df_all["Food_Type"].dropna().unique().tolist())
            sel_food = st.selectbox("🍽️ Food Type", food_types)
        with fc4:
            meal_types = ["All"] + sorted(df_all["Meal_Type"].dropna().unique().tolist())
            sel_meal = st.selectbox("🕐 Meal Type", meal_types)
        with fc5:
            prov_types = ["All"] + sorted(df_all["Provider_Type"].dropna().unique().tolist())
            sel_prov = st.selectbox("🏪 Provider Type", prov_types)

    # Apply filters
    df_filtered = df_all.copy()
    if search:
        df_filtered = df_filtered[df_filtered["Food_Name"].str.contains(search, case=False, na=False)]
    if sel_loc  != "All": df_filtered = df_filtered[df_filtered["Location"]     == sel_loc]
    if sel_food != "All": df_filtered = df_filtered[df_filtered["Food_Type"]    == sel_food]
    if sel_meal != "All": df_filtered = df_filtered[df_filtered["Meal_Type"]    == sel_meal]
    if sel_prov != "All": df_filtered = df_filtered[df_filtered["Provider_Type"]== sel_prov]

    st.markdown(f'<div class="page-subtitle">Showing <b>{len(df_filtered)}</b> of <b>{len(df_all)}</b> records</div>', unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    # Download
    csv_data = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"food_listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )


# ─────────────────────────────────────────────
# PAGE 3: CLAIMS ANALYSIS
# ─────────────────────────────────────────────
elif page == "📋 Claims Analysis":
    st.markdown('<div class="page-title">📋 Claims Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track and analyse claim activity across the network</div>', unsafe_allow_html=True)

    with st.spinner("Loading claims data..."):
        df_claims_all = run_query("""
            SELECT c.Claim_ID, c.Food_ID, fl.Food_Name,
                   c.Receiver_ID, r.Name AS Receiver_Name,
                   c.Status, c.Timestamp
            FROM claims c
            LEFT JOIN food_listings fl ON c.Food_ID   = fl.Food_ID
            LEFT JOIN receivers     r  ON c.Receiver_ID = r.Receiver_ID
        """)
        df_status_cnt = run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")

    if df_claims_all.empty:
        st.warning("No claims data found.")
        st.stop()

    # KPIs
    status_map = df_status_cnt.set_index("Status")["Count"].to_dict() if not df_status_cnt.empty else {}
    total_c    = df_claims_all.shape[0]
    pending_c  = status_map.get("Pending",   0)
    completed_c= status_map.get("Completed", 0)
    cancelled_c= status_map.get("Cancelled", 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("📋", total_c,     "Total Claims",     "green", "")
    with c2: kpi_card("⏳", pending_c,   "Pending",          "teal",  "Awaiting fulfilment")
    with c3: kpi_card("✅", completed_c, "Completed",        "lime",  "Successfully done")
    with c4: kpi_card("❌", cancelled_c, "Cancelled",        "olive", "")

    st.markdown("")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        if not df_status_cnt.empty:
            fig = px.bar(df_status_cnt, x="Status", y="Count",
                         title="Claims by Status",
                         color="Status",
                         color_discrete_sequence=GREEN_PALETTE)
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_top_recv = run_query("""
            SELECT r.Name AS Receiver, COUNT(c.Claim_ID) AS Claims
            FROM claims c JOIN receivers r ON c.Receiver_ID=r.Receiver_ID
            GROUP BY r.Name ORDER BY Claims DESC LIMIT 8
        """)
        if not df_top_recv.empty:
            fig2 = px.bar(df_top_recv, x="Claims", y="Receiver", orientation="h",
                          title="Top Receivers by Claims",
                          color="Claims", color_continuous_scale=GREEN_PALETTE[::-1])
            fig2.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

    # Timeline
    if "Timestamp" in df_claims_all.columns:
        df_time = df_claims_all.copy()
        df_time["Date"] = pd.to_datetime(df_time["Timestamp"]).dt.date
        df_timeline = df_time.groupby(["Date","Status"]).size().reset_index(name="Count")
        fig3 = px.line(df_timeline, x="Date", y="Count", color="Status",
                       title="Claims Over Time",
                       color_discrete_sequence=GREEN_PALETTE)
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">All Claims</div>', unsafe_allow_html=True)
    st.dataframe(df_claims_all, use_container_width=True, hide_index=True)

    csv_data = df_claims_all.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Claims CSV", csv_data,
                       f"claims_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "text/csv")


# ─────────────────────────────────────────────
# PAGE 4: EDA VISUALIZATIONS
# ─────────────────────────────────────────────
elif page == "📈 EDA Visualizations":
    st.markdown('<div class="page-title">📈 EDA Visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Interactive exploratory analysis of the food network dataset</div>', unsafe_allow_html=True)

    with st.spinner("Building visualizations..."):
        df_food_type    = run_query("SELECT Food_Type, COUNT(*) AS Count FROM food_listings GROUP BY Food_Type")
        df_meal_type    = run_query("SELECT Meal_Type, COUNT(*) AS Count FROM food_listings GROUP BY Meal_Type")
        df_claim_status = run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")
        df_city_list    = run_query("SELECT Location AS City, COUNT(*) AS Count FROM food_listings GROUP BY Location ORDER BY Count DESC LIMIT 10")
        df_top_prov     = run_query("SELECT p.Name AS Provider, SUM(fl.Quantity) AS Total_Qty FROM food_listings fl JOIN providers p ON fl.Provider_ID=p.Provider_ID GROUP BY p.Name ORDER BY Total_Qty DESC LIMIT 10")
        df_prov_type    = run_query("SELECT Type AS Provider_Type, COUNT(*) AS Count FROM providers GROUP BY Type")
        df_city_prov    = run_query("SELECT City, COUNT(*) AS Providers FROM providers GROUP BY City ORDER BY Providers DESC LIMIT 10")

    row1c1, row1c2 = st.columns(2)

    with row1c1:
        st.markdown("##### 🍽️ Food Type Distribution")
        if not df_food_type.empty:
            fig = px.pie(df_food_type, names="Food_Type", values="Count",
                         color_discrete_sequence=GREEN_PALETTE, hole=0.4)
            fig.update_layout(**PLOTLY_LAYOUT, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

    with row1c2:
        st.markdown("##### 🕐 Meal Type Distribution")
        if not df_meal_type.empty:
            fig2 = px.bar(df_meal_type, x="Meal_Type", y="Count",
                          color="Meal_Type", color_discrete_sequence=GREEN_PALETTE,
                          text="Count")
            fig2.update_traces(textposition="outside")
            fig2.update_layout(**PLOTLY_LAYOUT, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    row2c1, row2c2 = st.columns(2)

    with row2c1:
        st.markdown("##### 📋 Claim Status Distribution")
        if not df_claim_status.empty:
            fig3 = px.pie(df_claim_status, names="Status", values="Count",
                          color_discrete_sequence=GREEN_PALETTE, hole=0.35)
            fig3.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)

    with row2c2:
        st.markdown("##### 🏙️ Top Cities by Food Listings")
        if not df_city_list.empty:
            fig4 = px.bar(df_city_list, x="Count", y="City", orientation="h",
                          color="Count", color_continuous_scale=GREEN_PALETTE[::-1],
                          text="Count")
            fig4.update_traces(textposition="outside")
            fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)

    row3c1, row3c2 = st.columns(2)

    with row3c1:
        st.markdown("##### 🏆 Top Providers by Quantity Donated")
        if not df_top_prov.empty:
            fig5 = px.bar(df_top_prov, x="Total_Qty", y="Provider", orientation="h",
                          color="Total_Qty", color_continuous_scale=GREEN_PALETTE[::-1],
                          text="Total_Qty")
            fig5.update_traces(textposition="outside")
            fig5.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig5, use_container_width=True)

    with row3c2:
        st.markdown("##### 🏪 Provider Type Distribution")
        if not df_prov_type.empty:
            fig6 = px.pie(df_prov_type, names="Provider_Type", values="Count",
                          color_discrete_sequence=GREEN_PALETTE)
            fig6.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig6, use_container_width=True)

    st.markdown("##### 🌆 City-wise Provider Distribution")
    if not df_city_prov.empty:
        fig7 = px.bar(df_city_prov, x="City", y="Providers",
                      color="Providers", color_continuous_scale=GREEN_PALETTE[::-1],
                      text="Providers")
        fig7.update_traces(textposition="outside")
        fig7.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig7, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE 5: SQL ANALYSIS
# ─────────────────────────────────────────────
elif page == "🔍 SQL Analysis":
    st.markdown('<div class="page-title">🔍 SQL Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Deep-dive analytical queries on the food network database</div>', unsafe_allow_html=True)

    analyses = [
        ("🏙️ Providers by City",
         "SELECT City, COUNT(*) AS Provider_Count FROM providers GROUP BY City ORDER BY Provider_Count DESC"),

        ("🤝 Receivers by City",
         "SELECT City, COUNT(*) AS Receiver_Count FROM receivers GROUP BY City ORDER BY Receiver_Count DESC"),

        ("🏪 Provider Type Contribution",
         "SELECT Type AS Provider_Type, COUNT(*) AS Count, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM providers),2) AS Percentage FROM providers GROUP BY Type"),

        ("📞 Provider Contacts by City",
         "SELECT City, Name, Contact FROM providers ORDER BY City"),

        ("🏆 Top Receivers by Total Claims",
         "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims FROM receivers r LEFT JOIN claims c ON r.Receiver_ID=c.Receiver_ID GROUP BY r.Name, r.Type ORDER BY Total_Claims DESC LIMIT 10"),

        ("⚖️ Total Food Quantity Available",
         "SELECT SUM(Quantity) AS Total_Quantity, AVG(Quantity) AS Avg_Quantity, MAX(Quantity) AS Max_Quantity, MIN(Quantity) AS Min_Quantity FROM food_listings"),

        ("🏙️ City with Highest Listings",
         "SELECT Location AS City, COUNT(*) AS Listings, SUM(Quantity) AS Total_Qty FROM food_listings GROUP BY Location ORDER BY Listings DESC LIMIT 5"),

        ("🍽️ Food Type Distribution",
         "SELECT Food_Type, COUNT(*) AS Count, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM food_listings),2) AS Percentage FROM food_listings GROUP BY Food_Type ORDER BY Count DESC"),

        ("📋 Claims per Food Item",
         "SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Total_Claims, SUM(CASE WHEN c.Status='Completed' THEN 1 ELSE 0 END) AS Completed FROM food_listings fl LEFT JOIN claims c ON fl.Food_ID=c.Food_ID GROUP BY fl.Food_Name ORDER BY Total_Claims DESC LIMIT 10"),

        ("🥇 Provider with Highest Successful Claims",
         "SELECT p.Name AS Provider, p.Type, COUNT(c.Claim_ID) AS Successful_Claims FROM providers p JOIN food_listings fl ON p.Provider_ID=fl.Provider_ID JOIN claims c ON fl.Food_ID=c.Food_ID WHERE c.Status='Completed' GROUP BY p.Name, p.Type ORDER BY Successful_Claims DESC LIMIT 10"),

        ("📊 Claim Status Percentages",
         "SELECT Status, COUNT(*) AS Count, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS Percentage FROM claims GROUP BY Status"),

        ("📐 Average Quantity Claimed",
         "SELECT AVG(fl.Quantity) AS Avg_Qty_Claimed FROM food_listings fl JOIN claims c ON fl.Food_ID=c.Food_ID WHERE c.Status='Completed'"),

        ("🕐 Most Claimed Meal Type",
         "SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Times_Claimed FROM food_listings fl JOIN claims c ON fl.Food_ID=c.Food_ID GROUP BY fl.Meal_Type ORDER BY Times_Claimed DESC"),

        ("📦 Quantity Donated by Provider",
         "SELECT p.Name AS Provider, p.Type, SUM(fl.Quantity) AS Total_Donated FROM providers p JOIN food_listings fl ON p.Provider_ID=fl.Provider_ID GROUP BY p.Name, p.Type ORDER BY Total_Donated DESC LIMIT 10"),

        ("⏰ Expiring Food Items (Next 7 Days)",
         "SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location, Food_Type FROM food_listings WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY) ORDER BY Expiry_Date ASC"),
    ]

    for title, query in analyses:
        with st.expander(title):
            if title == "⏰ Expiring Food Items (Next 7 Days)":
                df = run_query(query)
                if not df.empty:
                    st.success(f"✅ {len(df)} food item(s) expiring within the next 7 days.")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download", csv,
                        "Expiring_Food_Items_Next_7_Days.csv", "text/csv",
                        key="dl_expiring_7days")
                else:
                    st.info("ℹ️ No food items are expiring within the next 7 days.")
                    st.markdown("**📋 Fallback: Top 20 Earliest Expiring Food Items**")
                    df_fallback = run_query(
                        "SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location, Food_Type "
                        "FROM food_listings ORDER BY Expiry_Date ASC LIMIT 20"
                    )
                    if not df_fallback.empty:
                        st.dataframe(df_fallback, use_container_width=True, hide_index=True)
                        csv_fb = df_fallback.to_csv(index=False).encode("utf-8")
                        st.download_button("⬇️ Download Fallback", csv_fb,
                            "Top20_Earliest_Expiring.csv", "text/csv",
                            key="dl_expiring_fallback")
                    else:
                        st.warning("No food listings found in the database.")
            else:
                df = run_query(query)
                if not df.empty:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        f"⬇️ Download",
                        csv,
                        f"{title.replace(' ','_').replace('(','').replace(')','')}.csv",
                        "text/csv",
                        key=f"dl_{title}"
                    )
                else:
                    st.info("No data returned for this query.")


# ─────────────────────────────────────────────
# PAGE 6: CRUD OPERATIONS
# ─────────────────────────────────────────────
elif page == "✏️ CRUD Operations":
    st.markdown('<div class="page-title">✏️ CRUD Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add, update, or remove food listings from the database</div>', unsafe_allow_html=True)

    crud_tab1, crud_tab2, crud_tab3, crud_tab4 = st.tabs(
        ["📖 View All", "➕ Add Listing", "✏️ Update Listing", "🗑️ Delete Listing"]
    )

    # ── TAB 1: VIEW ──────────────────────────────────────────
    with crud_tab1:
        df_view = run_query("SELECT * FROM food_listings ORDER BY Food_ID DESC")
        if not df_view.empty:
            st.dataframe(df_view, use_container_width=True, hide_index=True)
            csv = df_view.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download as CSV", csv, "food_listings.csv", "text/csv")
        else:
            st.info("No food listings found.")

    # ── TAB 2: ADD ──────────────────────────────────────────
    with crud_tab2:
        st.markdown('<div class="section-header">Add New Food Listing</div>', unsafe_allow_html=True)

        # Load dynamic options from DB
        db_provider_type = get_distinct("food_listings", "Provider_Type") or \
            ["Restaurant", "Hotel", "Supermarket", "Household", "Event", "NGO", "Other"]
        db_food_type = get_distinct("food_listings", "Food_Type") or \
            ["Veg", "Non-Veg", "Vegan", "Jain", "Gluten-Free"]
        db_meal_type = get_distinct("food_listings", "Meal_Type") or \
            ["Breakfast", "Lunch", "Dinner", "Snack", "Any"]
        provider_rows = get_provider_ids()
        food_id_is_auto = check_food_id_autoincrement()

        with st.form("add_form", clear_on_submit=True):
            ac1, ac2 = st.columns(2)
            with ac1:
                food_name   = st.text_input("🍽️ Food Name *", placeholder="e.g. Biryani")
                quantity    = st.number_input("⚖️ Quantity *", min_value=1, step=1, value=10)
                expiry_date = st.date_input("📅 Expiry Date *", value=date.today())
                if not food_id_is_auto:
                    manual_food_id = st.number_input("🆔 Food ID *", min_value=1, step=1, value=1)
                if provider_rows:
                    prov_labels = [f"{pid} – {name}" for pid, name in provider_rows]
                    sel_prov_label = st.selectbox("🏪 Provider *", prov_labels)
                    provider_id = provider_rows[prov_labels.index(sel_prov_label)][0]
                else:
                    provider_id = st.number_input("🏪 Provider ID *", min_value=1, step=1, value=1)
            with ac2:
                provider_type = st.selectbox("🏷️ Provider Type *", db_provider_type)
                location      = st.text_input("📍 Location *", placeholder="e.g. Pune")
                food_type     = st.selectbox("🍲 Food Type *", db_food_type)
                meal_type     = st.selectbox("🕐 Meal Type *", db_meal_type)

            submitted = st.form_submit_button("➕ Add Food Listing", use_container_width=True)
            if submitted:
                if not food_name or not location:
                    st.error("Please fill in all required fields.")
                else:
                    if food_id_is_auto:
                        ok = execute_dml(
                            """INSERT INTO food_listings
                               (Food_Name, Quantity, Expiry_Date, Provider_ID,
                                Provider_Type, Location, Food_Type, Meal_Type)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (food_name, quantity, expiry_date, provider_id,
                             provider_type, location, food_type, meal_type)
                        )
                    else:
                        ok = execute_dml(
                            """INSERT INTO food_listings
                               (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID,
                                Provider_Type, Location, Food_Type, Meal_Type)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (manual_food_id, food_name, quantity, expiry_date, provider_id,
                             provider_type, location, food_type, meal_type)
                        )
                    if ok:
                        st.success(f"✅ Food listing **{food_name}** added successfully!")
                    else:
                        st.error("Failed to add food listing. Check Provider ID exists or Food ID is not a duplicate.")

    # ── TAB 3: UPDATE ────────────────────────────────────────
    with crud_tab3:
        st.markdown('<div class="section-header">Update Food Listing</div>', unsafe_allow_html=True)

        df_ids = run_query("SELECT Food_ID, Food_Name FROM food_listings ORDER BY Food_ID DESC")
        if df_ids.empty:
            st.info("No listings available to update.")
        else:
            id_options = {f"{row['Food_ID']} – {row['Food_Name']}": row["Food_ID"]
                          for _, row in df_ids.iterrows()}
            selected_label = st.selectbox("Select Food Listing to Update", list(id_options.keys()))
            selected_id    = id_options[selected_label]

            df_current = run_query("SELECT * FROM food_listings WHERE Food_ID=%s", (selected_id,))

            if not df_current.empty:
                row = df_current.iloc[0]

                # Load dynamic options
                upd_ptype_opts = get_distinct("food_listings", "Provider_Type") or \
                    ["Restaurant","Hotel","Supermarket","Household","Event","NGO","Other"]
                upd_ftype_opts = get_distinct("food_listings", "Food_Type") or \
                    ["Veg","Non-Veg","Vegan","Jain","Gluten-Free"]
                upd_mtype_opts = get_distinct("food_listings", "Meal_Type") or \
                    ["Breakfast","Lunch","Dinner","Snack","Any"]
                upd_provider_rows = get_provider_ids()

                with st.form("update_form"):
                    uc1, uc2 = st.columns(2)
                    with uc1:
                        u_food_name   = st.text_input("🍽️ Food Name",   value=str(row["Food_Name"]))
                        u_quantity    = st.number_input("⚖️ Quantity",   min_value=1, step=1,
                                                        value=int(row["Quantity"]))
                        u_expiry      = st.date_input("📅 Expiry Date",
                                                      value=row["Expiry_Date"] if isinstance(row["Expiry_Date"], date)
                                                      else date.today())
                        if upd_provider_rows:
                            upd_prov_labels = [f"{pid} – {name}" for pid, name in upd_provider_rows]
                            cur_pid = int(row["Provider_ID"])
                            cur_prov_idx = next((i for i, (pid, _) in enumerate(upd_provider_rows) if pid == cur_pid), 0)
                            sel_upd_prov = st.selectbox("🏪 Provider *", upd_prov_labels, index=cur_prov_idx)
                            u_provider_id = upd_provider_rows[upd_prov_labels.index(sel_upd_prov)][0]
                        else:
                            u_provider_id = st.number_input("🏪 Provider ID", min_value=1, step=1,
                                                            value=int(row["Provider_ID"]))
                    with uc2:
                        u_prov_type = st.selectbox("🏷️ Provider Type", upd_ptype_opts,
                                                   index=upd_ptype_opts.index(row["Provider_Type"])
                                                   if row["Provider_Type"] in upd_ptype_opts else 0)
                        u_location  = st.text_input("📍 Location", value=str(row["Location"]))
                        u_food_type = st.selectbox("🍲 Food Type", upd_ftype_opts,
                                                   index=upd_ftype_opts.index(row["Food_Type"])
                                                   if row["Food_Type"] in upd_ftype_opts else 0)
                        u_meal_type = st.selectbox("🕐 Meal Type", upd_mtype_opts,
                                                   index=upd_mtype_opts.index(row["Meal_Type"])
                                                   if row["Meal_Type"] in upd_mtype_opts else 0)

                    upd_btn = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    if upd_btn:
                        ok = execute_dml(
                            """UPDATE food_listings SET
                               Food_Name=%s, Quantity=%s, Expiry_Date=%s, Provider_ID=%s,
                               Provider_Type=%s, Location=%s, Food_Type=%s, Meal_Type=%s
                               WHERE Food_ID=%s""",
                            (u_food_name, u_quantity, u_expiry, u_provider_id,
                             u_prov_type, u_location, u_food_type, u_meal_type, selected_id)
                        )
                        if ok:
                            st.success(f"✅ Food listing #{selected_id} updated successfully!")
                        else:
                            st.error("Update failed.")

    # ── TAB 4: DELETE ────────────────────────────────────────
    with crud_tab4:
        st.markdown('<div class="section-header">Delete Food Listing</div>', unsafe_allow_html=True)
        st.warning("⚠️ Deletion is permanent and cannot be undone.")

        df_del_ids = run_query("SELECT Food_ID, Food_Name, Location FROM food_listings ORDER BY Food_ID DESC")
        if df_del_ids.empty:
            st.info("No listings found.")
        else:
            del_opts = {f"{r['Food_ID']} – {r['Food_Name']} ({r['Location']})": r["Food_ID"]
                        for _, r in df_del_ids.iterrows()}
            del_label = st.selectbox("Select Listing to Delete", list(del_opts.keys()))
            del_id    = del_opts[del_label]

            # Preview
            df_preview = run_query("SELECT * FROM food_listings WHERE Food_ID=%s", (del_id,))
            if not df_preview.empty:
                st.dataframe(df_preview, use_container_width=True, hide_index=True)

            confirm = st.checkbox(f"I confirm deletion of Food Listing #{del_id}")
            if st.button("🗑️ Delete", disabled=not confirm):
                ok = execute_dml("DELETE FROM food_listings WHERE Food_ID=%s", (del_id,))
                if ok:
                    st.success(f"✅ Food Listing #{del_id} deleted successfully!")
                    st.rerun()
                else:
                    st.error("Deletion failed. This listing may have active claims.")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    © 2026 Amey Sawatkar | Local Food Wastage Management System | LABMENTIX Internship
</div>
""", unsafe_allow_html=True)

