import time
import pandas as pd

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

CITY_select = { '1': 'Chicago',
                '2': 'New York City',
                '3': 'Washington' }

month_select = { '1':'All','2':'January','3':'February','4':'March',
                 '5':'April','6':'May','7':'June' }

day_select = {'1':'All', '2':'Monday','3':'Tuesday','4':'Wednesday',
              '5':'Thursday','6':'Friday','7':'Saturday','8':'Sunday'}


print('\n        __ Let\'s explore some US bikeshare data __        \n')

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "All" to apply no month filter
    (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """

    # get user input for city. 
    while True:
        entry_city=input('Enter a number (from 1 to 3) to select the wanted city:\n\n1:  Chicago\n2:  New York City\n3:  Washington      >>>   ')
        try:
            city = CITY_select[entry_city]
            print('-'*20)
            print('The target city: ',city)
            print('-'*30)
            break
        except KeyError:
            print('\nPlease enter only a number from 1 to 3 !\n')
                   
    # get user input for a month exists in the csv sheets.
    while True:
        print()
        month_message=(
            'Enter a number (from 1 to 7) to select the wanted month:\n\n'
            '1:  *All months*\n'
            '2:  January\n'
            '3:  February\n'
            '4:  March\n'
            '5:  April\n'
            '6:  May\n'
            '7:  June      >>>   '
                    )
        entry_month=input(month_message)
        try:
            month = month_select[entry_month]
            print('-'*20)
            print('The target month(s): ',month)
            print('-'*30)
            break
        except KeyError:
            print('\nPlease enter only a number from 1 to 7 !\n')

 
    # get user input for day of week (All, monday, tuesday, ... sunday).

    while True:
        print()
        day_message=(
        'Enter a number (from 1 to 8) to select the wanted day:\n\n'
        '1: *All days*\n'
        '2: Monday\n'
        '3: Tuesday\n'
        '4: Wednesday\n'
        '5: Thursday\n'
        '6: Friday\n'
        '7: Saturday\n'
        '8: Sunday      >>>   '   
                    )
        entry_day=input(day_message)
        try:
            day = day_select[entry_day]
            print()
            print('-'*55)
            print('Processing data for\nCity: {} - Month(s): {} - Day(s): {}'.format(city,month,day))
            break
        except KeyError:
            print('\nPlease enter only a number from 1 to 8 !\n')
    
    print('-'*55)
    return city, month, day

def load_data(city,month,day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day Name'] = df['Start Time'].dt.day_name()
    df['Start Hour']=df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All': #and month in df['Month']:
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['Day Name']== day]
    
    return df

def time_stats(df):

    """ Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('* Most common month:                  ', most_common_month)
    # display the most common day of week
    most_common_day = df['Day Name'].mode()[0]
    print('* Most common day:                    ', most_common_day)
    # display the most common start hour
    most_common_start_hour = df['Start Hour'].mode()[0]
    print('* Most common start hour:             ', most_common_start_hour)

    print("\nProcess took {0:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """ Displays statistics on the most, least popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].mode()[0]
    print('* Most commonly used start station:   ',common_start_station)
    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0]
    print('* Most commonly used end station:     ',common_end_station)
    print()
    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('* Most common trip from start to end :\n',common_trip)
    print()
    # display least commonly used start station
    lcommon_start_station=df['Start Station'].value_counts().idxmin()
    print('Least commonly used start station:    ',lcommon_start_station)
    # display least commonly used end station
    lcommon_end_station=df['End Station'].value_counts().idxmin()
    print('Least commonly used end station:      ',lcommon_end_station)
 
    print("\nProcess took {0:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):

    """ Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_total=df['Trip Duration'].sum()
    print('* Total travel time:          {0:.1f} min.'.format(travel_time_total/60))  
    # display mean travel time
    travel_time_avg=df['Trip Duration'].mean()
    print('* Average travel time:        {0:.1f} min.'.format(travel_time_avg/60))
    # display maximum travel time
    travel_time_max=df['Trip Duration'].max()
    print('* Maximum travel time:        {0:.1f} min.'.format(travel_time_max/60))
    # display minimum travel time
    travel_time_mini=df['Trip Duration'].min()
    print('* Minimum travel time:        {0:.1f} sec.'.format(travel_time_mini))

    print("\nProcess took {0:.5f} seconds.".format(time.time() - start_time))
    print('-'*40)

def user_stats(df,city):

    """ Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print()
    subscriber_count=df['User Type'].value_counts()['Subscriber']
    print('* Counts of subscribers: ',subscriber_count)
    customer_count=df['User Type'].value_counts()['Customer']
    print('* Counts of customers:   ',customer_count)
    
    try:
        dependent_count=df['User Type'].value_counts()['Dependent']
        if dependent_count>0:
            print('* Counts of dependents:  ',dependent_count)
            print('-'*40)
    except Exception:
        pass

    if city!='Washington':
        
        # Display counts of gender
        print()
        male_count=df['Gender'].value_counts()['Male']
        print('* Counts of males:   ',male_count)
        female_count=df['Gender'].value_counts()['Female']
        print('* Counts of females: ',female_count)
        print('-'*40)

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest, most recent, and most common year of birth:\n')
        common_year=df['Birth Year'].mode()[0]
        print('* Most common year of birth:   ',int(common_year))
        earliest_year=df['Birth Year'].min()
        print('* Earliest year of birth:      ',int(earliest_year))
        most_recent_year=df['Birth Year'].max()
        print('* Most recent year of birth:   ',int(most_recent_year))


    print("\nProcess took {0:.5f} seconds.".format(time.time() - start_time)) 
    print('-'*40)

def row_data(df):

    ''' Raw data is displayed upon request by the user in the following manner:
        Script prompt the user if they want to see 5 lines of raw data,
        Display that data if the answer is 'yes',
        Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
        Stop the program when the user says 'no' or there is no more raw data to display.
     '''

    while True:
        desire = input('Do you want to check the top 5 lines of raw data? Enter yes or no >>  ')
        if desire.lower() != 'yes':
            break
        else:
            x=0
            while x<len(df):
                Y=df.iloc[x:x+5]
                print(Y)
                need_more=input('Check next 5 rows data? Enter yes or no >>  ')
                if need_more.lower()=='yes':
                    x+=5
                else:
                    break
            break
    
    print('-'*40)
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('___ Thanks ___')
            break

if __name__ == "__main__":
	main()
