"""
Course Name:    Programming for Data Science with Python
Programmer:     Akshat Johari
Project:        Explore US Bikeshare Data
Date Completed: 23-05-2020

Date Updated: 25-05-2020
Changes Made:
    1. Correct case-sensitivity for input from user
    2. Fixed error when input was 'Washington'
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = input("\nToday, you can select one of three cities to view bikehare data:\n1. Chicago\n2. Washington\n3. New York City\nPlease enter which city data you would like to see:\n")
    
    while city.lower() not in ("chicago", "washington", "new york city"):
        city = input("\nSorry, that seems to be an incorrect repsonse.\nPlease check that you are spelling the name of the city correctly.\n")
        
    while True:
        try:
            fil = int(input("\nDo you wish to filter the data? It can be done in the following ways:\n1. Month\n2. Day\n3. None\nPlease enter 1, 2, or 3: \n"))
            if fil not in (1,2,3):
                print("Invalid entry.")
                continue
        except ValueError:
            print("Invalid entry. Try again!\n")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    
    if fil == 1:
        month_dict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6}
        month = input("\nEnter the preferred month: \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \n").title()
        while month not in month_dict.keys():
            month = input("You seem to have entered an incorrect response. Please try again. You must enter your selection like 'Jan' or 'Feb'.\n")
        print("\nTo recap, you have decided to view data for {}, and filter by month = {}. If you've changed your mind, restart now!".format(city, month))
        month = month_dict[month]
    else:
        month = "all"

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if fil == 2:
        day_dict = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        day = input("\nEnter day:\nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nSunday \n").title()
        while day not in day_dict.keys():
            day = input("You seem to have entered an incorrect response. Please try again. You must enter your selection like 'Monday' or 'Thursday'.\n")
        print("\nTo recap, you have decided to view data for {}, and filter by day = {}. If you've changed your mind, restart now!".format(city, day))
        day = day_dict[day]
    else:
        day = "all"
    
    if fil == 3:
        print("\nTo recap, you have decided to view data for {}, and not apply a filter. Daring today, aren't we?".format(city))
    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Day"] = df["Start Time"].dt.dayofweek # creates a day column
    df["Month"] = df["Start Time"].dt.month	# creates a month column
    
    if month != "all":
        df = df[df["Month"] == month]
        
    if day != "all":
        df = df[df["Day"] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['Month'].mode()[0]
    print("The most popular month for bike travel is {}.\nThis may not reflect the most common month overall, depending on your filter choice".format(month_dict[popular_month]))

    # TO DO: display the most common day of week
    popular_day = df["Day"].mode()[0]
    print("The most popular day for bike travel is {}. Again, this might not be the most popular day overall, depending on filters.".format(day_dict[popular_day]))

    # TO DO: display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]
    print("The most popular hour for bike travel is {}:00 (in 24 hour format). If you wish to find the overall most active time, please choose to restart at the end, and remove the filter.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df["Start Station"].mode()[0]
    print("The most common start station is {}".format(popular_start))
    # TO DO: display most commonly used end station
    popular_end = df["End Station"].mode()[0]
    print("The most common end station is {}".format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    df["Combo Route"] = df["Start Station"] + ' - ' + df["End Station"]
    popular_route = df["Combo Route"].mode()[0]
    print("The most common start-end combination is {}".format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df["Trip Duration"].sum()
    print("The total travel time is {}".format(time.strftime('%H:%M:%S', time.gmtime(total_time))))

    # TO DO: display mean travel time
    avg_time = df["Trip Duration"].mean()
    print("The average travel time is {}".format(time.strftime('%H:%M:%S', time.gmtime(avg_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_df = df["User Type"].value_counts().rename_axis('User Types').reset_index(name='Count')
    print("User type counts, in tabular format:\n")
    print(user_types_df)

    # TO DO: Display counts of gender
    try:
        gender_df = df["Gender"].value_counts().rename_axis("Gender").reset_index(name='Count')
        print("\nGender distribution:\n")
        print(gender_df)
    except KeyError:
        print("\nGender data not available for this selection.\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        oldest = str(df["Birth Year"].min())
        youngest = str(df["Birth Year"].max())
        common = str(df["Birth Year"].mode()[0])
        print("\nThe oldest user in our database was born in {}.\nThe youngest was born in {}.\nThe most common year of birth for our users is {}.".format(oldest[:4], youngest[:4], common[:4]))
    except KeyError:
        print("\nYear of birth data unavailable for this selection.\n")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_choice = input("Would you like to see raw data? Y/N:\n")
        i = 0
        flag = 0
        # flag to check if any raw data is seen by the user
        backup = pd.read_csv(CITY_DATA[city.lower()])
        while raw_choice in ("Y", "y"):
            print(backup[i:i+5])
            flag = 1
            i+=5
            raw_choice = input("Would you like to see more data? \nType Y for YES, or any other key for NO.")
        if flag == 0:
            print("You have chosen to not see raw data.")
        else:
            print("I hope the data was enlightening.")
        print("That concludes the statistics.")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
    main()
