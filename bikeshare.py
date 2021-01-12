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

    # Prompt and get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to review data?\n")
        city = city.lower() #Accept lower case input.
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("\nInvalid. Try again. Please enter a name of city from three choices above\n")

    # Prompt and get user input for month in the first 6 months (all, january, february, ... , june)
    while True:
        month = input("\nDo you want details data of a specific month? If yes, type the month name of the first 6 months, or type 'all' for all 6 months\n")
        month = month.lower() #Accept lower case input.
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("\nInvalid. Try again. Please enter a name in the first 6 months or all for all 6 months.\n")

    # Prompt and get user input for day in a week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nDo you want details data of a specific day? If yes, type a day name or type 'all' for all the whole week\n")
        day = day.lower() #Accept lower case input.
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid. Try again. Please enter a name of the day in a week or all the whole week")

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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Format the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day in a week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # By month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # By month--create the new dataframe
        df = df[df['month'] == month]

    # By day of week if applicable
    if day != 'all':
        # By day in a week--create the new dataframe

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nThe Most Frequent Times of Travel...\n')
    start_time = time.time()

    # The most common month
    print("The most common month: ", df['month'].mode()[0], "\n")

    # The most common day of week
    print("The most common day of week:", df['day_of_week'].mode()[0], "\n")

    # The most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip:\n')
    start_time = time.time()

    # The most commonly used start station
    print("The Most Commonly Start Station: ", df['Start Station'].mode()[0], "\n") #Use mode method

    # The most commonly used end station
    print("The most commonly end station: ", df['End Station'].mode()[0], "\n") #Use mode method

    # The most frequent of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The Most Frequent of Start Station and End Station: ", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total Travel Time
    print("The total travel time: ", df['Trip Duration'].sum(), "\n") #Use sum method

    # Average total time
    print("The average trip duration: ", df['Trip Duration'].mean()) #Use mean method to get average

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nUser Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Display counts of gender
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        most_recent_year_of_birth = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        print("The most recent year of birth is ", most_recent_year_of_birth, "\n")

        earliest_year_of_birth = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        print("The earliest year of birth is ", earliest_year_of_birth, "\n")

        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("The most common year of birth is ", most_common_year_of_birth, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Give user an option to view raw detail data.
    data = 1
    while True:
        raw_detail = input('\n Would you like to see some raw detail data? Enter yes or no.\n')
        if raw_detail.lower() == 'yes': #accept user input for yes and no answer when prompting if
        # want to view raw data before computation.
            print(df[data:data+7])
            data = data+7 #change data output from 5 rows to 7 rows.
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
