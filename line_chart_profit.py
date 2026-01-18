import plotly.express as px

class Bar4:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        yearly_data = (
            self.df
            .groupby("Year", as_index=False)
            .agg(
                Profit=("Profit", "sum")
            )
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Total Profit by Year{suffix}"

        # 3. Membuat Line Chart
        fig = px.line(
            yearly_data,
            x="Year",
            y="Profit",
            markers=True
        )

        # 4. Styling Sumbu X
        fig.update_xaxes(
            tickmode="linear",
            tick0=yearly_data["Year"].min(),
            dtick=1,
            title=""
        )

        # 5. Layouting (Judul Tengah & Warna Kuning Emas)
        fig.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # Menggunakan warna kuning emas agar seragam
            colorway=["#D4AC0D"]
        )

        return fig