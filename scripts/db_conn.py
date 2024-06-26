import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Function to read CSV file and convert to DataFrame
def read_csv_to_df(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adjclose',
        'Volume': 'volume'
    })
    return df

# Read CSV files
df_bnb = read_csv_to_df('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/BNB-USD.csv')
df_eth = read_csv_to_df('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/ETH-USD.csv')
df_sol = read_csv_to_df('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/SOL-USD.csv')
df_xrp = read_csv_to_df('/home/jabez_kassa/week_9/Crypto-Trading-Engineering/data/XRP-USD.csv')

# Function to insert DataFrame into database
def insert_df_to_db(df, table_name):
    # Create the SQLAlchemy engine
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/historical_data')
    # Use the to_sql method to insert the DataFrame into the database
    df.to_sql(table_name, engine, if_exists='append', index=False)

# Insert DataFrames into database
insert_df_to_db(df_bnb, 'bnb_data')
insert_df_to_db(df_eth, 'eth_data')
insert_df_to_db(df_sol, 'sol_data')
insert_df_to_db(df_xrp, 'xrp_data')

# Function to get DataFrame from database
def get_df_from_db(conn, table_name):
    cur = conn.cursor()
    try:
        # Execute a query
        cur.execute(f"SELECT * FROM {table_name};")

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Get column names from the cursor
        colnames = [desc[0] for desc in cur.description]

        # Convert the result set to a DataFrame
        df = pd.DataFrame(rows, columns=colnames)
    finally:
        # Close the cursor
        cur.close()

    return df

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="historical_data",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)



# Close the connection
conn.close()


