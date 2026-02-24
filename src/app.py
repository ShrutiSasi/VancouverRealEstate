from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_plotly
import plotly.express as px
import pandas as pd

years = list(range(2004, 2023))
housing_data = pd.read_csv("data/raw/synthetic_house_prices_20_years.csv")
coord_data = pd.read_csv("data/raw/vancouver_neighborhoods_coordinates.csv")
neighborhood_choices = sorted(housing_data["Neighborhood"].dropna().unique().tolist())
property_type_choices = sorted(housing_data["Property Type"].dropna().unique().tolist())

app_ui = ui.page_fluid(    
    ui.layout_sidebar(
        ui.sidebar(
            ui.panel_title("Vancouver Real Estate"),
            ui.input_selectize(
                id="neighborhood",
                label="Select Neighborhood(s):",
                choices=neighborhood_choices,
                multiple=True 
            ),
            ui.input_slider(
                id="year",
                label="Select Year/Range:",
                min=min(years),
                max=max(years),
                value=[min(years),max(years)],
                step=1,
                sep=""
            ),
            ui.input_checkbox_group(
                id="property",
                label="Select Property Type:",
                choices=property_type_choices
            ),
            ui.input_action_button(
                "action_button", 
                "Reset filter"
            ),
            open="desktop",
        ),
        ui.panel_title("Real Estate Dashboard depicting house prices in Vancouver."),
        ui.layout_columns(
            ui.div(
                ui.layout_columns(
                    ui.value_box(
                        "Highest Price", 
                        ui.output_text("highest_price_val")
                    ),
                    ui.value_box(
                        "Lowest Price", 
                        ui.output_text("lowest_price_val")
                    ),
                    ui.value_box(
                        "Average Market Price", 
                        ui.output_text("average_price_val")
                    ),
                    fill=False,
                ),
                ui.card(
                    #ui.card(ui.card_header("YoY% Changes")),
                    output_widget("yoy_change_plot")
                )
            ),            
            ui.layout_columns(
                ui.card(
                    ui.card_header("Area Map"),
                    output_widget("map_plot"),
                    full_screen=True
                )
            )
        ),        
        ui.layout_columns(
            ui.card(
                #ui.card_header("Average Market Price by Neighborhood"), 
                output_widget("avg_market_trend_plot"), 
                full_screen=True
            ),
            ui.card(
                #ui.card_header("Top 5 expensive neighborhoods Trend"),
                output_widget("top_5_neighborhood_plot"), 
                full_screen=True
            )
        )
    )
    
)

