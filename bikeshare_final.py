#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city=input("Please enter one of the following cities you want to see data for:\n Chicago, New York City,or Washington\n")
        city=city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid input. Please enter a valid city.")
            
    # Get user to filter by month, day, or none.
    while True:
        month = input("Please enter the month you want to explore. If you do not want a month filter enter 'all'. \nChoices: All, January, February, March, April, May, June\n")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Please enter a valid month.')
   # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Do you want details specific to a particular day? If yes, type day name else type 'all'.\nChoices: All, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n")
        day = day.lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid input. Please enter a valid day")
    print('-'*40)
    return city, month, day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #loading the data set
    df = pd.read_csv(CITY_DATA[city])
    
    #conversion of time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #extracting day from start time
    df['day_of_week'] = df['Start Time'].dt.day_name
    #extracting month from start time
    df['month'] = df['Start Time'].dt.month
    #extracting hour from start time
    df['hour'] = df['Start Time'].dt.hour
    # filter by day of week if applicable
    
        # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day.title()]

    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Check if the DataFrame is empty
    if df.empty:
        print('No data available for the selected filters.')
        return

    # display the most common month
    common_month = df['month'].mode()
    if len(common_month) > 0:
        common_month = common_month[0]
        print(f'The most common month is {common_month}')
    else:
        print('No data available for the selected month.')


    # display the most common day of week
    common_day=df['day_of_week'].value_counts().idxmax()
    print(f'The most common day is {common_day}')


    # display the most common start hour
    common_start_hour=df['hour'].mode()[0]
    print(f'The most common start hour is {common_start_hour}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # Check if the DataFrame is empty
    if df.empty:
        print('No data available for the selected filters.')
        return

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()
    if len(common_start_station) > 0:
        common_start_station = common_start_station[0]
        print(f'The most commonly used start station is {common_start_station}')
    else:
        print('No data available for the selected start station.')

    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0]
    print(f'The most commonly used end station is {common_end_station}')


    # display most frequent combination of start station and end station trip
    combined_end_start_station=df[['Start Station', 'End Station']].mode().loc[0]
    print(f'The most common combination of start and end stations is {combined_end_start_station}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time= df['Trip Duration'].sum()
    print(f'The total travel time is {total_travel_time/60} minutes')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The mean travel time is {mean_travel_time/60}, minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(f'The count of user types is {user_types}')
    
    # Check if the 'Birth Year' column has any values
    if df['Birth Year'].isnull().all():
        print('No birth year data available for the selected filters.')
        return
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'The count of Gender is {gender_counts}')
    else:
        print('No data available for the selected filters.')
    

    # Display earliest, most recent, and most common year of birth
    
    #earliest year of birth
    earliest_birth_year = df['Birth Year'].min()
    print(f'The earliest year of birth is {earliest_birth_year}')
    
    #most recent birth of year
    recent_birth_year = df['Birth Year'].max()
    print(f'The most recent year of birth is {recent_birth_year}')
    
    #most common year of birth
    common_birth_year = df['Birth Year'].mode()[0]
    print(f'The most common year of birth is {common_birth_year}')
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def raw_data (df):
    """Displays the data due filteration.
    5 rows will added in each press"""
    print('press enter to see row data, press no to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))


# In[ ]:


def display_data(df):
    # Display.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to display data forindividual trips? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

