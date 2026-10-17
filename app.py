from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Used-Car Market Intelligence", page_icon="🚗", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "used_car_listings.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["manufacturing_year"] = pd.to_numeric(data["manufacturing_year"], errors="coerce")
    data["listed_price_inr"] = pd.to_numeric(data["listed_price_inr"], errors="coerce")
    data["kilometres_driven"] = pd.to_numeric(data["kilometres_driven"], errors="coerce")
    return data.dropna(subset=["listed_price_inr", "kilometres_driven"])

df = load_data()

st.title("🚗 Used-Car Market Intelligence")
st.caption("Business Analyst portfolio project | Pricing, inventory, and listing performance")
st.info("Dataset note: This project uses synthetic demonstration data, not verified live marketplace listings. Treat findings as practice analysis, not real market estimates.")

with st.sidebar:
    st.header("Filters")
    cities = st.multiselect("City", sorted(df["city"].unique()), default=sorted(df["city"].unique()))
    brands = st.multiselect("Brand", sorted(df["brand"].unique()), default=sorted(df["brand"].unique()))
    fuels = st.multiselect("Fuel type", sorted(df["fuel_type"].unique()), default=sorted(df["fuel_type"].unique()))
    statuses = st.multiselect("Listing status", sorted(df["listing_status"].unique()), default=sorted(df["listing_status"].unique()))
    age_range = st.slider("Vehicle age (years)", int(df["vehicle_age_years"].min()), int(df["vehicle_age_years"].max()),
                          (int(df["vehicle_age_years"].min()), int(df["vehicle_age_years"].max())))
    price_cap = st.slider("Maximum listed price (₹ lakh)", 1, 50, 50)

filtered = df[
    df["city"].isin(cities) &
    df["brand"].isin(brands) &
    df["fuel_type"].isin(fuels) &
    df["listing_status"].isin(statuses) &
    df["vehicle_age_years"].between(age_range[0], age_range[1]) &
    (df["listed_price_inr"] <= price_cap * 100000)
].copy()

if filtered.empty:
    st.warning("No listings match these filters. Adjust the filters in the sidebar.")
    st.stop()

