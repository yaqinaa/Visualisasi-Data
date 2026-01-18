import plotly.express as px

class Bar7:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing
        top_customer_data = (
            self.df.groupby("Customer Name")["Sales"]
            .sum()
            .reset_index()
            .sort_values(by="Sales", ascending=False)
            .head(10)
        )

        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Top 10 Customers by Sales{suffix}"

        # 3. Membuat Bar Chart Horizontal
        fig_top_customer = px.bar(
            top_customer_data,
            x="Sales",
            y="Customer Name",
            orientation="h", # Memastikan orientasi horizontal
            color="Sales",
            color_continuous_scale="YlOrBr",
            text_auto=".2s"
        )

        # 4. Layouting & Styling (Judul Tengah & Clean Axis)
        fig_top_customer.update_layout(
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1B2631'}
            },
            yaxis=dict(autorange="reversed", title=""), # Ranking 1 di atas, hapus label "Customer Name"
            xaxis_title="", # Hapus label "Total Sales" agar lebih luas
            margin=dict(t=80, b=40, l=120, r=40),
            height=450,
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # 5. Finishing Touches
        fig_top_customer.update_traces(
            marker_line_color='#1B2631',
            marker_line_width=1,
            textposition='outside' # Angka sales di luar batang agar tidak menumpuk
        )
        fig_top_customer.update_yaxes(automargin=True)
        
        return fig_top_customer