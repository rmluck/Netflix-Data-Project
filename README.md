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

### Start program

Run __netflix_viewing_activity.py__.

In the opened terminal, the program will display the following message asking you to enter your data file:

```
Enter .csv file containing viewing activity: |
```