total_listings = len(filtered)
avg_price = filtered["listed_price_inr"].mean()
median_price = filtered["listed_price_inr"].median()
sold_share = (filtered["listing_status"].eq("Sold").mean() * 100)
avg_km = filtered["kilometres_driven"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Listings analyzed", f"{total_listings:,}")
c2.metric("Average listed price", f"₹{avg_price/100000:.2f} lakh")
c3.metric("Median listed price", f"₹{median_price/100000:.2f} lakh")
c4.metric("Sold share in sample", f"{sold_share:.1f}%")

tab1, tab2, tab3, tab4 = st.tabs(["Market overview", "Pricing drivers", "Inventory & sales", "Data explorer"])

with tab1:
    left, right = st.columns(2)
    brand_stats = filtered.groupby("brand", as_index=False).agg(
        average_price=("listed_price_inr", "mean"), listings=("listing_id", "count"))
    brand_stats["average_price_lakh"] = brand_stats["average_price"] / 100000
    left.plotly_chart(px.bar(brand_stats.sort_values("listings", ascending=False), x="brand", y="listings",
                             title="Listings by brand", labels={"brand":"Brand","listings":"Listings"}), use_container_width=True)
    city_stats = filtered.groupby("city", as_index=False).agg(average_price=("listed_price_inr", "mean"), listings=("listing_id", "count"))
    city_stats["average_price_lakh"] = city_stats["average_price"] / 100000
    right.plotly_chart(px.bar(city_stats.sort_values("average_price_lakh", ascending=False), x="city", y="average_price_lakh",
                              title="Average listed price by city", labels={"city":"City","average_price_lakh":"Average price (₹ lakh)"}),
                       use_container_width=True)
    seg = filtered.groupby("vehicle_segment", as_index=False).agg(listings=("listing_id","count"), average_price=("listed_price_inr","mean"))
    seg["average_price_lakh"] = seg["average_price"] / 100000
    st.plotly_chart(px.pie(seg, names="vehicle_segment", values="listings", title="Listing mix by vehicle segment"), use_container_width=True)

with tab2:
    left, right = st.columns(2)
    left.plotly_chart(px.scatter(filtered, x="vehicle_age_years", y="listed_price_inr", color="vehicle_segment",
                                 hover_data=["brand","model","city"], title="Vehicle age vs listed price",
                                 labels={"vehicle_age_years":"Vehicle age (years)","listed_price_inr":"Listed price (₹)"}),
                      use_container_width=True)
    right.plotly_chart(px.scatter(filtered, x="kilometres_driven", y="listed_price_inr", color="fuel_type",
                                  hover_data=["brand","model","vehicle_age_years"], title="Kilometres driven vs listed price",
                                  labels={"kilometres_driven":"Kilometres driven","listed_price_inr":"Listed price (₹)"}),
                       use_container_width=True)
    fuel_stats = filtered.groupby("fuel_type", as_index=False).agg(average_price=("listed_price_inr","mean"), listings=("listing_id","count"))
    fuel_stats["average_price_lakh"] = fuel_stats["average_price"] / 100000
    st.plotly_chart(px.bar(fuel_stats, x="fuel_type", y="average_price_lakh", title="Average listed price by fuel type",
                           labels={"fuel_type":"Fuel type","average_price_lakh":"Average price (₹ lakh)"}), use_container_width=True)

with tab3:
    left, right = st.columns(2)
    status_stats = filtered.groupby("listing_status", as_index=False).size().rename(columns={"size":"listings"})
    left.plotly_chart(px.pie(status_stats, names="listing_status", values="listings", title="Available vs sold listings"), use_container_width=True)
    sold = filtered[filtered["listing_status"] == "Sold"]
    if not sold.empty:
        right.plotly_chart(px.histogram(sold, x="days_listed", nbins=20, title="Days listed before sold (sample)",
                                        labels={"days_listed":"Days listed"}), use_container_width=True)
    else:
        right.info("No sold listings in this filter selection.")
    st.markdown("#### Brand inventory snapshot")
    inv = filtered.groupby(["brand","listing_status"], as_index=False).size().rename(columns={"size":"listings"})
    st.dataframe(inv.sort_values("listings", ascending=False), use_container_width=True, hide_index=True)

with tab4:
    st.markdown("#### Filtered listing records")
    st.dataframe(filtered.sort_values("listed_price_inr", ascending=False), use_container_width=True, hide_index=True)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_used_car_listings.csv", mime="text/csv")

st.divider()
st.subheader("Automated business observations")
observations = []
top_brand = filtered["brand"].value_counts()
if not top_brand.empty:
    observations.append(f"**Largest listing count:** {top_brand.index[0]} has {int(top_brand.iloc[0])} listings in the current selection.")
older = filtered[filtered["vehicle_age_years"] >= 8]
newer = filtered[filtered["vehicle_age_years"] <= 3]
if not older.empty and not newer.empty:
    observations.append(f"**Age-price comparison:** vehicles aged 8+ years average ₹{older['listed_price_inr'].mean()/100000:.2f} lakh; vehicles aged 0–3 years average ₹{newer['listed_price_inr'].mean()/100000:.2f} lakh.")
top_city = filtered.groupby("city")["listed_price_inr"].mean().sort_values(ascending=False)
if len(top_city) >= 2:
    observations.append(f"**City price spread:** {top_city.index[0]} has the highest average listed price and {top_city.index[-1]} the lowest among the selected cities.")
if observations:
    for item in observations:
        st.markdown(f"- {item}")
st.caption("Interpretation reminder: listings and sold status are simulated. Validate recommendations against real marketplace, transaction, and demand data before making commercial decisions.")
