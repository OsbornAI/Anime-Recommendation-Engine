from collections import Counter
import numpy as np
import pandas as pd

# This will also check to see the amount of good values available left and if it is too low then it will clear the blacklist from the shows it hasnt watched yet
# Maybe I should block the ability to add too many shows aka limit it to be 500 shows
def recommendContent(anime_df, username, anime_list, blacklist):
    # This will create the common vector of our watched anime
    list_df = anime_df[anime_df['anime_id'].str.contains("|".join(anime_list[1:]))] # We use 1: here to not include the first item in the list which will be an empty character
    if len(anime_list[1:]) == 0:
        list_df = list_df.sort_values(by='weighted_score', ascending=False).iloc[:20, :].sample(n=10)

    ep_len_bins = []
    ep_count_bins = []
    rating_bins = []
    source_bins = []
    show_type_bins = []
    weighted_scores = []
    genre_bins = []
    licensor_bins = []
    producer_bins = []
    studio_bins = []
    for _, row in list_df.iterrows():
        ep_len = row[14]
        if pd.notna(ep_len):
            ep_len_bins.append(ep_len)

        ep_count = row[12]
        if pd.notna(ep_count):
            ep_count_bins.append(ep_count)

        rating = row[6]
        if pd.notna(rating):
            rating_bins.append(rating)

        source = row[5] # Also have to check to make sure the value is not 'add some'
        if pd.notna(source):
            source_bins.append(source)

        show_type = row[4]
        if pd.notna(show_type):
            show_type_bins.append(show_type)

        weighted_score = row[17]
        if pd.notna(weighted_score):
            weighted_scores.append(weighted_score)

        genres = row[10]
        if pd.notna(genres):
            for genre in genres.split(', '):
                if genre != 'add some':
                    genre_bins.append(genre)

        licensors = row[7] 
        if pd.notna(genres):
            for licensor in licensors.split(', '):
                if licensor != 'add some':
                    licensor_bins.append(licensor)
                    
        producers = row[8]
        if pd.notna(producers):
            for producer in producers.split(', '):
                if producer != 'add some':
                    producer_bins.append(producer)

        studios = row[9]
        if pd.notna(studios):
            for studio in studios.split(', '):
                if studio != 'add some':
                    studio_bins.append(studio)

    ep_len_common = [item[0] for item in Counter(ep_len_bins).most_common()][:3] # Will take the 3 most common
    ep_count_common = [item[0] for item in Counter(ep_count_bins).most_common()][:3]
    rating_common = [item[0] for item in Counter(rating_bins).most_common()][:3]
    source_common = [item[0] for item in Counter(source_bins).most_common()][:3]
    show_type_common = [item[0] for item in Counter(show_type_bins).most_common()][:3]
    weighted_score_median = np.median(weighted_scores)
    genres_common = [item[0] for item in Counter(genre_bins).most_common()][:3]
    licensors_common = [item[0] for item in Counter(licensor_bins).most_common()][:3]
    producers_common = [item[0] for item in Counter(producer_bins).most_common()][:3]
    studios_common = [item[0] for item in Counter(studio_bins).most_common()][:3]

    common = {'ep_len': ep_len_common, 'ep_count': ep_count_common, 'rating': rating_common, 'source': source_common, 
              'show_type': show_type_common, 'weighted_score': weighted_score_median, 'genres': genres_common, 'licensors': licensors_common,
              'producers': producers_common, 'studios': studios_common}

    return common