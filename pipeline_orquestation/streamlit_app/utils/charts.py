import plotly.express as px

def plot_avg_intelligence(breeds_df):
    avg_origin = breeds_df.groupby('origin')['intelligence'].mean().reset_index()
    return px.bar(avg_origin, x='origin', y='intelligence', title='Average Intelligence by Origin')
