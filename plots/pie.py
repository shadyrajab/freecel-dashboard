import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_pie(dataframe, tipo, key, title, color=None):
    color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
    if key.lower() == "clientes":
        counts = dataframe[tipo].value_counts()
        fig = go.Figure(
            go.Pie(
                labels=counts.index,
                values=counts.values,
                marker=dict(colors=color),
                pull=0.03,
            )
        )
        title_text = f'<b>{title}</b>'
    else:
        fig = go.Figure(
            px.pie(
                dataframe,
                values=key,
                names=tipo,
                title=title,
                color_discrete_sequence=color
            )
        )
        title_text = title

    fig.update_traces(textposition='inside', textinfo='value')
    fig.update_layout(
        title=title_text,
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
