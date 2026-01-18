import plotly.express as px

class Bar3:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        yearly_data = (
            self.df
            .groupby("Year", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Total Sales by Year{suffix}"

        # 3. Membuat Line Chart
        fig_sales = px.line(
            yearly_data,
            x="Year",
            y="Sales",
            markers=True
        )

        # 4. Styling Sumbu X agar tetap rapi
        fig_sales.update_xaxes(
            tickmode="linear",
            tick0=yearly_data["Year"].min(),
            dtick=1,
            title=""
        )

        # 5. Layouting dengan Judul Dinamis di Tengah
        fig_sales.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # Menambahkan warna kuning emas agar senada dengan yang lain
            colorway=["#D4AC0D"] 
        )

        return fig_sales