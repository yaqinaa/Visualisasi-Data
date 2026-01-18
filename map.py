import plotly.express as px
import numpy as np

# Mapping nama state ke kode 2 huruf
STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

class MapSalesState:
    def __init__(self, df):
        self.df = df

    # Tambahkan parameter year="All" agar tidak TypeError
    def plot(self, year="All"):
        # --- PREP DATA ---
        df = self.df.copy()
        df["State"] = df["State"].astype(str).str.strip()

        state_sales = (
            df
            .groupby("State", as_index=False)
            .agg(Sales=("Sales", "sum"))
        )

        # Mapping ke kode state
        state_sales["State_Code"] = state_sales["State"].map(STATE_ABBR)
        state_sales = state_sales.dropna(subset=["State_Code"])

        # Log scale supaya gradasi kuningnya rata
        state_sales["Sales_log"] = np.log10(state_sales["Sales"] + 1)

        # LOGIKA JUDUL DINAMIS
        # Jika tahun bukan 'All', maka judul akan bertambah "in 2015" misalnya
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Geographical Distribution of Sales by State{suffix}"

        # --- CHOROPLETH MAP ---
        fig = px.choropleth(
            state_sales,
            locations="State_Code",
            locationmode="USA-states",
            color="Sales_log",
            scope="usa",
            color_continuous_scale="YlOrBr", # Tema Kuning Emas
            hover_name="State",
            hover_data={"Sales": ":,.0f", "Sales_log": False} # Sembunyikan sales_log dari tooltip
        )

        # --- FINAL TOUCH (RAPID) ---
        fig.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5, # Judul di tengah
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            margin=dict(l=10, r=10, t=80, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                lakecolor='#FFFFFF',
                showlakes=True
            ),
            coloraxis_showscale=False # Hilangkan colorbar biar clean
        )

        # Auto zoom
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )

        return fig