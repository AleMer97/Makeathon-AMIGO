from FeatureCloud.app.engine.app import AppState, app_state, Role
import time
import os
import logging

from neo4j import GraphDatabase, Query, Record
from neo4j.exceptions import ServiceUnavailable
from pandas import DataFrame

from utils import read_config,write_output

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
        
        # Create a driver session with defined DB
        with driver.session(database=NEO4J_DB) as session:
                
            # Example Query to Count Nodes 
            node_count_query = """MATCH (b:Biological_sample)-->(d:Disease)
WITH b,d,any(s in d.synonyms WHERE s STARTS WITH "ICD10CM") as icd10
RETURN b, d.name, icd10, d.name = "control" as control LIMIT 1000
"""
        
            # Use .data() to access the results array        
            results = session.run(node_count_query).data()
            logger.info(results)
            
        write_output(f"{results}")

        # Close the driver connection
        driver.close()

        return 'terminal'



