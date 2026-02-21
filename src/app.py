from shiny import App, ui
import pandas as pd

years = list(range(2004, 2023))
housing_data = pd.read_csv("data/raw/synthetic_house_prices_20_years.csv")
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
                    ui.value_box("Highest Price", "Value 1"),
                    ui.value_box("Lowest Price", "Value 2"),
                    ui.value_box("Average Market Price", "Value 3"),
                    fill=False,
                ),
                ui.layout_columns(
                    ui.card(ui.card_header("YoY% Changes"))
                )
            ),            
            ui.layout_columns(
                ui.card(ui.card_header("Area Map"))
            )
        ),        
        ui.layout_columns(
            ui.card(ui.card_header("Average Market Price by Neighborhood"), full_screen=True),
            ui.card(ui.card_header("Top 5 expensive neighborhood Trend"), full_screen=True),
            col_widths=[6, 6],
        )
    )
    
)

def server(input, output, session):
    pass

app = App(app_ui, server)