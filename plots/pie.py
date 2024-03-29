import plotly.graph_objects as go
import streamlit as st


def plot_pie(dataframe, tipo, key, title, color):
    counts = dataframe[tipo].value_counts()
    labels = counts.index if key == "Clientes" else dataframe[tipo]
    values = counts.values if key == "Clientes" else dataframe[key]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            marker={"colors": color},
        )
    )

    fig.update_traces(textposition="inside", textinfo="value")
    fig.update_layout(
        title=f"<b>{title}</b>",
        yaxis={"autorange": "reversed"},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
