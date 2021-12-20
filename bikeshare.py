# Modules
import time
import pandas as pd
from colorama import Fore

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


logo = f"""{Fore.CYAN}
█▀▄ ▀ █ ▄▀ █▀▀ ▄▀▀ █   ▄▀▄ █▀▀▄ █▀▀
█▀█ █ █▀▄  █▀▀  ▀▄ █▀▄ █▀█ █▐█▀ █▀▀
▀▀  ▀ ▀ ▀  ▀▀▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀▀ ▀▀▀\n{Fore.RESET}Made by Soliman2020"""



print(logo)
print('\n        __ Let\'s analyze some US bikeshare data __        \n')

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
        entry_city=input('\nEnter a number to select one of the following cities:\n\n[1] -  Chicago\n[2] -  New York City\n[3] -  Washington      >>>   ')
        try:
            city = CITY_select[entry_city]
            print('-'*20)
            print('The target city: ',city)
            print('-'*30)
            break
        except KeyError:
            print('\nPlease enter only a number (1,2 or 3) \n')
                   
    # get user input for a month exists in the csv sheets.
    while True:
        print()
        month_message=(
            'Now, please enter a number to apply the month filter:\n\n'
            '[1] -  *All months* (no filter)\n'
            '[2] -   January\n'
            '[3] -   February\n'
            '[4] -   March\n'
            '[5] -   April\n'
            '[6] -   May\n'
            '[7] -   June      >>>   '
                    )
        entry_month=input(month_message)
        try:
            month = month_select[entry_month]
            print('-'*20)
            print('The target month(s): ',month)
            print('-'*30)
            break
        except KeyError:
            print('\nPlease enter only a number from 1 to 7 \n')

 
    # get user input for day of week (All, monday, tuesday, ... sunday).

    while True:
        print()
        day_message=(
        'Last step, enter a number to apply the day filter:\n\n'
        '[1] - *All days* (no filter)\n'
        '[2] -  Monday\n'
        '[3] -  Tuesday\n'
        '[4] -  Wednesday\n'
        '[5] -  Thursday\n'
        '[6] -  Friday\n'
        '[7] -  Saturday\n'
        '[8] -  Sunday      >>>   '   
                    )
        entry_day=input(day_message)
        try:
            day = day_select[entry_day]
            print()
            print('-'*55)
            print(f'Processing data for\nCity: {city} - Month(s): {month} - Day(s): {day}')
            break
        except KeyError:
            print('\nPlease enter only a number from 1 to 8 \n')
    
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

        # TODO: Checking errors (duplicates ,NaN or wrong data types) in the data frame.
    # print(df.info())
    # print()

    # # TODO: Missing data counter before any fix.
    # print('NaN_Before_Fix= ',df.isnull().sum().sum())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
   
    if city!="Washington": 
        ## Fix NaN issue for (Gender) by Forward Fill.
        df['Gender']=df['Gender'].fillna(method = 'ffill', axis = 0)
        ## Fix NaN issue for (User Type) by Forward Fill.
        df['User Type'] = df['User Type'].fillna(method = 'ffill', axis = 0)
        ## Fix NaN issue for (Birth Year) by doing mean.
        mean_birth= df['Birth Year'].mean()
        df['Birth Year']=df['Birth Year'].fillna(mean_birth)
        # Convert the Birth Year column to integer
        df['Birth Year']= df['Birth Year'].astype(int)

    # # TODO: Missing data counter after our fix.
    # print('NaN_After_Fix =',df.isnull().sum().sum())

    # # Checking for duplicates and do fixing in case of we had some:
    # print('Duplicated_data = ',sum(df.duplicated()))
    df.drop_duplicates(inplace=True)

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

    """ Displays statistics on the most frequent times of travel.
        
        Args: 
        (DataFrame) df - DataFrame created depending on previous filters.
    
    """

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

    """ Displays statistics on the most, least popular stations and trip.
        
        Args: 
        (DataFrame) df - DataFrame created depending on previous filters.
    
    """

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

    """ Displays statistics on the total and average trip duration.
        
        Args: 
        (DataFrame) df - DataFrame created depending on previous filters.
    
    """

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

    """ Displays statistics on bikeshare users.
    
        Args: 
        (DataFrame) df - DataFrame created depending on previous filters.
        (str) city - name of the city to apply an extra filter.
    
    """

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
        print('\nEarliest, most recent and most common year of birth:\n')
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

        Args:
        (DataFrame) df - DataFrame created depending on previous filters.

     '''

    while True:
        desire = input('Do you want to check the top 5 lines of raw data? Enter \'yes\' to confirm or any other entry to skip. >>  ')
        if desire.lower() != 'yes':
            break
        else:
            x=0
            while x<len(df):
                Y=df.iloc[x:x+5]
		pd.set_option('display.max_columns',20)  # to display the complete/undiducted table and avoid the collapsed columns.
                print(Y)
                need_more=input('\nWanna display the next 5 rows data? Enter \'yes\' to confirm or any other entry to skip. >>  ')
                if need_more.lower()=='yes':
                    x+=5
                else:
                    break
            break
    
    print('-'*40)
            
def main():

    ''' Main function that links all of our functions to work together and do the asked calculations.  
    '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        row_data(df)

        restart = input('\nWould you like to restart? Enter \'yes\' to confirm or any other entry to shutdown. \n')
        if restart.lower() != 'yes':
            print('___ Thanks ___')
            break

if __name__ == "__main__":
	main()
