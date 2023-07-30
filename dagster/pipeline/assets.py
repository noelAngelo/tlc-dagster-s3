import requests
import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup
from dagster import AssetExecutionContext, MetadataValue, asset, AssetIn, Config

# GLOBAL VARIABLES
S3_BUCKET = 'app-dev-apse2-tlc-dagster'
LIMIT = 5


class S3Config(Config):
    bucket_name: str = S3_BUCKET


@asset(group_name='TLC')
def get_trip_data_links(context: AssetExecutionContext):
    """
    fetches the content of the provided URL, parse it with BeautifulSoup, and then filter and return all the links that
    contain "parquet" in the URL.
    """
    try:
        response = requests.get('https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    trip_data = {'yellow': [], 'green': [], 'fhvhv': [], 'fhv': []}

    for link in soup.find_all('a', href=True):
        if 'parquet' in link['href'] and 'pdf' not in link['href']:
            if 'yellow' in link['href']:
                trip_data['yellow'].append(link['href'])
            elif 'green' in link['href']:
                trip_data['green'].append(link['href'])
            elif 'fhvhv' in link['href']:
                trip_data['fhvhv'].append(link['href'])
            else:
                trip_data['fhv'].append(link['href'])

    # recorded metadata can be customized
    metadata = {
        "yellow": len(trip_data['yellow']),
        'green': len(trip_data['green']),
        'fhvhv': len(trip_data['fhvhv']),
        'fhv': len(trip_data['fhv'])
        # "preview": MetadataValue.md(df[["title", "by", "url"]].to_markdown()),
    }
    context.add_output_metadata(metadata=metadata)
    return trip_data


@asset(group_name='TLC', ins={'links': AssetIn('get_trip_data_links')})
def collect_trip_data_from_links(context: AssetExecutionContext, config: S3Config, links: dict):
    """
    Reads a link containing the contents of a Parquet file, creates an array with the current timestamp, and then
    appends that array as a new column with the name "processed_timestamp" to the original PyArrow Table.

    :param config:
    :param links:
    :param context:
    :return:
    """
    processed_tables = []
    metadata = {}
    n_processed_tables = 0
    for taxi_type in links.keys():
        total_rows = 0
        context.log.info(f'Collecting data from {taxi_type} links')
        for link in links[taxi_type]:
            if LIMIT > 0 and LIMIT == n_processed_tables:
                break
            else:
                n_processed_tables += 1

            # URL pattern
            pattern = r'/([^\/]+)\.parquet$'
            match = re.search(pattern, link)
            if match:
                filename = match.group(1)
                context.log.debug(f'Reading from {link}')
                try:
                    # Extract data
                    df = pd.read_parquet(path=link)

                    # Transform data - add audit column
                    df['processed_timestamp'] = datetime.now()
                    processed_tables.append(df)
                    total_rows += len(df)
                    context.log.info(f'Found {len(df):,} rows')

                    # Load data - upload to S3
                    s3_url = f's3://{config.bucket_name}/trips/{filename}.parquet'
                    context.log.debug(f'Writing to {s3_url}')
                    df.to_parquet(s3_url)

                except Exception as e:
                    context.log.error(f"Error processing link '{link}': {e}")
                    raise Exception
        metadata[taxi_type] = total_rows
    context.add_output_metadata(metadata=metadata)
