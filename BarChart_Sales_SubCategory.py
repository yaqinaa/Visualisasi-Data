import plotly.express as px

class Bar1:
    def __init__(self, df):
        self.df = df

    def plot(self, year="All"):
        # 1. Data Processing: Ambil Top 10 Sub-Category
        df_grouped = self.df.groupby("Sub-Category")["Sales"].sum().reset_index()
        df_grouped = df_grouped.sort_values(by="Sales", ascending=False).head(10)
        
        # 2. Logika Judul Dinamis
        suffix = f" in {year}" if year != "All" else ""
        title_text = f"Top Product by Sales{suffix}"

        # 3. Membuat Pie Chart (Penuh)
        fig = px.pie(
            df_grouped,
            values='Sales',
            names='Sub-Category',
            # MENGGUNAKAN WARNA KUNING EMAS (Gradasi YlOrBr)
            color_discrete_sequence=px.colors.sequential.YlOrBr_r 
        )

        # 4. Styling: Tanpa legenda, label otomatis, border putih agar clean
        fig.update_traces(
            textposition='inside', 
            textinfo='label+percent',
            marker=dict(line=dict(color='#FFFFFF', width=2)), 
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.2f}<extra></extra>"
        )

        # 5. Layouting (Tinggi Seragam & Judul Tengah)
        fig.update_layout(
            showlegend=False, 
            title={
                'text': f"<b>{title_text}</b>",
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95, # Angkat sedikit biar simetris
                'font': {'size': 20, 'color': '#1B2631'}
            },
            # Margin T=100 disamakan dengan Bar2 dan Bar7 agar rata
            margin=dict(l=30, r=30, t=100, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450 # KUNCI BIAR RATA BOXNYA
        )

        return fig