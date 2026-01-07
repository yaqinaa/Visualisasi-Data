import plotly.express as px

class Bar1:
    def __init__(self, df):
        self.df = df

    def plot(self):
        df_grouped = self.df.groupby("Sub-Category")["Sales"].sum().reset_index()
        df_grouped = df_grouped.sort_values(by="Sales", ascending=False).head(10)
        fig = px.bar(
            df_grouped,
            x="Sales",
            y="Sub-Category",
            orientation="h",
            height=500
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig
