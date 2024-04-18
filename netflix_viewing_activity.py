"""
Analyzes personal Netflix viewing activity.
"""

# Import necessary libraries.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, timezone
pd.options.mode.chained_assignment = None


def ask_for_data() -> pd.DataFrame:
    """
    Asks for .csv file that contains viewing activity.

    Returns:
        pd.DataFrame: data from .csv file
    """

    data_file = input("Enter .csv file containing viewing activity: ")
    df = pd.read_csv(data_file)
    df = _drop_unnecessary_data(df)

    return df


def convert_times(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts timestamps to local timezone.

    Parameters:
        df (pd.DataFrame): viewing data
    
    Returns:
        pd.DataFrame: updated viewing data with times converted to local timezone
    """

    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=time_zone)

    df["start_time"] = pd.to_datetime(df["Start Time"], utc=True)
    df = df.set_index("start_time")

    print("\nIt is necessary to convert all of your viewing data to the correct time zone.")
    time_zone = input("What is your local time zone? Specify in the format US/Eastern or US/Pacific: ")
    df["Start Time"] = pd.to_datetime(df["Start Time"]).apply(utc_to_local)
    df["Start Time"] = df["Start Time"].apply(lambda x: x.strftime("%Y-%m-%d, %H:00:00"))
    df.index = df.index.tz_convert(time_zone)
    df = df.reset_index()
    df["Duration"] = pd.to_timedelta(df["Duration"])
    df["Day"] = df["start_time"].dt.dayofweek
    df["Day"] = ["Monday" if number == 0 else number for number in df["Day"]]
    df["Day"] = ["Tuesday" if number == 1 else number for number in df["Day"]]
    df["Day"] = ["Wednesday" if number == 2 else number for number in df["Day"]]
    df["Day"] = ["Thursday" if number == 3 else number for number in df["Day"]]
    df["Day"] = ["Friday" if number == 4 else number for number in df["Day"]]
    df["Day"] = ["Saturday" if number == 5 else number for number in df["Day"]]
    df["Day"] = ["Sunday" if number == 6 else number for number in df["Day"]]
    df["Date"] = pd.to_datetime(df["start_time"].dt.date)
    df = df.drop(["start_time"], axis=1)

    return df


def ask_for_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asks for profile of account to analyze.

    Parameters:
        df (pd.DataFrame): viewing data
    
    Returns:
        pd.DataFrame: updated viewing data with profile(s) that user wants to analyze
    """

    account_or_profile = ""
    while account_or_profile != "A" and account_or_profile != "P":
        account_or_profile = input("\nWould you like to analyze your entire account or a specific profile (A or P)? ")

    if account_or_profile == "P":
        print("This account's profiles are as follows:")
        profiles = [profile for profile in set(df["Profile Name"].values)]
        for profile in sorted(profiles):
            print(f"  {profile}")
        chosen_profile = ""
        while chosen_profile not in profiles:
            chosen_profile = input("Which profile would you like to analyze? ")
        df = df[df["Profile Name"] == chosen_profile]

    return df


def separate_types_of_content(df: pd.DataFrame) -> pd.DataFrame:
    """
    Separate shows from movies.

    Parameters:
        df (pd.DataFrame): viewing data
    
    Returns:
        pd.DataFrame: updated viewing data separated by type of content
    """

    names = []
    seasons = []
    episodes = []
    types = []

    for title in df.Title:
        if title.count(":") >= 2:
            names.append(title.split(":")[0])
            seasons.append(title.split(":")[1])
            episodes.append(title.split(":")[2].split(" (")[0])
            types.append("TV Show")
        else:
            names.append(title)
            seasons.append(None)
            episodes.append(None)
            types.append("Movie")

    df["Name"] = names
    df["Season"] = seasons
    df["Episode"] = episodes
    df["Type"] = types

    return df


def ask_for_content_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asks whether to analyze a show or movie.

    Parameters:
        df (pd.DataFrame): viewing data
    
    Returns:
        pd.DataFrame: updated viewing data with types of content that user wants to analyze
    """

    profile_or_account = ""
    while profile_or_account != "A" and profile_or_account != "M" and profile_or_account != "TV":
        profile_or_account = input("\nWould you like to analyze all viewing activity or your viewing activity of only "
                                   "movies or only TV shows (A, M, or TV)? ")

    if profile_or_account == "M" or profile_or_account == "TV":
        if profile_or_account == "M":
            content_type = "Movie"
        else:
            content_type = "TV Show"
        df = df[df["Type"] == content_type]
        df = ask_for_title(df, content_type)

    return df


def ask_for_title(df: pd.DataFrame, content_type: str) -> pd.DataFrame:
    """
    Asks for title to analyze.

    Parameters:
        df (pd.DataFrame): viewing data
        content_type (str): type of content that user wants to analyze
    
    Returns:
        pd.DataFrame: updated viewing data with title(s) that user wants to analyze
    """

    all_titles = ""

    if content_type == "Movie":
        all_titles = input("\nWould you like to analyze all movies or a specific title (A or S)? ")
    elif content_type == "TV Show":
        all_titles = input("\nWould you like to analyze all shows or a specific title (A or S)? ")

    if all_titles == "S":
        print(f"\n{content_type}s you have watched:")
        titles = [title for title in set(df["Name"].values)]
        for title in sorted(titles):
            print(f"  {title}")

        chosen_title = ""
        while chosen_title not in titles:
            chosen_title = input("Which title would you like to analyze? ")

        return df[df["Name"] == chosen_title]
    else:
        return df


def choose_analysis(df: pd.DataFrame) -> tuple[str, str, str, str]:
    """
    Asks how to analyze data.

    Parameters:
        df (pd.DataFrame): viewing data
    
    Returns:
        str: chosen analysis option
        str: chosen profile(s) to analyze
        str: chosen types of content to analyze
        str: chosen title(s) to analyze
    """

    options = {"Viewing Frequency", "Viewing Activity Timeline", "Viewing Heat Map", "Start Times",
               "Most Watched Days", "Most Watched Months", "Duration",
               "Total Time Watched", "Most Watched Movies", "Most Watched Shows",
               "Most Watched Episodes", "Device Types", "Countries"}

    chosen_type = ""
    if len(set(df["Name"].values)) > 1:
        options.remove("Most Watched Episodes")
        if len(set(df["Type"].values)) == 1:
            if "Movie" in set(df["Type"].values):
                options.remove("Most Watched Shows")
                chosen_type = "Movie"
            elif "TV Show" in set(df["Type"].values):
                options.remove("Most Watched Movies")
                chosen_type = "TV Show"
        else:
            chosen_type = "All Types"
    else:
        options.remove("Most Watched Shows")
        options.remove("Most Watched Movies")
        chosen_type = [t for t in set(df["Type"].values)][0]

    print("\nOptions for Data Analysis:")
    for option in sorted(options):
        print(f"  {option}")

    chosen_option = ""
    while chosen_option not in options:
        chosen_option = input("Which option would you like to choose? ")

    if len(set(df["Profile Name"].values)) == 1:
        chosen_profile = list(set(df["Profile Name"].values))[0]
    else:
        chosen_profile = "All Profiles"

    if len(set(df["Name"].values)) == 1:
        chosen_title = list(set(df["Name"].values))[0]
    else:
        chosen_title = "All Titles"

    return chosen_option, chosen_profile, chosen_type, chosen_title


def conduct_analysis(df: pd.DataFrame, analysis: str, profile: str, content_type: str, title: str):
    """
    Conducts analysis instructed by user.

    Parameters:
        df (pd.DataFrame): viewing data
        analysis (str): chosen analysis option
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    if analysis == "Countries":
        countries_analysis(df, profile, content_type, title)
    elif analysis == "Device Types":
        devices_analysis(df, profile, content_type, title)
    elif analysis == "Viewing Frequency":
        viewing_frequency_analysis(df, profile, content_type, title)
    elif analysis == "Viewing Activity Timeline":
        viewing_activity_analysis(df, profile, content_type, title)
    elif analysis == "Viewing Heat Map":
        viewing_heat_map(df, profile, content_type, title)
    elif analysis == "Most Watched Movies":
        most_watched_movies_analysis(df, profile)
    elif analysis == "Most Watched Shows":
        most_watched_shows_analysis(df, profile)
    elif analysis == "Most Watched Days":
        most_watched_days_analysis(df, profile, content_type, title)
    elif analysis == "Most Watched Episodes":
        most_watched_episodes_analysis(df, profile, title)
    elif analysis == "Duration":
        duration_analysis(df, profile, content_type, title)


def countries_analysis(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on countries watched from.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    if profile == "All Profiles":
        profiles = [n for n in {name for name in df["Profile Name"]}]
        countries = [c for c in {country for country in df["Country"]}]
        country_values = []
        plt.figure(figsize=(6, 8))
        for country in countries:
            values = []
            for profile in profiles:
                temp_countries = df[df["Country"] == country]
                temp_data = temp_countries[temp_countries["Profile Name"] == profile]
                try:
                    values.append(temp_data["Country"].value_counts().values[0])
                except IndexError:
                    values.append(0)
            country_values.append(values)
        for i in range(len(country_values)):
            if i == 0:
                plt.bar(profiles, country_values[i], label=countries[i])
            else:
                plt.bar(profiles, country_values[i], bottom=country_values[i - 1], label=countries[i])
        plt.xlabel("Profiles", fontsize=12, labelpad=1)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        if content_type == "All Types":
            plt.title("Where All Profiles Watched Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Where All Profiles Watched Movies", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Where All Profiles Watched TV Shows", fontsize=14)
        else:
            plt.title("Where All Profiles Watched '" + title + "'", fontsize=14)
        plt.legend()
        plt.show()
    else:
        countries = df["Country"].value_counts()
        amount = len(countries)
        x = np.arange(amount)
        colors = plt.get_cmap("viridis")
        plt.figure(figsize=(6, 8))
        bars = plt.bar(countries.index, countries.values, color=colors(x / amount))
        plt.xlabel("Countries", fontsize=12, labelpad=1)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        plt.bar_label(bars, label_type="edge")
        if content_type == "All Types":
            plt.title("Where " + profile + " Watched Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Where " + profile + " Watched Movies", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Where " + profile + " Watched TV Shows", fontsize=14)
        else:
            plt.title("Where " + profile + " Watched '" + title + "'", fontsize=14)
        plt.show()


def devices_analysis(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on devices watched from.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    if profile == "All Profiles":
        profiles = [n for n in {name for name in df["Profile Name"]}]
        devices = [d for d in {device for device in df["Device Type"]}]
        device_values = []
        plt.figure(figsize=(6, 8))
        for device in devices:
            values = []
            for profile in profiles:
                temp_devices = df[df["Device Type"] == device]
                temp_data = temp_devices[temp_devices["Profile Name"] == profile]
                try:
                    values.append(temp_data["Device Type"].value_counts().values[0])
                except IndexError:
                    values.append(0)
            device_values.append(values)
        for i in range(len(device_values)):
            if i == 0:
                plt.bar(profiles, device_values[i], label=devices[i])
            else:
                plt.bar(profiles, device_values[i], bottom=device_values[i - 1], label=devices[i])
        plt.xlabel("Profiles", fontsize=12, labelpad=1)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        if content_type == "All Types":
            plt.title("Devices All Profiles Used to Watch Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Devices All Profiles Used to Watch Movies", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Devices All Profiles Used to Watch TV Shows", fontsize=14)
        else:
            plt.title("Devices All Profiles Used to Watch '" + title + "'", fontsize=14)
        plt.legend()
        plt.show()
    else:
        devices = df["Device Type"].value_counts()
        amount = len(devices)
        x = np.arange(amount)
        colors = plt.get_cmap("viridis")
        plt.figure(figsize=(14, 6))
        bars = plt.barh(devices.index, devices.values, color=colors(x / amount))
        plt.xlabel("Frequency", fontsize=12)
        plt.ylabel("Devices", fontsize=12, labelpad=1)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.bar_label(bars, label_type="edge")
        if content_type == "All Types":
            plt.title("Devices " + profile + " Used to Watch Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Devices " + profile + " Used to Watch Movies", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Devices " + profile + " Used to Watch TV Shows", fontsize=14)
        else:
            plt.title("Devices " + profile + " Used to Watch '" + title + "'", fontsize=14)
        plt.gca().invert_yaxis()
        plt.show()


def viewing_frequency_analysis(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on viewing frequency.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    profile_count = df["Profile Name"].value_counts()
    amount = len(profile_count)
    x = np.arange(amount)
    colors = plt.get_cmap("viridis")
    plt.figure(figsize=(8, 6))
    bars = plt.bar(profile_count.index, profile_count.values, color=colors(x / amount))
    plt.xlabel("Profile Names", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        if content_type == "All Types":
            plt.title("Netflix Viewing Frequency of All Profiles", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Netflix Movie Viewing Frequency of All Profiles", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Netflix TV Show Viewing Frequency of All Profiles", fontsize=14)
        else:
            plt.title("Netflix Viewing Frequency of All Profiles for '" + title + "'", fontsize=14)
    else:
        if content_type == "All Types":
            plt.title("Netflix Viewing Frequency of " + profile, fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Netflix Movie Viewing Frequency of " + profile, fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Netflix TV Show Viewing Frequency of " + profile, fontsize=14)
        else:
            plt.title("Netflix Viewing Frequency of " + profile + " for '" + title + "'", fontsize=14)
    plt.show()


def viewing_activity_analysis(df :pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on viewing activity rate.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    by_date = pd.Series(df["Date"]).value_counts().sort_index()
    by_date.index = pd.DatetimeIndex(by_date.index)
    date_count = by_date.rename_axis("Date").reset_index(name="Count")
    idx = pd.date_range(min(by_date.index), max(by_date.index))
    date_count = by_date.reindex(idx, fill_value=0)
    amount = len(date_count)
    x = np.arange(amount)
    colors = plt.get_cmap("viridis")
    plt.figure(figsize=(8, 6))
    bars = plt.bar(date_count.index, date_count.values, color=colors(x / amount))
    plt.xlabel("Date", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        if content_type == "All Types":
            plt.title("Netflix Viewing Activity Timeline of All Profiles", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Netflix Movie Viewing Activity Timeline of All Profiles", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Netflix TV Show Viewing Activity Timeline of All Profiles", fontsize=14)
        else:
            plt.title("Netflix Viewing Activity Timeline of All Profiles for '" + title + "'", fontsize=14)
    else:
        if content_type == "All Types":
            plt.title("Netflix Viewing Activity Timeline of " + profile, fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Netflix Movie Viewing Activity Timeline of " + profile, fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Netflix TV Show Viewing Activity Timeline of " + profile, fontsize=14)
        else:
            plt.title("Netflix Viewing Activity Timeline of " + profile + " for '" + title + "'", fontsize=14)
    plt.show()


def viewing_heat_map(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on viewing activity and frequency.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    by_hour = df["Start Time"].value_counts().sort_index(ascending=True)
    by_hour.index = pd.to_datetime(by_hour.index)
    hour_count = by_hour.rename_axis("Date Hour").reset_index(name="Count")
    idx = pd.date_range(min(by_hour.index), max(by_hour.index), freq="1H")
    hour_count = by_hour.reindex(idx, fill_value=0)
    df_count = hour_count.rename_axis("Datetime").reset_index(name="Frequency")
    df_count["Date"] = df_count["Datetime"].dt.date
    df_count["Hour"] = df_count["Datetime"].dt.hour
    df_count["Day"] = df_count["Datetime"].dt.weekday
    df_count["Month"] = df_count["Datetime"].dt.month
    df_count["Year"] = df_count["Datetime"].dt.year
    df_count = df_count.drop(["Datetime"], axis=1)
    df_heatmap = df_count[["Day", "Hour", "Frequency"]].groupby(["Day", "Hour"]).sum()
    matrix = df_heatmap.unstack().fillna(0)
    hours_list = list(range(0,24))
    days_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    sns.set_context("talk")
    fig, ax = plt.subplots(figsize=(12,5))
    ax = sns.heatmap(matrix, linewidths=0.5, ax=ax, yticklabels=days_list, xticklabels=hours_list, cmap="viridis")
    if profile == "All Profiles":
        if content_type == "All Types":
            ax.axes.set_title("Heatmap of Netflix Viewing Activity of All Profiles", fontsize=20, y=1.02)
        elif content_type == "Movie" and title == "All Titles":
            ax.axes.set_title("Heatmap of Netflix Movie Viewing Activity of All Profiles", fontsize=20, y=1.02)
        elif content_type == "TV Show" and title == "All Titles":
            ax.axes.set_title("Heatmap of Netflix TV Show Viewing Activity of All Profiles", fontsize=20, y=1.02)
        else:
            ax.axes.set_title("Heatmap of Netflix Viewing Activity of All Profiles for '" + title + "'", fontsize=20,
                              y=1.02)
    else:
        if content_type == "All Types":
            ax.axes.set_title("Heatmap of Netflix Viewing Activity of " + profile, fontsize=20, y=1.02)
        elif content_type == "Movie" and title == "All Titles":
            ax.axes.set_title("Heatmap of Netflix Movie Viewing Activity of " + profile, fontsize=20, y=1.02)
        elif content_type == "TV Show" and title == "All Titles":
            ax.axes.set_title("Heatmap of Netflix TV Show Viewing Activity of " + profile, fontsize=20, y=1.02)
        else:
            ax.axes.set_title("Heatmap of Netflix Viewing Activity of " + profile + " for '" + title + "'",
                              fontsize=20, y=1.02)
    ax.set(xlabel="Hour of Day", ylabel="Day of Week")
    plt.show()


def most_watched_movies_analysis(df: pd.DataFrame, profile: str):
    """
    Conducts analysis based on most watched movies.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
    """

    df = df[df["Type"] == "Movie"]
    top_movies = df["Name"].value_counts().nlargest(10)
    amount = len(top_movies)
    x = np.arange(amount)
    colors = plt.get_cmap("viridis")
    plt.figure(figsize=(8, 8))
    bars = plt.bar(top_movies.index, top_movies.values, color=colors(x / amount))
    plt.xlabel("Movies", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        plt.title("Most Watched Movies by All Profiles", fontsize=14)
    else:
        plt.title("Most Watched Movies by " + profile, fontsize=14)
    plt.show()


def most_watched_shows_analysis(df: pd.DataFrame, profile: str):
    """
    Conducts analysis based on most watched shows.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
    """

    df = df[df["Type"] == "TV Show"]
    top_shows = df["Name"].value_counts().nlargest(10)
    amount = len(top_shows)
    x = np.arange(amount)
    colors = plt.get_cmap("viridis")
    plt.figure(figsize=(8, 8))
    bars = plt.bar(top_shows.index, top_shows.values, color=colors(x / amount))
    plt.xlabel("Shows", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        plt.title("Most Watched TV Shows by All Profiles", fontsize=14)
    else:
        plt.title("Most Watched TV Shows by " + profile, fontsize=14)
    plt.show()


def most_watched_episodes_analysis(df: pd.DataFrame, profile: str, title: str):
    """
    Conducts analysis based on most watched episodes of a specific show.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        title (str): chosen title(s) to analyze
    """

    top_episodes = df["Episode"].value_counts().nlargest(10)
    amount = len(top_episodes)
    x = np.arange(amount)
    colors = plt.get_cmap("viridis")
    plt.figure(figsize=(8, 8))
    bars = plt.bar(top_episodes.index, top_episodes.values, color=colors(x / amount))
    plt.xlabel("Episodes", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=25, ha="right", fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        plt.title("Most Watched Episodes of '" + title + "' by All Profiles", fontsize=14)
    else:
        plt.title("Most Watched Episodes of '" + title + "' by " + profile, fontsize=14)
    plt.show()


def most_watched_days_analysis(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on most watched days of the week.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["Day"] = pd.Categorical(df["Day"], categories=days, ordered=True)
    frequency_per_day = df.sort_values("Day")["Day"].value_counts().sort_index()
    amount = len(frequency_per_day)
    x = np.arange(amount)
    colors = plt.get_cmap("winter").reversed()
    plt.figure(figsize=(8, 8))
    bars = plt.bar(frequency_per_day.index, frequency_per_day.values, color=colors(x / amount))
    plt.xlabel("Day of Week", fontsize=12, labelpad=1)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.bar_label(bars, label_type="edge")
    if profile == "All Profiles":
        if content_type == "All Types":
            plt.title("Most Watched Days by All Profiles", fontsize=14)
        elif content_type == "Movie":
            plt.title("Most Watched Days for Movies by All Profiles", fontsize=14)
        elif content_type == "TV Show":
            plt.title("Most Watched Days for TV Shows by All Profiles", fontsize=14)
        else:
            plt.title("Most Watched Days for '" + title + "' by All Profiles", fontsize=14)
    else:
        if content_type == "All Types":
            plt.title("Most Watched Days by " + profile, fontsize=14)
        elif content_type == "Movie":
            plt.title("Most Watched Days for Movies by " + profile, fontsize=14)
        elif content_type == "TV Show":
            plt.title("Most Watched Days for TV Shows by " + profile, fontsize=14)
        else:
            plt.title("Most Watched Days for '" + title + "' by " + profile, fontsize=14)
    plt.show()


def duration_analysis(df: pd.DataFrame, profile: str, content_type: str, title: str):
    """
    Conducts analysis based on duration of viewing.

    Parameters:
        df (pd.DataFrame): viewing data
        profile (str): chosen profile(s) to analyze
        content_type (str): chosen types of content to analyze
        title (str): chosen title(s) to analyze
    """

    thirty_minutes = pd.to_timedelta("0:30:00")
    one_hour = pd.to_timedelta("1:00:00")
    hour_and_a_half = pd.to_timedelta("1:30:00")
    two_hours = pd.to_timedelta("2:00:00")
    two_and_a_half_hours = pd.to_timedelta("2:30:00")
    three_hours = pd.to_timedelta("3:00:00")

    def categorize_duration(d):
        category = ""
        if content_type == "All Types":
            if d < thirty_minutes:
                category = "< 0.5 hrs."
            elif d < one_hour:
                category = "0.5-1 hrs."
            elif d < hour_and_a_half:
                category = "1-1.5 hrs."
            elif d < two_hours:
                category = "1.5-2 hrs."
            elif d < two_and_a_half_hours:
                category = "2-2.5 hrs."
            elif d < three_hours:
                category = "2.5-3 hrs."
            else:
                category = "> 3 hrs."
        elif content_type == "Movie":
            if d < hour_and_a_half:
                category = "< 1.5 hrs."
            elif d < two_hours:
                category = "1.5-2 hrs."
            elif d < two_and_a_half_hours:
                category = "2-2.5 hrs."
            elif d < three_hours:
                category = "2.5-3 hrs."
            else:
                category = "3 hrs."
        elif content_type == "TV":
            if d < thirty_minutes:
                category = "< 0.5 hrs."
            elif d < one_hour:
                category = "0.5-1 hrs."
            else:
                category = "> 1 hr."

        return category

    if profile == "All Profiles":
        df_duration = df[["Profile Name", "Duration"]]
        df_duration["Duration Category"] = df_duration["Duration"].apply(categorize_duration)
        profiles = [n for n in {name for name in df_duration["Profile Name"]}]
        durations = [d for d in {duration for duration in df_duration["Duration Category"]}]
        duration_values = []
        plt.figure(figsize=(6, 8))
        for duration in durations:
            values = []
            for profile in profiles:
                temp_durations = df_duration[df_duration["Duration Category"] == duration]
                temp_data = temp_durations[temp_durations["Profile Name"] == profile]
                try:
                    values.append(temp_data["Duration Category"].value_counts().values[0])
                except IndexError:
                    values.append(0)
            duration_values.append(values)
        for i in range(len(duration_values)):
            if i == 0:
                plt.bar(profiles, duration_values[i], label=durations[i])
            else:
                plt.bar(profiles, duration_values[i], bottom=duration_values[i - 1], label=durations[i])
        plt.xlabel("Profiles", fontsize=12, labelpad=1)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        if content_type == "All Types":
            plt.title("Duration of Content All Profiles Watched on Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Duration of Movies All Profiles Watched on Netflix", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Duration of TV Shows All Profiles Watched on Netflix", fontsize=14)
        else:
            plt.title("Duration of '" + title + "' All Profiles Watched on Netflix", fontsize=14)
        plt.legend()
        plt.show()
    else:
        df_duration = df[["Duration"]]
        df_duration["Duration Category"] = df_duration["Duration"].apply(categorize_duration)
        durations_count = df_duration["Duration Category"].value_counts()
        amount = len(durations_count)
        x = np.arange(amount)
        colors = plt.get_cmap("viridis")
        plt.figure(figsize=(6, 8))
        bars = plt.bar(durations_count.index, durations_count.values, color=colors(x / amount))
        plt.xlabel("Duration", fontsize=12, labelpad=1)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        plt.bar_label(bars, label_type="edge")
        if content_type == "All Types":
            plt.title("Duration of Content " + profile + " Watched on Netflix", fontsize=14)
        elif content_type == "Movie" and title == "All Titles":
            plt.title("Duration of Movies " + profile + " Watched on Netflix", fontsize=14)
        elif content_type == "TV Show" and title == "All Titles":
            plt.title("Duration of TV Shows " + profile + " Watched on Netflix", fontsize=14)
        else:
            plt.title("Duration of '" + title + "' Watched By " + profile, fontsize=14)
        plt.show()


def _drop_unnecessary_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops unnecessary columns within the dataframe.

    Parameters:
        df (pd.DataFrame): viewing data

    Returns:
        pd.DataFrame: updated viewing data with unnecessary columns dropped
    """

    df = df[df["Supplemental Video Type"].isna()]
    df["duration_minutes"] = df["Duration"].str.split(":").apply(lambda x: int(x[0]) * 60 + int(x[1]))
    df = df[df["duration_minutes"] >= 5]
    df = df.drop(
        ["Attributes", "Supplemental Video Type", "Bookmark", "Latest Bookmark", "duration_minutes"], axis=1)

    return df


if __name__ == "__main__":
    """
    Code that executes only when this module is run.
    """

    initial_dataframe = ask_for_data()
    initial_dataframe = convert_times(initial_dataframe)

    first_run = True
    while True:
        if first_run:
            first_run = False
        else:
            terminate = ""
            while terminate != "Y" and terminate != "N":
                terminate = input("\nWould you like to continue (Y or N)? ")
            if terminate == "N":
                break

        current_dataframe = ask_for_profile(initial_dataframe)
        current_dataframe = separate_types_of_content(current_dataframe)
        current_dataframe = ask_for_content_type(current_dataframe)

        analysis, profile, content_type, title = choose_analysis(current_dataframe)
        conduct_analysis(current_dataframe, analysis, profile, content_type, title)
