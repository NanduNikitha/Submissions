import pandas as pd

def calculate_distance_matrix(df) -> pd.DataFrame:
    pivot_table = df.pivot_table(values='distance', index='id_start', columns='id_end', aggfunc='sum', fill_value=0)
    distance_matrix = pivot_table + pivot_table.T
    distance_matrix.values[[range(len(distance_matrix.index))]*2] = 0
    return distance_matrix

df = pd.read_csv("dataset-3.csv") 
calculate_distance_matrix(df)

import pandas as pd
from itertools import product

def unroll_distance_matrix(df):
    unique_ids = df['id_start'].unique()
    combinations = list(product(unique_ids, repeat=2))
    combinations = [(start, end) for start, end in combinations if start != end]
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for start, end in combinations:
        distance = df[(df['id_start'] == start) & (df['id_end'] == end)]['distance'].values
        if len(distance) > 0:
            unrolled_df = unrolled_df.append({
                'id_start': start,
                'id_end': end,
                'distance': distance[0]
            }, ignore_index=True)

    return unrolled_df
df = pd.read_csv("dataset-3.csv") 
unroll_distance_matrix(df)

def find_ids_within_ten_percentage_threshold(df, reference_id):
   
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = reference_avg_distance * 0.10
    within_threshold_ids = df.groupby('id_start')['distance'].mean()
    within_threshold_ids = within_threshold_ids[
        (within_threshold_ids >= (reference_avg_distance - threshold)) &
        (within_threshold_ids <= (reference_avg_distance + threshold))
    ].reset_index()

    sorted_ids_within_threshold = within_threshold_ids.sort_values('id_start')[['id_start', 'distance']]

    return sorted_ids_within_threshold


df = pd.read_csv("dataset-3.csv") 
find_ids_within_ten_percentage_threshold(df, reference_id)

def calculate_toll_rate(df):
   
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle, rate in rate_coefficients.items():
        df[vehicle] = df['distance'] * rate
    return df
df = pd.read_csv("dataset-3.csv")
calculate_toll_rate(df)
