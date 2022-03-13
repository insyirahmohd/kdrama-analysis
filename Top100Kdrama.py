import streamlit as st
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt

st.title("Top Kdrama Analysis")
st.image("https://chingutotheworld.com/wp-content/uploads/2019/05/kdrama.jpg")
st.markdown("""**Data Source:** [Top 100 Korean Drama (MyDramaList)as of the end of 2021](https://www.kaggle.com/chanoncharuchinda/top-100-korean-drama-mydramalist)
""" )

col_names = ['Name', 'YearRelease', 'AiredDate', 'AiredOn', 'NumEp', 'Network', 'Duration', 'ContentRating', 'Synopsis', 'Cast', 'Genre', 'Tags', 'Rank', 'Rating']
# load dataset
df = pd.read_csv("top100_kdrama.csv", header=0, names=col_names) # 0 is false. names will be col_names as dah declare
df = df.drop(['AiredDate', 'Synopsis', 'Cast', 'Genre', 'Tags', 'Rank'],axis=1)

### LABEL THE RATING. HIGHER THAN MEAN = 1, LOWER THAN MEAN = 0 ###
df['RatingLabel'] = np.zeros((100,))
df['RatingLabel'] = np.where(df['Rating'] > 8.7, 1, 0) # 1 = high rating/above mean
################################################################

### ONLY THE FIRST NETWORK CHOSEN TO BE THE AIRING NETWORK ###
for i, row in enumerate (df['Network']):
    net = str(row)
    net = net.split(',')
    df['Network'][i] = net[0].strip()
################################################################

### CATEGORISE AIRING DAY INTO WEEKEND AND WEEKDAYS ###
#Friday and Saturday consider as Weekdays
df['Days'] = np.zeros((100,))
for i, col in enumerate(df['AiredOn']):
    day = col.split(", ")

    if day[0].find('Saturday') == True or day[0].find('Sunday') == True:
      df['Days'][i] = 'Weekend'
    else:
      df['Days'][i] = 'Weekday'
df = df.drop(['AiredOn'], axis = 1)
################################################################

### CHANGE DURATION TO MINUTES ###
def t_converter(duration):
    duration = duration.strip(" min.").replace(" hr. ",":")
    # SHould now have a string of this formate'X:YY'
    T = duration.split(':')
    if len(T)==2:
        hours = int(T[0])*60
        mins = int(T[1])
        time = hours +mins
    else:
        time = int(T[0]) #this only has minutes
    return time
for i, run in enumerate(df['Duration']):
    df['Duration'][i] = t_converter(run)
df.rename(columns = {'Duration':'Duration/min'}, inplace = True)
################################################################

### CATEGORISE LESS THAN HOUR AND AT LEAST HOUR PER EPISODE INTO NEW COLUMN ###
for i, run in enumerate(df['Duration/min']):
  df['Duration'] = np.where(df['Duration/min'] >= 60, 'atleastHour', 'belowHour')
df.head()
################################################################

df1 = df.drop(['Name', 'RatingLabel'],axis=1)
# CSS to inject contained in a string
# hide_dataframe_row_index = """
#             <style>
#             .row_heading.level0 {display:none}
#             .blank {display:none}
#             </style>
#             """

# # Inject CSS with Markdown
# st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# Display an interactive table
#st.dataframe(df)

st.subheader("Based on your choices: ")
st.markdown('RatingLabel = 0 represents drama with rating below than mean(8.7)')
st.markdown('RatingLabel = 1 represents drama with rating more than mean(8.7)')
#SIDEBAR
st.sidebar.header('CHOICES')
#Choose how many drama/data to display
display_df = st.sidebar.select_slider('KDRAMA TOP', 
                                      options=[3, 5, 10, 20])
df1 = df.drop(['RatingLabel'], axis = 1)

if display_df == 3:
  st.subheader('TOP 3 KDRAMA 2021')
  st.dataframe(df1[0:3])

elif display_df == 5:
  st.subheader('TOP 5 KDRAMA 2021')
  st.dataframe(df1[0:5])

elif display_df == 10:
  st.subheader('TOP 10 KDRAMA 2021')
  st.dataframe(df1[0:10])  

elif display_df == 20:
  st.subheader('TOP 20 KDRAMA 2021')
  st.dataframe(df1[0:20])

#Choose factor to group by data
option = st.sidebar.selectbox('Highest Rating by: ',
                                ['Year', 'Network', 'Duration per episode', 'Type of day', 'Content rating'])

if option == 'Year':
  df_groupby = df.groupby('YearRelease')['Rating'].sum()
  df_groupby = df_groupby.sort_values(ascending=False)
  st.write(df_groupby)
  
  # plot the result
  fig, ax = plt.subplots()
  df.groupby(['YearRelease','RatingLabel']).count()['Rating'].unstack().plot(ax=ax)
  st.pyplot(fig)

elif option == 'Network':
  df_groupby = df.groupby('Network')['Rating'].sum()
  df_groupby = df_groupby.sort_values(ascending=False)
  st.write(df_groupby)

  # plot the result
  fig, ax = plt.subplots()
  df.groupby(['Network','RatingLabel']).count()['Rating'].unstack().plot(ax=ax)
  st.pyplot(fig)

elif option == 'Duration per episode':
  df_groupby = df.groupby('Duration')['Rating'].sum()
  df_groupby = df_groupby.sort_values(ascending=False)
  st.write(df_groupby)

  # atleastHour = df[df['Duration/min']>=60]
  # belowHour = df[df['Duration/min']<60]

  # st.write('Kdramas with duration at least an hour per episode')
  # st.write(atleastHour)
  # st.write('Kdramas with duration less than an hour per episode')
  # st.write(belowHour)

  # plot the result
  fig, ax = plt.subplots()
  df.groupby(['Duration','RatingLabel']).count()['Rating'].unstack().plot(ax=ax)
  st.pyplot(fig)

elif option == 'Type of day':
  df_groupby = df.groupby('Days')['Rating'].sum()
  df_groupby = df_groupby.sort_values(ascending=False)
  st.write(df_groupby)

  # plot the result
  fig, ax = plt.subplots()
  df.groupby(['Days','RatingLabel']).count()['Rating'].unstack().plot(ax=ax)
  st.pyplot(fig)

elif option == 'Content rating':
  df_groupby = df.groupby('ContentRating')['Rating'].sum()
  df_groupby = df_groupby.sort_values(ascending=False)
  st.write(df_groupby)

  # plot the result
  fig, ax = plt.subplots()
  df.groupby(['ContentRating','RatingLabel']).count()['Rating'].unstack().plot(ax=ax)
  st.pyplot(fig)