import plotly.express as px

class Bar6:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        segment_profit = (
            self.df
            .groupby("Segment", as_index=False)
            .agg(Profit=("Profit", "sum"))
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Total Profit per Segment{suffix}"

        # 3. Membuat Donut Chart (Hole 0.4)
        fig_segment_profit = px.pie(
            segment_profit,
            names="Segment",
            values="Profit",
            hole=0.4,
            color_discrete_sequence=[
                "#f7f4e4",
                "#f6da28",
                "#c19502",
                "#8F5D00"
            ]
        )

        # 4. Styling (Garis border hitam/navy dihapus)
        fig_segment_profit.update_traces(
            textposition='inside',
            textinfo='label+percent',
            # Marker line ditiadakan atau dibuat putih tipis agar seperti awal
            marker=dict(line=dict(color='white', width=1)), 
            hovertemplate="<b>%{label}</b><br>Profit: $%{value:,.2f}<extra></extra>"
        )

        # 5. Layouting dengan Judul Dinamis di Tengah
        fig_segment_profit.update_layout(
            showlegend=False,
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450
        )

        return fig_segment_profit