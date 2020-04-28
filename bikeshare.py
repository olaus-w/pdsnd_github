#tested using python 3.5.6, numpy 1.13.3, and pandas 0.22.0
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
    city = ''
    month = ''
    day = ''
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not city:
        text = input('Which city would you like to view data for? Enter "Chicago", "New York City", or "Washington": ' ).lower()
        if text in valid_cities:
            city = text
        else:
            print('That entry is not a valid selection, please try again.')
    # get user input for month (all, january, february, ... , june)
    #limited filter options to available date range in the data set
    while not month:
        text = input('Data is available for January through June. Which month would you like to view data for? Enter "all" or a specific month eg "January" : ' ).lower()
        if text in valid_months:
            month = text
        else:
            print('That entry is not a valid, please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while not day:
        text = input('Which day of the week would you like to view data for? Enter "all" or a specific day such as "Tuesday": ').lower()
        if text in valid_days:
            day = text
        else:
            print('That entry is not a valid, please try again.')

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
    df = pd.read_csv(CITY_DATA[city])
    #convert Start Time to datetime for filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #add columns for filters to match on
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #filter by month and day if not all
    #limited index options to available date range in the data set
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = 1 + months.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month_index]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if "all" selected
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('The most popular month to take a trip is {}'.format(popular_month))
    else:
        print('A filter has been set for month so most popular month is supressed.')

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day of the week to start a trip is {}'.format(popular_day))
    else:
        print('A filter has been set for day of the week so most popular day is supressed.')


    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour to start a trip is {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('The most popular station to start a trip at is {}'.format(popular_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular station to end a trip at is {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start and End'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Start and End'].mode()[0]
    print('The most frequent start and stop station combination is {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {}'.format(total_travel_time))
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is {}'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = pd.Series.value_counts(df['User Type'])
    print('User type counts for this data query are as follows:\n', user_types)

    # Display counts of gender
# check for data present, breaks on Washington
    if city != 'washington':
        user_genders = pd.Series.value_counts(df['Gender'])
        print('User gender counts for this data set are as follows:\n', user_genders)

        # Display earliest, most recent, and most common year of birth
        most_common_birth = df['Birth Year'].mode()[0]
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        print('The most common birth year in this data set is {}, the earliest birth year is {}, and the most recent birth year is {}'.format(
        most_common_birth, earliest_birth_year, most_recent_birth_year))

    else:
        print('Gender and birth year data are not available for this city')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_raw_data(df):
    """Displays the raw data 5 lines at a time as requested by user"""
    prompt = input('Would you like to see the raw data five rows at a time ("yes" to view, any other text will skip this section)?')
    if prompt == 'yes':
        print(df.shape)
        i = 0
        while i < df.shape[0]:
            print(df.iloc[i: i + 5])
            more = input('If you are finished viewing the raw date type "q"')
            i += 5
            if more.lower() == 'q':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        disp_raw_data(df)
        restart = input('\nIf you would like to restart enter "yes", any other text will trigger exit. :\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
