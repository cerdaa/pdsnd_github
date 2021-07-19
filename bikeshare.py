# Author: Andres Cerda
# Last update: 7/9/2021

import time
import pandas as pd
import numpy as np
import os

# Dictionaries and lists for menus and options

CITY_DATA = { 1: ('Chicago','chicago.csv'),
              2: ('New York City', 'new_york_city.csv'),
              3: ('Washington', 'washington.csv')
                 }

MAIN_MENU = ['New Analysis', 'Exit Tool']
CITY_LIST = ['Chicago', 'New York City', 'Washington', 'Main Menu']
MONTHS_LIST = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Main Menu']
DAYS_LIST = ['All','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Main Menu']

def menu(menu_list, menu_title, input_label, first_value, last_value):
    """
    Displays a menu and request valid selection.
    Arguments:
             (list) menu_list - A list with the labels of each option. The first element is the name/descrption of the menu
             (str) input_label - A string with the label tha will be displayed requesting a reponse.
             (int) first_value - The first valid value
             (int) last_value - The last valid value
    Returns: (int) selection - the selected value
    """

    print('-'*80)
    print(menu_title + "\n")

    i = 0
    for menu_item in menu_list:
        print(str(i) + ' - ' + str(menu_list[i]))
        i += 1

    print('-'*80)
    print('\n')

    while True:
        selection = input(input_label+': ')
        try:
            selection = int(selection)
        except:
            print('Invalid entry. Please try again.')
        else:
            if first_value <= selection <= last_value:
                break
            else:
                print('Invalid entry. Please try again.')

    print('-'*80)
    return selection

def screen_clear():
   # Clears the screen
   # Credit to: https://www.tutorialspoint.com/how-to-clear-screen-in-python
   if os.name == 'posix':
      cls_var = os.system('clear')
   else:
      # for windows platfrom
      cls_var = os.system('cls')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city_selection - index of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = 4
    month = 13
    day = 8

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    screen_clear()
    city = menu(CITY_LIST, "Available Cities", "What city do you want to analyze? Enter the number of your selection", 0, 3)

    # TO DO: get user input for month (all, january, february, ... , june)
    if city != 3:
        screen_clear()
        month = menu(MONTHS_LIST, 'Analysis for city: {}'.format(CITY_DATA[city+1][0]), "What period of time do you want to analyze? Enter the number of your selection", 0, 13)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        if month != 13:
            screen_clear()
            day = menu(DAYS_LIST, 'Analysis for city: {} for month: {}'.format(CITY_DATA[city+1][0], MONTHS_LIST[month]), "What day of the week do you want to analyze? Enter the number of your selection", 0, 8)

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
    df = pd.read_csv(CITY_DATA[city][1])

    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 0:
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 0:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==DAYS_LIST[day]]
    return df

def display_row_data(df):
    """Prompts for the option to view raw data, continue viwing stats or going to the main menu. It displays 5 rows at a time.
    Args:
        (dataframe) df - Pandas DataFrame with data to display.

    """

    while True:
        continue_flag = input('Press 0 to continue running stats, 1 to view raw data or 2 to exit to main menu: ')
        try:
            continue_flag = int(continue_flag)
        except:
            print('Invalid entry. Please try again.')
        else:
            if 0 <= continue_flag <= 2:
               break
            else:
                print('Invalid entry. Please try again:')

    if continue_flag == 1:
        first_row = 0
        while True:
            print(df.iloc[first_row:first_row+5])
            keep_printing = input('Press 0 to continue running stats, 1 to continue viewing raw data (5 next rows): ')
            while True:
                try:
                    keep_printing = int(keep_printing)
                except:
                    print('Invalid entry. Please try again:')
                else:
                    if 0 <= keep_printing <= 1:
                        break
                    else:
                        print('Invalid entry. Please try again:')
            if keep_printing == 1:
                first_row += 5
            else:
                break
        return True
    elif continue_flag == 2:
        return False
    else:
        return True

def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - Pandas DataFrame with data to display
    Returns:
        False: if the users select not to continue
        True:  if the users wants to continue
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: ' + MONTHS_LIST[df['month'].value_counts().idxmax()])
    print('The number of incidences is: ' + str(df['month'].value_counts().max()))

    # TO DO: display the most common day of week
    print('The most common day of week is: ' + str(df['day_of_week'].value_counts().idxmax()))
    print('The number of incidences on that day is: ' + str(df['day_of_week'].value_counts().max()))

    # TO DO: display the most common start hour
    print('The most common start hour is: ' + str(df['start_hour'].value_counts().idxmax()) + ':00')
    print('The number of incidences at that hour is: '+ str(df['start_hour'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return display_row_data(df)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) df - Pandas DataFrame with data to display
    Returns:
        False: if the users select not to continue
        True:  if the users wants to continue
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common used start station is: ' + str(df['Start Station'].value_counts().idxmax()))
    print('The number of incidences in that station is: ' + str(df['Start Station'].value_counts().max()))

    # TO DO: display most commonly used end station
    print('The most common used end station is: ' + str(df['End Station'].value_counts().idxmax()))
    print('The number of incidences in that station is: ' + str(df['End Station'].value_counts().max()))

    # TO DO: display most frequent combination of start station and end station trip
    print('The most frequent combination of start and end station is: ' + str(df.groupby(['Start Station'])['End Station'].value_counts().idxmax()))
    print('The number of incidences of such combination is: ' + str(df.groupby(['Start Station'])['End Station'].value_counts().max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return display_row_data(df)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (dataframe) df - Pandas DataFrame with data to display
    Returns:
        False: if the users select not to continue
        True:  if the users wants to continue
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time is: ' + "{:.2f}".format(df['Trip Duration'].sum()/60) + ' min')


    print('The shortest travel time is: ' + "{:.2f}".format(df['Trip Duration'].min()/60) + ' min')
    print('The largest travel time is: ' + "{:.2f}".format(df['Trip Duration'].max()/60) + ' min')

    # TO DO: display mean travel time
    print('The mean travel time is: ' + "{:.2f}".format(df['Trip Duration'].mean()/60) + ' min')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return display_row_data(df)

def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (dataframe) df - Pandas DataFrame with data to display
    Returns:
        False: if the users select not to continue
        True:  if the users wants to continue
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts())
    print('\n')

    # TO DO: Display counts of gender
    try:
        print('Counts of gender:')
        print(df['Gender'].value_counts())
        print('\n')
    except:
        print('This city does not have gender information')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('Birthday information:')
        print('The earliest year of birth is: ' + str(int(df['Birth Year'].min())))
        print('The most recent year of birth is: ' + str(int(df['Birth Year'].max())))
        print('The most common year of birth is: ' + str(int(df['Birth Year'].mode())))
    except:
        print('This city does not have birthday information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return display_row_data(df)

def main():

    while True:
        screen_clear()
        print('-'*80)
        print('-'*25 + ' US Bikeshare Analytical Tool ' + '-'*25)
        print('-'*80)

        selection = menu(MAIN_MENU, "Main Menu", "Enter your selection", 0, 1)

        if selection == 0:
            city, month, day = get_filters()
            if city < len(CITY_DATA) and month < 13 and day < 8:
                screen_clear()
                print('-'*80)
                print('City: ' + CITY_LIST[city])
                print('Month: ' + MONTHS_LIST[month])
                print('Day: ' + DAYS_LIST[day])
                print('-'*80)
                df = load_data(city+1, month, day)
                if time_stats(df):
                    if station_stats(df):
                        if trip_duration_stats(df):
                            user_stats(df)
        else:
            break

if __name__ == "__main__":
	main()
