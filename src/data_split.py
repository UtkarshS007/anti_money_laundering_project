import logging
from sklearn.model_selection import train_test_split    
import datatable as dt
import pandas as pd

# Configure logging
logging.basicConfig(filename='data_split.log', level=logging.INFO)
# Define a stream handler to write log messages to the terminal
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Create a formatter and set it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console)

def data_split(raw_data):
    logging.info("Starting data splitting")

    try:
        train_df, test_df = train_test_split(raw_data.to_pandas(), test_size=0.2, random_state=42, stratify=raw_data['Is Laundering'])
        train_dt = dt.Frame(train_df)
        test_dt = dt.Frame(test_df)
        
        logging.info("Data splitting finished")
        return train_dt, test_dt

    except Exception as e:
        logging.error(f"An error occurred during data splitting: {e}")
        return None, None