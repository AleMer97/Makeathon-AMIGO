from FeatureCloud.app.engine.app import AppState, app_state, Role
import time
import os
import logging
from data_fetcher import DataFetcher

from neo4j import GraphDatabase, Query, Record
from neo4j.exceptions import ServiceUnavailable
from pandas import DataFrame

from utils import read_config,write_output,ResultRow,CSVResultsBuilder

from FeatureCloud.app.engine.app import AppState, app_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = read_config()

@app_state('initial')
class ExecuteState(AppState):

    def register(self):
        self.register_transition('terminal', Role.BOTH)

    def run(self):
        # Get Neo4j credentials from config
        neo4j_credentials = config.get("neo4j_credentials", {})
        NEO4J_URI = neo4j_credentials.get("NEO4J_URI", "")
        NEO4J_USERNAME = neo4j_credentials.get("NEO4J_USERNAME", "")
        NEO4J_PASSWORD = neo4j_credentials.get("NEO4J_PASSWORD", "")
        NEO4J_DB = neo4j_credentials.get("NEO4J_DB", "")
        logger.info(f"Neo4j Connect to {NEO4J_URI} using {NEO4J_USERNAME}")
        
        # Driver instantiation
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

        # Result
        result = CSVResultsBuilder()

        # Create a driver session with defined DB
        with driver.session(database=NEO4J_DB) as session:
            # Result Builder
            logger.info("Fetching data from Neo4j: ...")
            fetcher = DataFetcher(session)
            logger.info("Fetching data from Neo4j: Done")
                
            
        
        print("test:" + result.csv())
        write_output(f"{result.csv()}")

        # Close the driver connection
        driver.close()

        return 'terminal'



