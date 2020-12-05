import pandas as pd
import sqlite3
from collections import Counter
import numpy as np

def recommendationLevel(row, common_vector):
    recommend_level = 0

    ep_len = row[13]
    if not pd.isnull(ep_len):
        lookup = {element: (len(common_vector[0]) - i)/len(common_vector[0]) for i, element in enumerate(common_vector[0])}
        if ep_len in lookup.keys():
            recommend_level += lookup[ep_len]

    ep_count = row[11]
    if not pd.isnull(ep_count):
        lookup = {element: (len(common_vector[1]) - i)/len(common_vector[1]) for i, element in enumerate(common_vector[1])}
        if ep_count in lookup.keys():
            recommend_level += lookup[ep_count]

    rating = row[5]
    if not pd.isnull(rating):
        lookup = {element: (len(common_vector[2]) - i)/len(common_vector[2]) for i, element in enumerate(common_vector[2])}
        if rating in lookup.keys():
            recommend_level += lookup[rating]

    show_type = row[4]
    if not pd.isnull(show_type):
        lookup = {element: (len(common_vector[3]) - i)/len(common_vector[3]) for i, element in enumerate(common_vector[3])}
        if show_type in lookup.keys():
            recommend_level += lookup[show_type]

    weighted_score = row[16]
    if not pd.isnull(weighted_score):
        similarity = 1 - abs(weighted_score - common_vector[4])
        recommend_level += similarity

    genres = row[9]
    if not pd.isnull(genres):
        lookup = {element: (len(common_vector[5]) - i)/len(common_vector[5]) for i, element in enumerate(common_vector[5])}
        temp_recommend_level = 0
        for genre in genres.split(', '):
            if genre in lookup.keys():
                temp_recommend_level += lookup[genre]
        temp_recommend_level /= sum(lookup.values())
        recommend_level += temp_recommend_level
    
    return recommend_level

# This will also check to see the amount of good values available left and if it is too low then it will clear the blacklist from the shows it hasnt watched yet
# Maybe I should block the ability to add too many shows aka limit it to be 500 shows
def recommend(sql_dir, username, anime_list, blacklist):
    conn = sqlite3.connect(sql_dir)
    df = pd.read_sql_query("SELECT * FROM anime", conn)
    conn.close()

    # This section will create us our comparison vector
    list_df = df[df['anime_id'].str.contains("|".join(anime_list[1:]))] # We use 1: here to not include the first item in the list which will be an empty character
    if len(anime_list[1:]) == 0:
        list_df = list_df.iloc[:500, :]

    ep_len_bins = []
    ep_count_bins = []
    rating_bins = []
    show_type_bins = []
    weighted_scores = []
    genres_bins = []
    for _, row in list_df.iterrows():
        ep_len = row[13]
        if not pd.isnull(ep_len):
            ep_len_bins.append(ep_len)

        ep_count = row[11]
        if not pd.isnull(ep_count):
            ep_count_bins.append(ep_count)

        rating = row[5]
        if not pd.isnull(rating):
            rating_bins.append(rating)

        show_type = row[4]
        if not pd.isnull(show_type):
            show_type_bins.append(show_type)

        weighted_score = row[16]
        if not pd.isnull(weighted_score):
            weighted_scores.append(weighted_score)

        genres = row[9]
        if not pd.isnull(genres):
            for genre in genres.split(', '):
                genres_bins.append(genre)

    ep_len_common = [item[0] for item in Counter(ep_len_bins).most_common()][:3] # Will take the 3 most common
    ep_count_common = [item[0] for item in Counter(ep_count_bins).most_common()][:3]
    rating_common = [item[0] for item in Counter(rating_bins).most_common()][:3]
    show_type_common = [item[0] for item in Counter(show_type_bins).most_common()][:3]
    weighted_score_average = np.median(weighted_scores)
    genres_common = [item[0] for item in Counter(genres_bins).most_common()][:3]

    common_vector = [ep_len_common, ep_count_common, rating_common, show_type_common, weighted_score_average, genres_common]

    recommendation_levels = []
    for _, row in df.iterrows():
        recommendation_level = recommendationLevel(row, common_vector)
        recommendation_levels.append(recommendation_level)
    df['recommendation_level'] = recommendation_levels
    df = df.sort_values(by='recommendation_level')

    return df.head()