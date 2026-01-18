import plotly.express as px

class Bar5:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        segment_sales = (
            self.df
            .groupby("Segment", as_index=False)
            .agg(Sales=("Sales", "sum"))
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Total Sales per Segment{suffix}"

        # 3. Membuat Bar Chart
        fig_segment_sales = px.bar(
            segment_sales, 
            x="Segment", 
            y="Sales",
            color="Sales",
            color_continuous_scale=[
              "#f7f4e4",
              "#f4ebb3",
              "#f2d46f",
              "#F6C102"
            ],
            text_auto=".2s",
        )

        # 4. Styling & Layouting (Fokus pada Judul)
        fig_segment_sales.update_traces(
            textposition='outside',
            marker_line_color='#1B2631',
            marker_line_width=1
        )

        fig_segment_sales.update_layout(
            # Bagian ini yang krusial bro
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95, # Mengangkat sedikit posisi judul
                'font': {'size': 20, 'color': '#1B2631'}
            },
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title="",
            # T=100 memberikan ruang lebih luas untuk judul agar tidak tertutup container
            margin=dict(l=20, r=20, t=100, b=20), 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450
        )

        fig_segment_sales.update_xaxes(showgrid=False)
        fig_segment_sales.update_yaxes(showgrid=True, gridcolor='#F0F0F0')

        return fig_segment_sales