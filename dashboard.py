import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. SETUP & DATA CLEANING
sns.set_theme(style="whitegrid", palette="viridis")
df = pd.read_csv("data/sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df_sorted = df.sort_values("Date")

# 2. SEABORN STATISTICAL PLOTS (Box & Violin)
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.boxplot(x="Product", y="Price", data=df)
plt.title("Price Distribution by Product")
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.violinplot(x="Region", y="Quantity", data=df, inner="quart")
plt.title("Quantity Distribution by Region")
plt.tight_layout()
plt.savefig("visualizations/seaborn_plots.png")

# 3. CORRELATION HEATMAP
plt.figure(figsize=(8, 6))
corr = df[["Quantity", "Price", "Total_Sales"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Numerical Correlation Matrix")
plt.savefig("visualizations/correlation_heatmap.png")

# 4. MULTI-PLOT DASHBOARD (STATIC)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
sns.barplot(ax=axes[0, 0], x="Region", y="Total_Sales", data=df, estimator=sum)
sns.countplot(ax=axes[0, 1], x="Product", data=df)
sns.lineplot(ax=axes[1, 0], x="Date", y="Total_Sales", data=df_sorted)
sns.scatterplot(ax=axes[1, 1], x="Quantity", y="Total_Sales", hue="Product", data=df)
plt.tight_layout()
plt.savefig("visualizations/dashboard_static.png")

# 5. INTERACTIVE DASHBOARD (PLOTLY)
fig_dash = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Total Sales by Region",
        "Product Market Share",
        "Sales Trend",
        "Price vs Quantity",
    ),
    specs=[
        [{"type": "bar"}, {"type": "pie"}],
        [{"type": "scatter"}, {"type": "scatter"}],
    ],
)

# Adding Traces
region_sales = df.groupby("Region")["Total_Sales"].sum().reset_index()
fig_dash.add_trace(
    go.Bar(x=region_sales["Region"], y=region_sales["Total_Sales"], name="Region"),
    row=1,
    col=1,
)

product_sales = df.groupby("Product")["Total_Sales"].sum().reset_index()
fig_dash.add_trace(
    go.Pie(labels=product_sales["Product"], values=product_sales["Total_Sales"]),
    row=1,
    col=2,
)

fig_dash.add_trace(
    go.Scatter(
        x=df_sorted["Date"], y=df_sorted["Total_Sales"], mode="lines", name="Trend"
    ),
    row=2,
    col=1,
)

fig_dash.add_trace(
    go.Scatter(
        x=df["Price"],
        y=df["Quantity"],
        mode="markers",
        marker=dict(color=df["Total_Sales"]),
    ),
    row=2,
    col=2,
)

fig_dash.update_layout(height=800, title_text="Interactive Sales Performance Dashboard")
fig_dash.write_html("visualizations/interactive_dashboard.html")

print("All visualizations have been generated successfully.")
