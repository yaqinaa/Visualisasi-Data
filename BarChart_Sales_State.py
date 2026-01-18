import plotly.express as px

class Bar2:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing: Ambil Top 10 City by Sales
        df_grouped = self.df.groupby("City")["Sales"].sum().reset_index()
        df_grouped = df_grouped.sort_values(by="Sales", ascending=False).head(10)
        
        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Top 10 Cities by Sales{suffix}"

        # 3. Membuat Bar Chart Horizontal dengan Gradasi
        fig = px.bar(
            df_grouped,
            x="Sales",
            y="City",
            orientation="h",
            color="Sales", 
            color_continuous_scale="YlOrBr" 
        )

        # 4. Styling: Rapikan tampilan batang
        fig.update_traces(
            marker_line_color='#1B2631', 
            marker_line_width=1,
            opacity=0.9,
            hovertemplate="<b>%{y}</b><br>Total Sales: $%{x:,.2f}<extra></extra>"
        )

        # 5. Layouting: Judul Tengah & Tinggi Seragam
        fig.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95, # Angkat sedikit agar sejajar secara vertikal dengan yang lain
                'font': {'size': 20, 'color': '#1B2631'}
            },
            yaxis=dict(autorange="reversed", title=""), 
            xaxis=dict(title="", showgrid=True, gridcolor='#F0F0F0'),
            # Margin T=100 disamakan agar box container tidak terlihat "naik-turun"
            margin=dict(l=10, r=20, t=100, b=10), 
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450, # KUNCI BIAR RATA DENGAN BAR1 DAN BAR7
            coloraxis_showscale=False 
        )

        return fig