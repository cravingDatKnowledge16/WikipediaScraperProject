from xml.dom.minidom import TypeInfo
from numpy import character
import plotly.express as px
import re
"""
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

fig = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)

fig.show()

"""

with open("results/TADA.txt", mode="r") as file:
    rawdata = file.read()
rawdata = rawdata.split()
rawdata2 = []
for i in range(len(rawdata)):
    if rawdata[i] != ":":
        rawdata2.append(rawdata[i])
rawdata3 = dict()

for i in range(0, len(rawdata2), 2):
    rawdata3[f"{rawdata2[i]}"] = f"{re.sub(pattern='https://de.wikipedia.org/wiki/', repl='', string=rawdata2[i+1])}"
#print(rawdata3)



sitelist = []
#sitelist.append(f"{re.sub(pattern='https://de.wikipedia.org/wiki/', repl='', string=rawdata2[1])}")
parentlist = []
valueList = []

for element in rawdata3:
    sitelist.append(rawdata3[element])
    valueList.append("1")
    for elementOfrawdata3 in rawdata3:
        pos = rawdata3[elementOfrawdata3].rfind(",")
        if elementOfrawdata3[0:pos] == element:
            parentlist.append(rawdata3[elementOfrawdata3])

data = dict(sites = sitelist, parents = parentlist, valueList = valueList)

print(len(sitelist))
print(len(parentlist))
print(len(valueList))


fig = px.sunburst(
    data,
    names='sites',
    parents='parents',
    values='valueList',
)

print(fig)

fig.show()
