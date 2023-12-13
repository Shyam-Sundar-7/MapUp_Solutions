import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix=df.pivot(index='id_1',columns='id_2',values='car')

    for i in range(len(car_matrix.index)):
        car_matrix.iloc[i,i]=0
    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    def category(x):
        if(x<=15):
            return "low"
        elif (x>15 and x<=25):
            return "medium"
        else:
            return "high"

    df['car_type']=df['car'].apply(lambda x : category(x)) 
    type_count=df['car_type'].value_counts().to_dict()
    sorted_dict = dict(sorted(type_count.items()))

    return sorted_dict


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus_value = df['bus'].mean()
    indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()
    return indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    filtered_routes = df.groupby('route')['truck'].mean()
    filtered_routes = filtered_routes[filtered_routes > 7].index.tolist()
    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    for i in range(len(matrix.index)):
        for j in range(len(matrix.columns)):
            if(matrix.iloc[i,j]>20):
                matrix.iloc[i,j]=round(matrix.iloc[i,j]*0.75,1)
            else:
                matrix.iloc[i,j]=round(matrix.iloc[i,j]*1.25,1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    def is_full_day_coverage(group):
        return set(group['start'].dt.hour) == set(range(24)) and set(group['end'].dt.hour) == set(range(24))
    
    def is_full_week_coverage(group):
        return set(group['start'].dt.day_name()) == {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    
    grouped = df.groupby(['id', 'id_2'])
    result = grouped.apply(lambda g: not (is_full_day_coverage(g) and is_full_week_coverage(g)))

    return result

