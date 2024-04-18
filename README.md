# Netflix Data Project

Rohan Mistry

Updated: April 16, 2024

## Overview

This project aims to analyze the viewing activity of a Netflix account, providing detailed analytics, statistics, and trends to inform the user about the way they use the Netflix service. The program was coded using Python and subsequent Python libraries such as Pandas, Matplotlib, NumPy, and Seaborn. Given a .csv file containing the viewing history of a Netflix account, this program uses past viewing data to conduct analysis and chart graphs based on viewing frequency, viewing duration, viewing location and time, most watched content, and more.

## Contents

This project contains 1 Python file and 1 csv file. The included files are listed below:

* __netflix_viewing_activity.py__: main module that runs the program which analyzes the viewing activity data provided
* __viewing_activity.csv__: sample viewing activity data used to test program

## Program

The instructions on how to run the program and how the program functions are listed below.

### Retrieving .csv file with viewing activity data

Before actually using this program, you will need to retrieve a .csv file containing the viewing activity data of your Netflix account. If you are logged into your Netflix account on your browser, you can go to the "[Get My Info](https://www.netflix.com/account/getmyinfo)" page and this page will appear:

![](/img/netflix_get_my_info_page.png)

Click the "Submit Request" button which will send a request to Netflix for your data. They will provide a downloadable report folder which contains many files, including one called __ViewingActivity.csv__. This is the file that contains the viewing activity data necessary for this project. 

### Start program and configure data

Run __netflix_viewing_activity.py__.

In the opened terminal, the program will display the following message asking you to enter your data file:

```
Enter .csv file containing viewing activity: |
```

Continue by typing in __ViewingActivity.csv__ (unless you renamed your data file):

Assuming you entered a valid filename, the program will proceed by asking you to enter your local time zone to to convert your viewing data's date and time information accordingly.

```
It is necessary to convert all of your viewing data to the correct time zone.
What is your local time zone? Specify in the format US/Eastern or US/Pacific: |
```

You need to enter your time zone in the specified format. You can use the [full list of the Pytz library's allowed time zones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568) and find yours.

I'm in the Pacific time zone so I'll use US/Pacific.

The next question the program will ask you is whether you would like the program to analyze the data pertaining to your entire Netflix account or to a specific user profile within that account.

```
Would you like to analyze your entire accuont or a specific profile (A or P)? |
```

If you answer with 'A', then the program will analyze your entire account. If you enter 'P', then the program will proceed to ask you which profile you would like to analyze:

```
This account's profiles are as follows:
    Charlie
    Ryan
```

Answer with your preferred profile and then the program will continue by asking you whether you would like the program to analyze all viewing activity or viewing activity of only movies or only TV shows. All the Netflix data is separated into movies or TV so you get to choose if you would like them to be grouped or if you want to narrow to one medium:

```
Would you like to analyze all viewing activity or your viewing activity of only movies or only TV shows (A, M, or TV)?
```

If you answer with 'A', then the program will analyze both movies and TV. If you enter 'M', then the program will only observe movies. If you enter 'TV', then the program will only observe TV.

If you choose specifically movies or TV, then the program will follow up by asking whether you would like to analyze all titles or a specific title.

For instance, if you chose movies in the previous question, then the program will show this prompt:

```
Would you like to analyze all movies or a specific title (A or S)? |
```

If you chose TV in the previous question, then the program will show this prompt:

```
Would you like to analyze all shows or a specific title (A or S)? |
```

In both scenarios, answering with 'A' means the program will analyze all titles and answering with 'S' means the program will analyze a specific title.

If you choose to analyze a specific movie, then this will be the next prompt that appears:

```
Movies you have watched:
    30 for 30: The Two Escobars
    Louis C.K.: Live at the Beacon Theater
    The Invisible War
Which title would you like to analyze? |
```

If you choose to analyze a specific show, then this will be the prompt that appears:

```
TV Shows you have watched:
    Archer
    Buffy the Vampire Slayer
    Star Trek
    The Office (U.S.)
Which title would you like to analyze? |
```

After you have answered all configuration questions, the final prompt will appear, asking you what data analysis option you would like the program to compute based on your specified data preferences:

```
Options for Data Analysis:
    Countries
    Device Types
    Duration
    Most Watched Days
    Most Watched Episodes
    Most Watched Months
    Most Watched Movies
    Most Watched Shows
    Start Times
    Total Time Watched
    Viewing Activity Timeline
    Viewing Frequency
    Viewing Heat Map
Which option would you like to choose? |
```

Depending on your configurations, a couple of these options may not show up. Enter what you would like the program to do and then the output will appear in the form of a data visualization.

Afterwards, the program will ask you whether you would like to continue:

```
Would you like to continue (Y or N)? |
```

If you choose to continue, then the process will restart (besides asking for the data file or time zone). If you choose to stop, then the program will terminate.