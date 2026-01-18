import plotly.express as px

class BubbleSalesProfit:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        bubble_data = (
            self.df
            .groupby("Category", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=("Quantity", "sum")
            )
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Sales vs Profit by Category{suffix}"

        # 3. Membuat Bubble Chart
        fig = px.scatter(
            bubble_data,
            x="Sales",
            y="Profit",
            size="Quantity",
            color="Category",
            hover_name="Category",
            size_max=60,
            # Gunakan urutan warna kuning/gold ke navy agar senada
            color_discrete_sequence=["#D4AC0D", "#1B2631", "#F6DA28"]
        )

        # 4. Layouting (Judul Tengah & Pembersihan Label)
        fig.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            xaxis_title="Total Sales",
            yaxis_title="Total Profit",
            legend_title="Category",
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Tambahkan grid halus untuk memudahkan pembacaan koordinat
        fig.update_xaxes(showgrid=True, gridcolor='#F0F0F0')
        fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0')

        return fig