import logging
import datatable as dt
import dask.dataframe as dd
import pandas as pd
import ast
import dask
from dask.distributed import Client
import pickle

# Configure logging
logging.basicConfig(filename='dask_dataframe_creation.log', level=logging.INFO)
# Define a stream handler to write log messages to the terminal
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Create a formatter and set it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console)

def create_dask_dataframe(**kwargs):
    logging.info("Starting Dask DataFrame creation")

    try:
        graph_features = kwargs['task_instance'].xcom_pull(task_ids='process_graph_data', key='graph_features_bytes')
        graph_features = pickle.loads(graph_features)
        # graph_features = [dask.delayed(lambda x: x)(string_data) for string_data in graph_features]

        # # Compute delayed objects
        # graph_features_computed = dask.compute(*graph_features)

        # Convert each string to a dictionary
        dicts = [ast.literal_eval(string_data) for string_data in graph_features]

        # Create a list of lists containing the dictionary values for each entry
        list_of_lists = [list(data_dict.values()) for data_dict in dicts]

        # Create a DataFrame from the list of lists
        lists_df = pd.DataFrame(list_of_lists, columns=dicts[0].keys())

        # Convert specific columns to the desired data types
        convert_dtype = {'Node': 'int64', 'degree': 'int64', 'in_degree': 'int64', 'out_degree': 'int64', 'clustering_coefficient': 'float64', 'degree_centrality': 'float64'}
        graph_features_df = lists_df.astype(convert_dtype)
        graph_features_ddf = dd.from_pandas(graph_features_df, npartitions=2)
        
        logging.info("Dask DataFrame creation finished")
        kwargs['task_instance'].xcom_push(key='graph_features_ddf', value=graph_features_ddf)
        return graph_features_ddf

    except Exception as e:
        logging.error(f"An error occurred during Dask DataFrame creation: {e}")
        return None
