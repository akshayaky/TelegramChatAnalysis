import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bs4 import BeautifulSoup as bs
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
def extractData(names, dataFields, dataName):
	extractedData = {}
	for i in names.keys():
		extractedData[i] = []
		for j in dataFields:
			if j not in names[i][dataName].keys():
				extractedData[i].append(0)
			else:
				extractedData[i].append(names[i][dataName][j])

	return extractedData

def figFill(x, data, hoverTemplate):
	first = True
	fig = go.Figure()
	for i in data.keys():
		if first:
			fig = go.Figure(go.Bar(x=x, y = data[i], name=i))
			first = False
		else:
			fig.add_trace(go.Bar(x=x, y=data[i], name=i))
	fig.update_traces(hovertemplate = hoverTemplate)
	fig.update_layout(bargap = 0,barmode='group', xaxis={'categoryorder':'category ascending'})
	return fig

def PlotandSave(names):
	people = []
	count = []
	length = []
	average = []
	personMonths = set()
	personDays = set()
	personTimes = set()        
	for i in names.keys():
		people.append(i)
		count.append(names[i]['count'])
		length.append(names[i]['length'])
		average.append(names[i]['length']/names[i]['count'])
		personMonths.update((names[i]['month'].keys()))
		personDays.update(names[i]['date'].keys())
		personTimes.update(names[i]['time'].keys())

	personMonths = sorted(personMonths)
	personTimes = sorted(personTimes)
	personDays = sorted(personDays)
	
	# idx = pd.date_range(personDays[0], personDays[-1])
	# l = []
	# for i in idx:
	# 	l.append(str(i)[0:10])
	# personDays = l


	monthlyPerPerson = extractData(names, personMonths, 'month')
	datePerPerson = extractData(names, personDays, 'date')
	timePerPerson = extractData(names, personTimes, 'time')
	
	# print(datePerPerson)
	
	messageVals = []
	nameVals = []
	for i in monthlyPerPerson.keys():
		messageVals.extend(monthlyPerPerson[i])
		nameVals.extend(len(monthlyPerPerson[i])*[i])
		personMonths += personMonths

	df = pd.DataFrame(list(zip(messageVals, nameVals, personMonths)),
			   columns =[ 'val', 'name', 'month'])
	widths = np.empty(len(messageVals))
	widths.fill(10)
	fig1 = px.bar(df, x='month', y='val',
			 hover_data=['name', 'val'], color='name',
			barmode='group', height=400)
	
	fig2 = figFill(personMonths, monthlyPerPerson, " <br>Date: %{x|%B %Y}</br>No. of Words %{y}")
	fig3 = figFill(personDays, datePerPerson, " <br>Date: %{x}</br>No. of Words %{y}")
	fig4 = figFill(personTimes, timePerPerson, " <br>Time: %{x}:00</br>No. of Words %{y}")


	# fig.update_layout(bargap = 0.5)
	# fig.show()
	with open('AnalysisResult.html', 'w') as f:
		f.write("<style>h1{text-align: center;}h2{text-align: center;}</style>")
		f.write("<h1>Chat Analysis</h1>")
		f.write("<h2>Monthly Distribution</h2>")
		f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
		f.write("<h2>Daily Distribution</h2>")
		f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
		f.write("<h2>Hourly Distribution</h2>")
		f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
	AddWordCloud(names)


def AddWordCloud(names):
	words = []
	for i in names.keys():
		words.extend(["".join(text) for text in names[i]['words']])
	words = " ".join(words)
    # print(words)
	stopwords = ["alla", "illa", "mhh", "Aah", "okay", "aan","ille", "alle", "Ooh", "ooh"]
	wordcloudChats = WordCloud(stopwords = stopwords, background_color="white", width = 700, height = 700).generate(words)
	wordcloudChats.to_file("wordCloud.png")

	html = open('AnalysisResult.html')
	soup = bs(html, 'html.parser')
      
	divs = soup.find_all("div")
      
    # Replace the already stored text with 
    # the new text which you wish to assign
	# new_text = soup.find(text=re.compile('')).replace_with('<img src = "wordCloud.png">')
	new_tag = soup.new_tag('img', src='wordCloud.png', **{'class':'center'})
	style_tag = soup.new_tag("style")
	style_tag.string = """
	.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
""" 
	divs[0].append(new_tag)
	divs[0].append(style_tag)
    # Adding content to div
	# new_img = '<img src = "wordCloud.png">'
  
    # Appending new div to html tree
	# soup.append(new_img)
    # Alter HTML file to see the changes done
	with open("AnalysisResult.html", "wb") as f_output:
		f_output.write(soup.prettify("utf-8"))


def PlotandSave1(names):
	df = px.data.gapminder().query("continent == 'Oceania'")
	fig = px.bar(df, x='year', y='pop',
			 hover_data=['lifeExp', 'gdpPercap'], color='country',
			 labels={'pop':'population of Canada'}, height=5000)
	# fig.write_html('first_figure.html', auto_open=True)