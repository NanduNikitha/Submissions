import pandas as pd
def generate_car_matrix(df) -> pd.DataFrame:
    matrix_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    matrix_df.values[[range(len(matrix_df.index))]*2] = 0
    return matrix_df

df = pd.read_csv("dataset-1.csv")
result_matrix = generate_car_matrix(df)
stored_result_df = pd.DataFrame(result_matrix.values, index=result_matrix.index, columns=result_matrix.columns)
print(stored_result_df)


def get_type_count(df) -> dict:
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().sort_index().to_dict()

    return type_counts  
df = pd.read_csv("dataset-1.csv")
get_type_count(df)

def get_bus_indexes(df) -> list:

    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    bus_indexes.sort()

    return bus_indexes  
df = pd.read_csv("dataset-1.csv") 
get_bus_indexes(df)


def filter_routes(df) -> list:
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes
df = pd.read_csv("dataset-1.csv") 
filter_routes(df)

def multiply_matrix(matrix) -> pd.DataFrame:
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix
matrix = stored_result_df
multiply_matrix(matrix)

def time_check(df) -> pd.Series:
  
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df.dropna(subset=['start_timestamp', 'end_timestamp'], inplace=True)
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    time_check_result = df.groupby(['id', 'id_2']).apply(
        lambda x: (x['duration'].sum() >= pd.Timedelta(days=7)) and 
                  ((x['start_timestamp'].min().time() == pd.Timestamp.min.time()) and 
                  (x['end_timestamp'].max().time() == pd.Timestamp.max.time()))
    )

    return time_check_result
df = pd.read_csv("dataset-2.csv") 
time_check(df)
