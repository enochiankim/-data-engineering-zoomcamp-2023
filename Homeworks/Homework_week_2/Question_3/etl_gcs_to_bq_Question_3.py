from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    #print(f"printed passenger count: {df['passenger_count']}")
    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="******",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

@flow()
def etl_main_flow(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)
    print(f"printed passenger count: {df['passenger_count']}")


@flow()
def etl_gcs_to_bq(months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"):
    for month in months:
        etl_main_flow(year, month, color)
    
if __name__ == "__main__":
    etl_gcs_to_bq()