def server(input, output, session):
    # Create a reactive calculation to filter the data
    @reactive.calc
    def filtered_df():
        df = pd.merge(housing_data, coord_data, how="inner", on=["Neighborhood"])
        # Filter by Year Range (Slider)
        # input.year() returns a tuple: (min_val, max_val)
        year_range = input.year()
        df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
        
        # Filter by Neighborhood (Selectize)
        # If no neighborhood is selected, it returns an empty tuple ()
        if input.neighborhood():
            df = df[df["Neighborhood"].isin(input.neighborhood())]
            
        # Filter by Property Type (Checkbox Group)
        # If nothing is checked, it returns an empty tuple ()
        if input.property():
            df = df[df["Property Type"].isin(input.property())]
            
        return df

    @render.text
    def highest_price_val():
        df = filtered_df()
        if df.empty:
            return "$0"
        max_val = df["Market Price"].max() 
        return f"${max_val:,.0f}"

    @render.text
    def lowest_price_val():
        df = filtered_df()
        if df.empty:
            return "$0"
        min_val = df["Market Price"].min() 
        return f"${min_val:,.0f}"

    @render.text
    def average_price_val():
        df = filtered_df()
        if df.empty:
            return "$0"
        avg_val = df["Market Price"].mean() 
        return f"${avg_val:,.0f}"

    @render_plotly
    def map_plot():
        # Get the current filtered data from the reactive calculation
        df = filtered_df()
        
        # Guard clause: if no data is found for the selection, return an empty figure
        if df.empty:
            return px.scatter_mapbox(title="No data available for selection")

        # Use the latest year within the filtered range for the map title/data
        current_max_year = df["Year"].max()
        map_data = df[df["Year"] == current_max_year]

        fig = px.scatter_mapbox(
            map_data,
            lat="Latitude",
            lon="Longitude",
            size="Market Price",
            color="Market Price",
            hover_name="Neighborhood",
            hover_data={"Market Price": ":,.0f", "Latitude": False, "Longitude": False},
            size_max=15, # Adjusted size for better dashboard fit
            zoom=10,
            mapbox_style="carto-positron"
        )

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0}, # Tighten margins for the card
            title=f"Vancouver Market Prices ({current_max_year})"
        )
        
        return fig

    @render_plotly
    def avg_market_trend_plot():
        # Get the current filtered data from the reactive calculation
        df = filtered_df()

        if df.empty:
            return px.bar(title="No data selected")

        # Process the data for the bar chart
        # We group by Neighborhood and calculate the mean of Market Price
        neighborhood_avg = (
            df.groupby("Neighborhood", as_index=False)["Market Price"]
            .mean()
            .sort_values(by="Market Price", ascending=False)
        )

        # Create the Plotly Bar Chart
        fig = px.bar(
            neighborhood_avg,
            x="Neighborhood",
            y="Market Price",
            labels={"Market Price": "Avg Price ($)"},
            color="Market Price",  # Adds a color gradient like your heatmap
            color_continuous_scale="Blues" 
        )

        # Final Layout Adjustments
        fig.update_layout(
            title="Average Market Price by Neighborhood",
            xaxis_title="Neighborhood",
            yaxis_title="Average Price ($)",
            template="plotly_white",
            showlegend=False
        )    
        return fig

    @render_plotly
    def top_5_neighborhood_plot():
        # Get the current filtered data from the reactive calculation
        df = filtered_df()
        if df.empty:
            return px.line(title="No data selected")

        # Process the data for the line chart
        # We group by Year and Neighborhood and calculate the mean of Market Price
        neighborhood_avg = (
            df.groupby(["Year", "Neighborhood"], as_index=False)["Market Price"]
            .mean()
        )        
        current_max_year = neighborhood_avg["Year"].max()
        latest_data = neighborhood_avg[neighborhood_avg["Year"] == current_max_year]
        top5_names = (
            latest_data.sort_values(by="Market Price", ascending=False)
            .head(5)["Neighborhood"]
            .tolist()
        )
        plot_data = neighborhood_avg[neighborhood_avg["Neighborhood"].isin(top5_names)]
        # Create the Plotly line Chart
        fig = px.line(
            plot_data,
            x="Year",
            y="Market Price",
            color="Neighborhood",
            markers=True,
            labels={"Market Price": "Avg Price ($)"}
        )

        # Final Layout Adjustments
        fig.update_layout(
            title=f"Trend for Top 5 Neighborhoods (as of {current_max_year})",
            template="plotly_white",
        hovermode="x unified", # Shows all 5 prices in one tooltip when hovering
        legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )    
        return fig

    @render_plotly
    def yoy_change_plot():
        df = filtered_df()
        if df.empty:
            return px.line(title="No data selected")

        # Calculate Average Price per Year (Aggregated across selected filters)
        # If multiple neighborhoods are selected, this shows the trend for the group
        yearly_avg = (
            df.groupby("Year")["Market Price"]
            .mean()
            .reset_index()
            .sort_values("Year")
        )

        # Calculate YoY % Change
        # We multiply by 100 to get a percentage (e.g., 0.05 becomes 5.0)
        yearly_avg["YoY Change %"] = yearly_avg["Market Price"].pct_change() * 100

        # Create the Plotly Line Chart
        # We drop the first row because YoY change for the first year is always NaN
        fig = px.line(
            yearly_avg.dropna(),
            x="Year",
            y="YoY Change %",
            markers=True,
            labels={"YoY Change %": "Price Growth (%)"},
            color_discrete_sequence=["#2c3e50"] # Sleek dark color
        )

        # Add a horizontal 'Zero' line to distinguish growth from decline
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)

        fig.update_layout(
            title="Year-over-Year Price Growth (%)",
            template="plotly_white",
            #yaxis_suffix="%",
            hovermode="x unified"
        )
        fig.update_yaxes(ticksuffix="%")
        return fig

app = App(app_ui, server)