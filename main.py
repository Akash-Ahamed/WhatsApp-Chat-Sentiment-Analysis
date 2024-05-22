import streamlit as st 
import preprocessor, helper
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import time





col1,col2 = st.columns([0.2,1], gap="small")
with col1:
   st.image("assets\whatsapp.png", width=80, )

with col2:
    st.title("WhatsApp Chat Analyzer\n Analysis Your Group or Single Chat")


# Basic Streamlit Setting and  Load the text file.............................. 
st.sidebar.title("Analysis Your Group or Single Chat")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

# To read file as bytes. so it is a bytes data stream file, which we need to convert into string file.   
    bytes_data = uploaded_file.getvalue() 
    
# Convert to String from bytes
    data=bytes_data.decode('utf-8')
    
    #st.text(data)
    df= preprocessor.preprocess(data)

# Disply the DataFrame using streamlit
    st.subheader("Your WhatsApp Chat Messages")
    st.dataframe(df)

#..............................................................................
    

# Streamlit web page Setting.....................................................
# Find the How much user exists in the group chat using Unique() function.
    user_list= df['user'].unique().tolist()
# We remove the group_notification from the User list
    user_list.remove('group_notification')
    user_list.sort()
# First show all user as a Overall name
    user_list.insert(0,"Overall")

    
# Display the sidebar select box and Find which user now selected.
    selected_user = st.sidebar.selectbox("User :",user_list)


    
# Start Analysis Button
    if st.sidebar.button("Start Analysis"):
        
        
# Analysis Show, totall messages, number of word, number of link, number media file.........................
# Fetch the totall messages and words
        num_messages,words, num_media_messages,num_links=helper.fetch_stats(selected_user,df)

# Webpage divided into 4 columns
        st.title("Overall Analysis")
        col1, col2, col3, col4 =st.columns(4, gap="medium")
# First Columns Contains....................................................................................
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(num_links)
       
        # find the active users in the group (group level)
        if selected_user=='Overall':
            st.title("Most Active User")
            x,percentage = helper.most_active_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(percentage)
        
    # Most Common Words
        st.title("Most Common Words")
        col1, col2 = st.columns(2, gap='medium')
        
        with col1:
            most_common_df = helper.most_common_words(selected_user,df)
            st.dataframe(most_common_df)
        
        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            st.pyplot(fig)
    
    
     # Most Used Emoji
        st.title("Most Used Emoji")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2= st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(), autopct = "%0.2f")
            st.pyplot(fig)



    # Most activity map show
        st.title("Most Activity Map")
        col1, col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day= helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month= helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='Orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


     # Daily timeline
        st.title("Daily Timeline")
        date_timeline = helper.daily_timeline(selected_user, df)

        fig,ax=plt.subplots()
        ax.plot(date_timeline['date'],date_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # Wordcloud
       # st.title("Wordcloud")
       # df_wc = helper.create_wordcloud(selected_user,df)
       # fig,ax=plt.subplots()
      #  ax.imshow(df_wc)
       # st.pyplot(fig)*/


    
   
    # Timeseries of message
        st.title("Monthly Timeline")
        timeline=helper.month_timeline(selected_user,df)
        fig, ax= plt.subplots()
        ax.plot(timeline['duration'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

   
    