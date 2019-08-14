import time
import pandas as pd

"""
This code was written as part of Udacity program of Data Sciences
author: bctv
Date: August 4th, 2019
Last update: August 4th, 2019
Notes:
Template was used
A function to display data was added
A function to compute statistics about rent and return was added
Data must be in same folder than the script
"""

#Holds dictionary of files supported
CITY_DATA = { '1': 'chicago.csv',
              '2': 'new_york_city.csv',
              '3': 'washington.csv' }
#Holds dictionary of months supported
MONTHS = { 'All':'all', 'January':'January', 'February':'February', 'March': 'March',
          'April': 'April', 'May': 'May', 'June': 'June', 'July': 'July', 'August': 'August',
          'September': 'September','October': 'October','November': 'November','December': 'December'}
#Holds dictionary of days supported
DAYS = { 'All': 'all' , 'Monday': 'Monday', 'Tuesday': 'Tuesday', 'Wednesday':'Wednesday',
        'Thursday':'Thursday', 'Friday':'Friday', 'Saturday':'Saturday', 'Sunday':'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    invalidInput = True
    while(invalidInput):
        city = input("Enter city: 1 = Chicago,  2 = New York City, 3 = Washington: ")
        if city in CITY_DATA.keys():
            invalidInput = False
        else:
            print('Upps! That\'s not correct, let\'s try one more time')

    # get user input for month (all, january, february, ... , june)
    invalidInput = True
    while(invalidInput):
        month = input("Enter month: all, January, February, ... , June: ")
        if month.capitalize() in MONTHS.keys():
            invalidInput = False
        else:
            print('Upps! That\'s not correct, let\'s try one more time')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    invalidInput = True
    while(invalidInput):
        day = input("Enter day of the week: all, Monday, Tuesday, ... Sunday: ")
        if day.capitalize() in DAYS.keys():
            invalidInput = False
        else:
            print('Upps! That\'s not correct, let\'s try one more time')

    print('-'*40)
    return city, month, day

def load_data(city, month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df_raw = pd.read_csv(CITY_DATA[city])

    # Convert the time coluns to datatime format
    df_raw['Start Time'] = pd.to_datetime(df_raw['Start Time'])
    df_raw['End Time'] = pd.to_datetime(df_raw['End Time'])

    # adding some new variables/columns of interest and adjusting type of var
    df_raw['Month Start Time'] = df_raw['Start Time'].dt.month_name(locale = 'English')
    df_raw['Day Start Time'] = df_raw['Start Time'].dt.weekday_name
    df_raw['Hour Start Time'] = df_raw['Start Time'].dt.hour
    df_raw['Hour End Time'] = df_raw['End Time'].dt.hour

    # filtering
    if month != 'all':
         df_raw['Month Start Time'] = df_raw['Month Start Time'] == month.capitalize()

    if day!='all':
        df_raw['Day Start Time'] = df_raw['Day Start Time'] == day.capitalize()

    return df_raw

def display_raw_data(df):
    """
    Shows data filtered by the city, month and day selected by the user - if applicable.
    Data will be displayed in chunks of 5 lines, as many times as the user requested
    If user answer to the question of showing raw data with "now", then it will skip to
    present the statistics

    Args:
        input: yes or no
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day, 5 lines at the time
    """
    # setting initial values for the loop that will display the data
    # change the end value if you want to display a different number of rows at the time
    initial = 0
    end = 5
    answer = input('\nData is ready to be used, would you like to see some of it?. Enter yes or no.\n')
    while answer.lower() == 'yes':
        print(df.iloc[initial:end])
        answer = input('\nWould you like to see more?. Enter yes or no.\n')
        if answer.lower() == 'yes':
            initial += 5
            end += 5
        else:
            answer.lower() == 'no'

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df['Month Start Time'].dtype != 'bool' or df['Day Start Time'].dtype != 'bool':
        # display the most common month if valid
        if df['Month Start Time'].dtype != 'bool':
            print('\nThe most popular month to rent bikes is:\n', df['Month Start Time'].value_counts().idxmax())

        # display the most common day of week
        if df['Day Start Time'].dtype != 'bool':
            print('\nThe most popular day in the week to rent bikes is:\n', df['Day Start Time'].value_counts().idxmax())

    # display the most common hour to rent bikes
    if df['Hour Start Time'].value_counts().idxmax() < 12:
        time_day = 'am'
    else:
        time_day = 'hrs'

    print('\nThe most popular hour to rent bikes is:\n', df['Hour Start Time'].value_counts().idxmax(),time_day)

    # display the most common hour to return bikes
    if df['Hour End Time'].value_counts().idxmax() < 12:
        time_day = 'am'
    else:
        time_day = 'hrs'

    print('\nThe most popular hour to return bikes is:\n', df['Hour End Time'].value_counts().idxmax(),time_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
        Displays statistics on the most popular stations and trip.
       Some statistics are shown in minutes and other in seconds for convenience
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most popular start station is:\n', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('\nThe most popular end station is:\n', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    df['trips'] = 'Start station: ' + df['Start Station'] + ' End station: ' + df['End Station']
    print('\nThe most popular trip was done by {} customers and it was between:\n{}'.format(df['trips'].value_counts().max(),df['trips'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total duration - in seconds - of all travels is {}, equivalent to {} hours'.format(df['Trip Duration'].sum(), round(df['Trip Duration'].sum()/3600,1)))

    # display mean travel time
    print('\nThe average duration in minutes of all travels is {}'.format(round((df['Trip Duration']/60).mean()),1))

    # display min travel time
    print('\nThe shortest duration in seconds of all travels is {}'.format(round(df['Trip Duration'].min()),1))

    # display max travel time
    print('\nThe longest duration in seconds of all travels is {}'.format(round(df['Trip Duration'].max()),1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nDistribution by types of users:\n',df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nDistribution by gender:\n',df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe younger customer born in {}'.format(int(df['Birth Year'].max())))
        print('\nThe oldest customer born in {}'.format(int(df['Birth Year'].min())))
        print('\nThe customer(s) that born in {} are the ones who rent more bikes with a total of {} times rented so far'.format(int(df['Birth Year'].value_counts().idxmax()),df['Birth Year'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rent_stats(df):
    """Displays statistics on bikeshare rents."""

    print('\nCalculating Stats on Bikeshare Rents...\n')
    start_time = time.time()

    # Information about the most recent rent
    print('\nCalculating Stats on the most recent rent...\n')
    print('\nThe most recent rent of a bike was {}'.format(df['Start Time'].max()))

    if 'Gender' in df.columns:
        print('\nThe gender of the customer that rented the bike is {}'.format(df['Gender'][df['Start Time'] == df['Start Time'].max()].to_string(index = False)))
    if 'Birth Year' in df.columns:
        print('\nThe customer was born in{}'.format(df['Birth Year'][df['Start Time'] == df['Start Time'].max()].to_string(index = False)))

    print('\nThe station where the bike was rented was{}'.format(df['Start Station'][df['Start Time'] == df['Start Time'].max()].to_string(index = False)))
    print('\nThe station where the bike was rented was{}'.format(df['End Station'][df['Start Time'] == df['Start Time'].max()].to_string(index = False)))

    # Information about the latest time a bike was return
    print('\nCalculating Stats on the latest time of return...\n')
    print('\nThe latest return of a bike was {}'.format(df['End Time'].max()))

    if 'Gender' in df.columns:
        print('\nThe gender of the customer that rented the bike is {} '.format(df['Gender'][df['End Time'] == df['End Time'].max()].to_string(index = False)))
    if 'Birth Year' in df.columns:
        print('\nThe customer was born in {}'.format(df['Birth Year'][df['End Time'] ==df['End Time'].max()].to_string(index = False)))

    print('\nThe station where the bike was returned was {}'.format(df['Start Station'][df['End Time'] == df['End Time'].max()].to_string(index = False)))
    print('\nThe station where the bike was returned was {}'.format(df['End Station'][df['End Time'] == df['End Time'].max()].to_string(index = False)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rent_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
