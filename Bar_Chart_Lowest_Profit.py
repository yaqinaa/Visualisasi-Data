import plotly.express as px

class BarLowestProfitCity:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        # Tetap sort ascending=True agar profit terendah (paling negatif) di awal list
        city_profit = (
            self.df
            .groupby("City", as_index=False)
            .agg(Profit=("Profit", "sum"))
            .sort_values(by="Profit", ascending=True)
            .head(10)
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Top 10 Cities with Lowest Profit{suffix}"

        # 3. Membuat Bar Chart Horizontal
        fig = px.bar(
            city_profit,
            x="Profit",
            y="City",
            orientation="h",
            text="Profit",
            color="Profit",
            # Gunakan _r (reversed) agar nilai negatif terkecil dapet warna gelap
            color_continuous_scale="YlOrBr_r" 
        )

        # 4. Layouting (Ranking Balik & Judul Tengah)
        fig.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'font': {'size': 20, 'color': '#1B2631'}
            },
            # yaxis reversed agar index 0 (paling rugi) ada di paling atas
            yaxis=dict(autorange="reversed", title=""),
            xaxis_title="",
            margin=dict(l=20, r=20, t=100, b=20),
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450
        )

        # 5. Styling Bar
        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            marker_line_color='#1B2631',
            marker_line_width=1
        )

        return fig