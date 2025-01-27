import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from graphs import get_all_graphs
from data_processing import merged_data

# Get graphs for the initial data
(
    sales_over_time_fig,
    sales_category_fig,
    sales_subcategory_fig,
    profit_over_time_fig,
    customer_heatmap_fig,
    customer_city_fig,
    top_products_fig,
    shipping_mode_fig,
    shipping_comparison_fig,
) = get_all_graphs(merged_data)

# Create a list of countries for the dropdown
country_options = [
    {"label": country, "value": country} for country in merged_data["Country"].unique()
]

# Create a list of categories for the dropdown
category_options = [
    {"label": category, "value": category}
    for category in merged_data["Category"].unique()
]

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)
app.title = "E-commerce Sales Analytics Dashboard"

# Layout
app.layout = html.Div(
    children=[
        # Header Section
        html.Div(
            children=[
                html.H2(
                    "Welcome Back to your Sales Analytics Dashboard!",
                    style={"textAlign": "left", "color": "#ffffff", "flex": 1},
                ),
                # Profile Icon Placeholder
                html.I(
                    className="bi bi-person-circle",
                    style={"font-size": "50px", "color": "white", "marginLeft": "10px"},
                ),
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#151138",
                "display": "flex",
                "alignItems": "center",
            },
        ),
        # Date Picker Section
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(
                        children=[
                            html.P(
                                "Set custom filters to analyze your sales",
                                style={
                                    "color": "lightgrey",
                                    "fontSize": "20px",
                                    "marginRight": "20px",
                                },
                            ),
                        ]
                    ),
                    width=3,
                    style={
                        "padding": "10px",
                        "display": "flex",
                        "alignItems": "center",
                    },
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.DatePickerRange(
                                id="date-picker-range",
                                start_date=merged_data["Order.Date"].min().date(),
                                end_date=merged_data["Order.Date"].max().date(),
                                display_format="YYYY-MM-DD",
                                style={"color": "white"},
                            ),
                        ]
                    ),
                    width=3,
                    style={"padding": "10px"},
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="country-dropdown",
                                options=country_options,
                                multi=True,
                                placeholder="Select countries",
                                style={"color": "black", "width": "100%"},
                            ),
                        ]
                    ),
                    width=3,
                    style={"padding": "10px"},
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="category-dropdown",
                                options=category_options,
                                multi=True,
                                placeholder="Select Product Category",
                                style={"color": "black", "width": "100%"},
                            ),
                        ]
                    ),
                    width=3,
                    style={"padding": "10px"},
                ),
            ],
            style={"padding": "10px", "margin": "0"},
        ),
        # Main Dashboard Section
        dbc.Row(
            children=[
                # Total Sales Section
                dbc.Col(
                    html.Div(
                        children=[
                            # First Card: Total Sales
                            html.Div(
                                children=[
                                    html.H5(
                                        "Total Sales",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        html.H4(
                                            id="total-sales",
                                            style={
                                                "textAlign": "left",
                                                "color": "#00cb51",
                                                "fontSize": "50px",
                                            },
                                        )
                                    ),
                                    html.H5(
                                        "Sales Volume",
                                        style={
                                            "textAlign": "left",
                                            "color": "#ffffff",
                                            "marginTop": "20px",
                                        },
                                    ),
                                    dbc.Row(
                                        dcc.Graph(
                                            figure=sales_over_time_fig,
                                            id="sales-over-time",
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "marginBottom": "10px",
                                },
                            ),
                            # Second Card: Sales by Category
                            html.Div(
                                children=[
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                children=[
                                                    html.H5(
                                                        "Sales Distribution Insights",
                                                        style={
                                                            "textAlign": "left",
                                                            "color": "#ffffff",
                                                            "padding": "20px",
                                                        },
                                                    ),
                                                ],
                                                width=6,
                                            ),
                                            dbc.Col(
                                                children=[
                                                    dcc.Graph(
                                                        figure=sales_category_fig,
                                                        id="sales-category",
                                                        style={
                                                            "width": "140px",
                                                            "height": "140px",
                                                        },
                                                    )
                                                ],
                                                width=6,
                                            ),
                                        ],
                                    )
                                ],
                                style={
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "height": "140px",
                                },
                            ),
                        ],
                    ),
                    width=3,
                ),
                # Net Profit Section
                dbc.Col(
                    html.Div(
                        children=[
                            # First Card: Net Profit
                            html.Div(
                                children=[
                                    html.H5(
                                        "Net Profit",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        html.H4(
                                            id="total-profit",
                                            style={
                                                "textAlign": "left",
                                                "color": "#00cb51",
                                                "fontSize": "50px",
                                            },
                                        )
                                    ),
                                    html.H5(
                                        "Profit Margin",
                                        style={
                                            "textAlign": "left",
                                            "color": "#ffffff",
                                            "marginTop": "20px",
                                        },
                                    ),
                                    dbc.Row(
                                        html.H4(
                                            id="profit-margin",
                                            style={
                                                "textAlign": "left",
                                                "color": "#00cb51",
                                                "fontSize": "50px",
                                            },
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "marginBottom": "10px",
                                },
                            ),
                            html.Div(
                                children=[
                                    html.H5(
                                        "Profit Over Time",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        dcc.Graph(
                                            figure=profit_over_time_fig,
                                            id="profit-over-time",
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                },
                            ),
                        ],
                    ),
                    width=3,
                ),
                # Shipping Cost Section
                dbc.Col(
                    html.Div(
                        children=[
                            # First Card: Shipping Costs
                            html.Div(
                                children=[
                                    html.H5(
                                        "Total Shipping Cost",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        html.H4(
                                            id="total-costs",
                                            style={
                                                "textAlign": "left",
                                                "color": "#fb5a62",
                                                "fontSize": "50px",
                                            },
                                        )
                                    ),
                                    html.H5(
                                        "Average Shipping Cost",
                                        style={
                                            "textAlign": "left",
                                            "color": "#ffffff",
                                            "marginTop": "20px",
                                        },
                                    ),
                                    dbc.Row(
                                        html.H4(
                                            id="most-expensive-shipping",
                                            style={
                                                "textAlign": "left",
                                                "color": "#fb5a62",
                                                "fontSize": "50px",
                                            },
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "marginBottom": "10px",
                                },
                            ),
                            html.Div(
                                children=[
                                    html.H5(
                                        "Shipping Mode Information",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        dcc.Graph(
                                            figure=shipping_comparison_fig,
                                            id="shipping-comparison",
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                },
                            ),
                        ],
                    ),
                    width=3,
                ),
                # Customer Insights Section
                dbc.Col(
                    html.Div(
                        children=[
                            # First Card: Map
                            html.Div(
                                children=[
                                    html.H5(
                                        "Customer Insights",
                                        style={"textAlign": "left", "color": "#ffffff"},
                                    ),
                                    dbc.Row(
                                        dcc.Graph(
                                            figure=customer_heatmap_fig,
                                            id="customer-heatmap",
                                        )
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "marginBottom": "10px",
                                },
                            ),
                            # Second Card: Top Products
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.H5(
                                                "Customers Favorite Products",
                                                style={
                                                    "textAlign": "left",
                                                    "color": "white",
                                                    "marginBottom": "20px",
                                                },
                                            ),
                                            html.Div(id="top-products-container"),
                                        ],
                                    ),
                                ],
                                style={
                                    "padding": "20px",
                                    "paddingBottom": "26px",
                                    "backgroundColor": "#272950",
                                    "borderRadius": "10px",
                                    "height": "260px",
                                },
                            ),
                        ],
                    ),
                    width=3,
                ),
            ],
            style={"padding": "10px", "margin": "0px"},
            className="g-2",
        ),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#151138",
        "padding": "0",
        "margin": "0",
        "minHeight": "100vh",
    },
)


# Callback to update sales, profit, and graphs based on the selected date range, countries and categories
@app.callback(
    [
        Output("total-sales", "children"),
        Output("total-profit", "children"),
        Output("total-costs", "children"),
        Output("most-expensive-shipping", "children"),
        Output("profit-margin", "children"),
        Output("top-products-container", "children"),
        Output("sales-over-time", "figure"),
        Output("sales-category", "figure"),
        Output("profit-over-time", "figure"),
        Output("customer-heatmap", "figure"),
        Output("shipping-comparison", "figure"),
    ],
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        Input("country-dropdown", "value"),
        Input("category-dropdown", "value"),
    ],
)
def update_dashboard(start_date, end_date, selected_countries, selected_categories):
    # Filter the sales data based on the selected date range
    filtered_data = merged_data[
        (merged_data["Order.Date"] >= start_date)
        & (merged_data["Order.Date"] <= end_date)
    ]

    if selected_countries:
        filtered_data = filtered_data[filtered_data["Country"].isin(selected_countries)]

    if selected_categories:
        filtered_data = filtered_data[
            filtered_data["Category"].isin(selected_categories)
        ]

    # Calculate total sales, profit and costs
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    total_costs = filtered_data["Shipping.Cost"].sum()
    average_shipping = filtered_data["Shipping.Cost"].mean()

    # Calculate profit margin
    if total_sales > 0:
        profit_margin = (total_profit / total_sales) * 100
    else:
        profit_margin = 0

    # Get the top 5 products by sales
    top_products = (
        filtered_data.groupby("Product Name")["Sales"].sum().nlargest(5).reset_index()
    )
    top_products_list = updateTopProductList(top_products)

    # Get the graphs with the updated data
    (
        sales_over_time_fig,
        sales_category_fig,
        sales_subcategory_fig,
        profit_over_time_fig,
        customer_heatmap_fig,
        customer_city_fig,
        top_products_fig,
        shipping_mode_fig,
        shipping_comparison_fig,
    ) = get_all_graphs(filtered_data)

    return (
        f"${total_sales:,.0f}",
        f"${total_profit:,.0f}",
        f"${total_costs:,.0f}",
        f"${average_shipping:,.2f}",
        f"{profit_margin:,.2f}%",
        top_products_list,
        sales_over_time_fig,
        sales_category_fig,
        profit_over_time_fig,
        customer_heatmap_fig,
        shipping_comparison_fig,
    )


def updateTopProductList(top_products):
    tooltips = [
        dbc.Tooltip(
            id=f"tooltip-{i}",
            target=f"product-name-{i}",
            children=product,
            style={
                "backgroundColor": "black",
                "color": "white",
            },
        )
        for i, product in enumerate(top_products["Product Name"])
    ]

    # Create the updated top products display
    top_products_list = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        f"{i+1}. {product}",
                        id=f"product-name-{i}",
                        style={
                            "flex": 1,
                            "textAlign": "left",
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "color": "white",
                            "cursor": "pointer",
                        },
                    ),
                    html.Div(
                        f"${sales:,.0f}",
                        style={"flex": 1, "textAlign": "right", "color": "white"},
                    ),
                ],
                style={
                    "display": "flex",
                    "width": "100%",
                    "marginBottom": "10px",
                },
            )
            for i, (product, sales) in enumerate(
                zip(top_products["Product Name"], top_products["Sales"])
            )
        ]
        + tooltips
    )

    return top_products_list


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
