import plotly.express as px
from data_processing import customers
import pandas as pd


def get_all_graphs(data):

    ########################################################################################
    ##################################### Sales Graphs #####################################
    ########################################################################################

    data.loc[:, "Month"] = data["Order.Date"].dt.to_period("M").astype(str)
    sales_by_month = data.groupby("Month").agg({"Sales": "sum"}).reset_index()

    sales_over_time_fig = px.line(
        sales_by_month,
        x="Month",
        y="Sales",
        labels={"Month": "Month", "Sales": "Total Sales"},
    )
    sales_over_time_fig.update_layout(
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="lightgray",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color="white"),
        margin=dict(l=10, r=10, t=0, b=10),
        autosize=True,
    )

    ########################################################################################
    ##################################### Profit Graphs ####################################
    ########################################################################################

    profit_by_month = data.groupby("Month").agg({"Profit": "sum"}).reset_index()

    profit_over_time_fig = px.line(
        profit_by_month,
        x="Month",
        y="Profit",
        labels={"Month": "Month", "Profit": "Total Profit"},
    )
    profit_over_time_fig.update_layout(
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color="white"),
        margin=dict(l=10, r=10, t=0, b=10),
    )

    ########################################################################################
    ############################ Sales Distribution Graphs #################################
    ########################################################################################

    # Sales distribution by category
    sales_category_fig = px.pie(
        data,
        names="Category",
        values="Sales",
        color_discrete_sequence=px.colors.sequential.dense,
    )
    sales_category_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin={"t": 0, "b": 0, "l": 10, "r": 10},
    )
    sales_category_fig.update_traces(
        textinfo="percent+label", textposition="inside", textfont=dict(color="black")
    )

    # Sales distribution by sub-category
    sales_subcategory_fig = px.pie(
        data,
        names="Sub-Category",
        values="Sales",
        title="Sales by Sub-Category",
    )
    sales_subcategory_fig.update_traces(textinfo="percent+label")

    ########################################################################################
    ################################## Shipping Graphs #####################################
    ########################################################################################

    shipping_costs_by_month = (
        data.groupby("Month").agg({"Shipping.Cost": "sum"}).reset_index()
    )
    shipping_costs_over_time_fig = px.line(
        shipping_costs_by_month,
        x="Month",
        y="Shipping.Cost",
        title="Shipping Cost Over Time",
    )
    shipping_costs_over_time_fig.update_layout(
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="lightgray",
            zeroline=False,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color="white"),
        margin=dict(l=10, r=10, t=50, b=10),
    )

    # Most used shipping mode
    shipping_mode_data = (
        data["Ship.Mode"]
        .value_counts(normalize=True)
        .reset_index()
        .rename(columns={"Ship.Mode": "Ship Mode", "proportion": "Percentage"})
        .sort_values("Percentage", ascending=True)
    )
    shipping_mode_data["Tick.Labels"] = shipping_mode_data["Ship Mode"].apply(
        lambda x: x.replace(" ", "<br>")
    )
    shipping_mode_fig = px.bar(
        shipping_mode_data,
        x="Percentage",
        y="Ship Mode",
        orientation="h",
    )
    shipping_mode_fig.update_traces(
        text=shipping_mode_data.apply(lambda row: f"{row['Percentage']:.1%}", axis=1),
        textposition="inside",
        textfont=dict(color="white"),
        marker_color="#656ef2",
        marker=dict(
            line=dict(width=0),
            color="#656ef2",
            cornerradius=10,
        ),
        # width=0.15,  # Make bars thinner
        hoverinfo="none",
    )
    shipping_mode_fig.update_layout(
        title=dict(
            text="Most Used Shipping Mode",
            x=0.5,
            font=dict(color="white", size=18),
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            showticklabels=True,
            tickvals=list(range(len(shipping_mode_data))),
            ticktext=shipping_mode_data["Tick.Labels"],
            showgrid=False,
            zeroline=False,
            ticklabelstandoff=10,
            tickfont=dict(color="white"),
        ),
        barmode="stack",
        bargap=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=10, r=30),
    )

    # Shipping comparion order share and cost share
    # Calculate total sales and total shipping costs per shipping mode
    aggregated_data = (
        data.groupby("Ship.Mode")
        .agg(
            Orders_per_Mode=("Order.ID", "count"),
            Shipping_Cost_per_Mode=("Shipping.Cost", "sum"),
        )
        .reset_index()
    )
    # Calculate proportions for sales and shipping costs
    aggregated_data["Order_Share"] = (
        aggregated_data["Orders_per_Mode"] / aggregated_data["Orders_per_Mode"].sum()
    )
    aggregated_data["Shipping_Cost_Share"] = (
        aggregated_data["Shipping_Cost_per_Mode"]
        / aggregated_data["Shipping_Cost_per_Mode"].sum()
    )

    # Melt data for a grouped bar chart
    melted_data = pd.melt(
        aggregated_data,
        id_vars=["Ship.Mode"],
        value_vars=["Order_Share", "Shipping_Cost_Share"],
        var_name="Metric",
        value_name="Proportion",
    )
    melted_data["Tick.Labels"] = melted_data["Ship.Mode"].apply(
        lambda x: x.replace(" ", "<br />")
    )

    melted_data["Metric"] = melted_data["Metric"].replace(
        {
            "Order_Share": "Share of Orders",
            "Shipping_Cost_Share": "Share of Shipping Costs",
        }
    )

    # Plot the grouped bar chart
    shipping_comparison_fig = px.bar(
        melted_data,
        x="Ship.Mode",
        y="Proportion",
        color="Metric",
        barmode="group",
        text=melted_data["Proportion"].apply(lambda x: f"{x:.1%}"),
    )

    # Customize the layout
    shipping_comparison_fig.update_traces(
        textposition="outside",
        textfont=dict(color="white"),
        marker_line_width=0,
    )

    # workaround to get a linebreak to the ticktext
    tick_vals = melted_data["Ship.Mode"].unique()
    tick_text = [label.replace(" ", "<br>") for label in tick_vals]

    shipping_comparison_fig.update_layout(
        title=None,
        xaxis=dict(
            title=None,
            tickangle=0,
            tickfont=dict(size=12, color="white"),
            tickvals=tick_vals,
            ticktext=tick_text,
        ),
        yaxis=dict(
            title=None,
            tickformat=".0%",
            tickfont=dict(size=12, color="white"),
            zeroline=False,
            gridcolor="lightgray",
        ),
        legend=dict(
            title=None,
            font=dict(size=12, color="white"),
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="left",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, l=10, r=10),
    )

    ########################################################################################
    ################################## Customer Graphs #####################################
    ########################################################################################

    # Customers per country
    customers_per_country = (
        data.groupby("Country")["Customer.ID"]
        .nunique()
        .reset_index(name="Customer Count")
    )

    customer_heatmap_fig = px.choropleth(
        customers_per_country,
        locations="Country",
        locationmode="country names",
        color="Customer Count",
        color_continuous_scale="sunset",
    )
    customer_heatmap_fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            bgcolor="rgba(0,0,0,0)",
            showland=True,
            landcolor="rgba(0,0,0,0)",
            showocean=True,
            oceancolor="rgba(0,0,0,0)",
            showlakes=True,
            lakecolor="rgba(0,0,0,0)",
        ),
        coloraxis_colorbar=dict(
            orientation="h",
            title=dict(
                text="Number of Customers",
                font=dict(color="white"),
                side="top",
            ),
            tickfont=dict(color="white"),
        ),
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Top cities by customer count
    customers_per_city = data.groupby("City").size().reset_index(name="Customer Count")
    top_cities = customers_per_city.nlargest(10, "Customer Count")

    customers_city_fig = px.bar(
        top_cities,
        x="City",
        y="Customer Count",
        title="Top 10 Cities by Number of Customers",
        text="Customer Count",
    )
    customers_city_fig.update_layout(xaxis_title="City", yaxis_title="Customer Count")

    ########################################################################################
    ################################### Product Graphs #####################################
    ########################################################################################

    # Top 10 products by sales
    top_products_fig = px.bar(
        data.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index(),
        x="Sales",
        y="Product Name",
        orientation="h",
        labels={"Sales": "Sales", "Product Name": "Product"},
        title="Top 10 Products by Sales",
    )
    top_products_fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return (
        sales_over_time_fig,
        sales_category_fig,
        sales_subcategory_fig,
        profit_over_time_fig,
        customer_heatmap_fig,
        customers_city_fig,
        top_products_fig,
        shipping_mode_fig,
        shipping_comparison_fig,
    )
