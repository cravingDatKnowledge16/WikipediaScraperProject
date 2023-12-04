import pandas as pd
import numpy as np

#pd.set_option("max_columns", 30)

import plotly.express as px
import plotly.graph_objects as go
import os
"""
starbucks_locations = pd.read_csv("datasets/starbucks_store_locations.csv")
starbucks_dist = starbucks_locations.groupby(by=["Country", "State/Province", "City"]).count()[["Store Number"]].rename(columns={"Store Number":"Count"})
starbucks_dist["World"] = "World"
starbucks_dist = starbucks_dist.reset_index()
starbucks_dist.head()


fig = px.sunburst(
    starbucks_dist,
    path=["World", "Country", "State/Province", "City"],
    values='Count',
    title="Starbucks Store Count Distribution World Wide [Country, State, City]",
    width=750, height=750)
fig.show()

"""


data = dict(
    character=['Photon', 'Altgriechische Sprache', 'Licht', 'Elektromagnetische Welle', 'Austauschteilchen'],
    parent=['', 'Photon', 'Photon', 'Photon', 'Photon']
)

fig = px.sunburst(
    data,
    names="character",
    parents="parent"
)
fig.show()
