import re
import pandas as pd


def preprocess(data):
    pattern =r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    date=[]
    times=[]
    for i in dates:
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])
   
    time=[]
    for i in times:
        time.append(i.split("\u202f")[0])

    # Create dataframe using dictionary
    df = pd.DataFrame({
        'User_Messages':messages,
        'Message_Date':date,
        'time': time,
        })
    
    df.rename(columns={'Message_Date': 'date'}, inplace=True)


#Separate Users and Messages From User_Messages
    users =[]
    messages=[]

    for i in df['User_Messages']:
        whole_messages = re.split('([\w\W]+?):\s',i)
        if whole_messages[1:]:
            users.append(whole_messages[1])
            messages.append(whole_messages[2])
        else:
            users.append('group_notification')
            messages.append(whole_messages[0])

        
    df['user']= users
    df['message']= messages
    df.drop(columns=['User_Messages'], inplace=True)

    # Separates Day,Month, and Years from Date column
    df['date']=pd.to_datetime(df['date'])
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()

    df['time'] = pd.to_datetime(df['time'])
    df['hour']= df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    df.head(10)

    return df