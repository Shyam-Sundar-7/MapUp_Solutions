import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    index = df['id_start'].unique().tolist()
    columns=df['id_end'].unique().tolist()
    union = sorted(list(set(index) | set(columns)))
    distance_matrix = pd.DataFrame(0.0,columns=union, index=union)
    for index, row in df.iterrows():
        start_id, end_id, distance = row['id_start'],row['id_end'], row['distance']
        distance_matrix.loc[start_id, end_id]= distance
        distance_matrix.loc[end_id, start_id]=distance

    for i in range(2,len(distance_matrix.columns)):
        for j in range(i-2,-1,-1):
            distance_matrix.iloc[i,j]=round(distance_matrix.iloc[i-1,j]+distance_matrix.iloc[i,i-1],1)
            distance_matrix.iloc[j,i]=distance_matrix.iloc[i,j]

    return distance_matrix


def unroll_distance_matrix(d)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    id_start=list()
    id_end=list()
    distance=list()
    for i in d.index:
        for j in d.index:
            if (i!=j):
                id_start.append(i)
                id_end.append(j)
                distance.append(d.loc[i,j])
    df=pd.DataFrame()
    df['id_start']=id_start
    df['id_end']=id_end
    df['distance']=distance
    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    mean_value=df[df['id_start'] == reference_id]['distance'].mean()
    id_start_list=sorted(list(df[(df['distance']>=mean_value*.9) & (df['distance']<=mean_value*1.1)]['id_start'].unique()))
    df=pd.DataFrame(id_start_list)

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    df['moto']=0.8*df['distance']
    df['car']=1.2*df['distance']
    df['rv']=1.5*df['distance']
    df['bus']=2.2*df['distance']
    df['truck']=3.6*df['distance']
    df.drop(['distance'],axis=1,inplace=True)

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    discount_factors = {
        'weekday': [(pd.to_datetime('00:00:00').time(), pd.to_datetime('10:00:00').time(), 0.8),
                    (pd.to_datetime('10:00:00').time(), pd.to_datetime('18:00:00').time(), 1.2),
                    (pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time(), 0.8)],
        'weekend': [(pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time(), 0.7)]
    }
    
    # Function to apply discount factor based on time and day
    def apply_discount(row):
        start_time = pd.to_datetime(row['start_time']).time()
        end_time = pd.to_datetime(row['end_time']).time()
        day_type = 'weekend' if row['start_day'] in ['Saturday', 'Sunday'] else 'weekday'
        
        for start, end, discount in discount_factors[day_type]:
            if start <= start_time < end:
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    row[vehicle] *= discount
                break
        return row
    
    # Apply the discount factor to each row
    df = df.apply(apply_discount, axis=1)
    
    return df