
from urlextract import URLExtract
extract = URLExtract()

import matplotlib.pyplot as plt

from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


# 1st Class for fetch_stats

def fetch_stats(selected_user,df):
# If we wanted to all group members chat 
    if selected_user =='Overall':
# .shape() return number of rows and columns, .shape[0] means only return rows.
        # Fetch number of messages
        num_messages = df.shape[0]

        # Number of words
        words=[]
        for i in df['message']:
            words.extend(i.split())
        
        # Fetch number of media messages
        num_media_messages =df[df['message']=='<Media omitted>\n'].shape[0]
        
        # Fetch number of links shared
        links =[]
        for i in df['message']:
            links.extend(extract.find_urls(i))
        
        return num_messages, len(words),num_media_messages,len(links)
    
    # If we wanted to select specified group member 
    else:
        # Specified selected user totall messages
        num_messages=df[df['user']==selected_user].shape[0]
        # Specified selected user totall number of word
        words=[]
        for i in df[df['user']==selected_user]['message']:
            words.extend(i.split())
        # Specified selected user media messages
        num_media_messages=df[df['user']==selected_user][df['message']=='<Media omitted>\n'].shape[0]

        links =[]
        for i in df[df['user']==selected_user]['message']:
            links.extend(extract.find_urls(i))
        
        return num_messages,len(words),num_media_messages,len(links)
    

# 2nd Class for Active user
def most_active_user(df):
    x=df['user'].value_counts().head()
    dfd=round((df['user'].value_counts()/ df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})

    return x,dfd


# 3rd class for wordcloud
def create_wordcloud(selected_user, df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

# 4th Class for most common words
def most_common_words(selected_user, df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]
    

    temp=df[df['user'] !='group_notification']
    temp=temp[temp['message'] !='<Media omitted>\n']

    words_most=[]
    for i in temp['message']:
        words_most.extend(i.split())
    most_common_df=pd.DataFrame(Counter(words_most).most_common(20))

    return most_common_df

# 5th class 
def emoji_helper(selected_user, df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    emojis=[]
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# 6th class for Timeseries of message
def month_timeline(selected_user, df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    timeline=df.groupby(['year','month']).count()['message'].reset_index()
    duration=[]
    for i in range(timeline.shape[0]):
        duration.append(timeline['month'][i]+"-"+ str(timeline['year'][i]))
    timeline['duration']= duration
    return timeline


 # 7th class for Daily timeline
def daily_timeline(selected_user, df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    date_timeline=df.groupby(['year','month','day']).count()['message'].reset_index()

    date=[]
    for i in range(date_timeline.shape[0]):
    #date.append(date_timeline['year'][i]+"-"+ str(timeline['year'][i]))
        date.append(date_timeline['day'][i]+"-"+date_timeline['month'][i]+"-"+str(date_timeline['year'][i]))

    date_timeline['date']= date

    return date_timeline

# 8th class for Activity Day
def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    day_map = df['day'].value_counts()
    return day_map

# *th class for Activity month
def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df= df[df['user']==selected_user]

    day_map = df['month'].value_counts()
    return day_map  
