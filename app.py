import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt

@st.cache
def load_data():
    data = pd.read_csv("data/athlete_events.csv")
    regions = pd.read_csv("data/noc_regions.csv")
    merged = pd.merge(data, regions, on='NOC', how='left')
    return data, regions, merged

data, regions, merged = load_data()
st.sidebar.image("images/Olympic_rings.png")

def home(title):
    st.title(title)
    st.image("images/OLYMPIC-LOGOS.jpg")
    
def page1(title):
    st.title(title)
    goldMedals = merged[(merged.Medal == 'Gold')]
    if st.checkbox("Show raw data?"):
        x = st.sidebar.slider("Choose the number of rows to display", min_value=0, value=10, max_value=goldMedals.shape[0])
        st.write(goldMedals.head(x))
    goldMedals = goldMedals[np.isfinite(goldMedals['Age'])]
    st.header("Age distribution of Gold Medalist")
    st.plotly_chart(px.histogram(goldMedals, x='Age'))
    st.info("Most athelets are in their 20's")
    st.header("Gender distribution of Gold Medalist")
    st.plotly_chart(px.pie(goldMedals, names='Sex'))
    st.info("there are more male Gold Medalist then females, let's see why is that")
    st.header("Height distribution of Gold Medalist")
    st.plotly_chart(px.histogram(goldMedals, x='Height'))
    st.info('Most gold medalists are 1.8m tall.')
    st.header("Weight distribution of Gold Medalist")
    st.plotly_chart(px.histogram(goldMedals, x='Weight'))
    st.info("most winners have a weight range of 69.5kg-70.4kg")
    st.header("Height and Weight Scatter plot")
    st.plotly_chart(px.scatter(goldMedals, 'Height', 'Weight'))
    st.info("we can see a pattern here, most participants maintain their weight according to their height.")
    
def page2(title):
    st.title(title)
    womenInOlympics = merged[(merged.Sex == 'F') & (merged.Season == 'Summer')]
    st.header("How have female participants increased over the years?")
    st.plotly_chart(px.histogram(womenInOlympics, 'Year'))
    st.info("Women in olymipcs are seen a lot more now then 1900's")
    st.header('What sport is played most by women in olympics?')
    st.plotly_chart(px.histogram(womenInOlympics, 'Sport'))
    st.info("most women in olympics are athletes")
    st.header("Height and Weight Scatter plot")
    st.plotly_chart(px.scatter(womenInOlympics, 'Height', 'Weight'))
    st.info("we can see a pattern here, most participants maintain their weight according to their height.")

def page3(title):
    st.title(title)
    MenOverTime = merged[(merged.Sex == 'M') & (merged.Season == 'Summer')]
    WomenOverTime = merged[(merged.Sex == 'F') & (merged.Season == 'Summer')]
    part = MenOverTime.groupby('Year')['Sex'].value_counts()
    fig = plt.figure(figsize=(20, 10))
    part.loc[:,'M'].plot()
    st.header("Variation of Participants over time")
    st.write('Variation of Male Athletes over time')
    st.pyplot(fig)
    part = WomenOverTime.groupby('Year')['Sex'].value_counts()
    fig = plt.figure(figsize=(20, 10))
    part.loc[:,'F'].plot()
    st.write('Variation of Female Athletes over time')
    st.pyplot(fig)
    st.markdown("""
What I immediately saw is that for women:

1. We have a steep increase in the population;
2. The grow is constant.

On the other hand, the grow for men seems less strong:

1. After the 1990 we can see a relevant decrease in the number of male athletes at the summer games;
2. The growth has slowly restarted recently.
---
""")
    fig = plt.figure(figsize=(20, 10))
    sns.boxplot('Year', 'Age', data=MenOverTime)
    st.header("Variation of Age over time")
    st.write('Variation of Age for Male Athletes over time')
    st.pyplot(fig)
    fig = plt.figure(figsize=(20, 10))
    sns.boxplot('Year', 'Age', data=WomenOverTime)
    st.write('Variation of Age for Female Athletes over time')
    st.pyplot(fig)
    st.markdown("""
Interesting points for me:

* Generally, the age distribution starts has a lower minimum and a lower maximum;
* In 1904 the age distribution is strongly different from the other Olympics.
---
""")
    st.header("Variation of weight along time")
    fig = plt.figure(figsize=(20, 10))
    sns.pointplot('Year', 'Weight', data=MenOverTime)
    st.write('Variation of Weight for Male Athletes over time')
    st.pyplot(fig)
    fig = plt.figure(figsize=(20, 10))
    sns.pointplot('Year', 'Weight', data=WomenOverTime)
    st.write('Variation of Weight for Female Athletes over time')
    st.pyplot(fig)
    st.info("What we can see is that it seems that we do not have data for women before 1924.")
    st.markdown("---")
    st.header("Variation of height along time")
    fig = plt.figure(figsize=(20, 10))
    sns.pointplot('Year', 'Height', data=MenOverTime, palette='Set2')
    st.write('Variation of Height for Male Athletes over time')
    st.pyplot(fig)
    fig = plt.figure(figsize=(20, 10))
    sns.pointplot('Year', 'Height', data=WomenOverTime, palette='Set2')
    st.write('Variation of Height for Female Athletes over time')
    st.pyplot(fig)
    st.markdown("""
What we may see:

* For both men and women, the height is incrementing over time but it is decreasing between the 2012 and the 2016.
* For women we have a peak between 1928 and 1948.
---
""")
    
def page4(title):
    st.title(title)
    goldMedals = merged[(merged.Medal == 'Gold')]
    goldMedals = goldMedals[np.isfinite(goldMedals['Age'])]
    st.header("Which Country has won the most gold medals?")
    st.plotly_chart(px.histogram(goldMedals, x='region'))
    st.info("USA has the most medals, India has 119 medals so far.")
    st.header("Top 5 countries according to the medals count")
    cols = st.beta_columns([1,5])
    medal = cols[0].radio('Select a Medal', ['Gold', 'Silver', 'Bronze'])
    medalCounts = merged[merged.Medal==medal]['region'].value_counts().head()
    cols[1].plotly_chart(px.bar(x=medalCounts.index, y=medalCounts.values))
    st.info("USA has the most Gold, Silver, Bronze medals.")
    st.header("Top 5 countries with most participants")
    participation = merged['region'].value_counts().head()
    st.plotly_chart(px.bar(x=participation.index, y=participation.values))
    st.info("that explains all the medals, USA has the most participants in the Olympics")

def about(title):
    st.title(title)

pages = {"Introduction": home,
         "Analysis of gold medalist": page1,
         "Women in Olympics": page2,
         "YearWise Analysis": page3,
         "Countrywise Analysis": page4,
         "About": about
         }

page = st.sidebar.selectbox("Choose a page..", list(pages.keys()))
pages[page](page)
