import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_pie(dataframe, tipo, key, title, color=None):
    color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
    counts = dataframe[tipo].value_counts()

    labels = counts.index if key == "clientes" else dataframe[tipo]
    values = counts.values if key == "clientes" else dataframe[key]

    total = counts.sum()
    sizes = [count / total for count in counts.values]

    largest_slice_index = sizes.index(max(sizes))

    pull_values = [0.07 if i == largest_slice_index else 0.05 for i in range(len(sizes))]
    
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=color),
            pull = pull_values,
        )
    )

    fig.update_traces(textposition='inside', textinfo='value')
    fig.update_layout(
        title=f'<b>{title}</b>',
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
