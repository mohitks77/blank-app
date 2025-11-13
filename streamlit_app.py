import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# Page config
st.set_page_config(page_title="Power Potential Ranking", layout="wide")

colored_header(
    label="District-wise Power Potential Dashboard",
    description="Assign weights to factors and rank the best districts.",
    color_name="blue-70"
)

# Sidebar
st.sidebar.header("⚖️ Weight Adjustment Panel")

# List numeric factors
factors = df.select_dtypes(include=['number']).columns.tolist()
weights = {}

for col in factors:
    weights[col] = st.sidebar.slider(f"Weight for {col}", 0.0, 1.0, 0.3)

# Normalize weights
w_sum = sum(weights.values())
if w_sum == 0:
    st.error("Please set at least one non-zero weight.")
    st.stop()

norm_weights = {k: v / w_sum for k, v in weights.items()}

# Score calculation
score_df = df.copy()
score_df["score"] = 0
for col in factors:
    score_df["score"] += score_df[col] * norm_weights[col]

score_df = score_df.sort_values(by="score", ascending=False)

# UI Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏆 District Ranking Table")
    st.dataframe(score_df, use_container_width=True)

with col2:
    st.subheader("🥇 Top District")
    top = score_df.iloc[0]
    st.metric(label="Best District", value=top["district"], delta=f"Score: {top['score']:.3f}")
    style_metric_cards()

    st.markdown("### Normalized Weights Used")
    st.json(norm_weights)

st.markdown("---")
st.subheader("📊 Factor Influence Visualization (Coming Soon)")
