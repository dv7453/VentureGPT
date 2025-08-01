# agents/generalized_agent.py

import yaml
import logging
from .generalised_agent_helper import GeneralizedAgentHelper


class GeneralizedAgent:
    def __init__(self, config_path='config/config.yaml'):
        # Load configuration
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Extract API key for Groq (assuming it's stored here)
        llama_api_key = config['agents']['generalized_agent']['llama_api_key']

        # Initialize helper functions
        self.helper = GeneralizedAgentHelper(llama_api_key_env_var='GENERALIZED_AGENT_API_KEY')

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def process(self, storage, idea_id):
        """
        Processes the aggregated data to generate a comprehensive report.
        """
        try:
            self.logger.info("Starting report generation.")

            # Aggregate data from storage
            aggregated_data = self.helper.aggregate_data(storage, idea_id)

            # Summarize the data using Llama
            summary = self.helper.summarize_data_with_llama(aggregated_data)

            # Optionally, format the report using Llama
            final_report = self.helper.format_report_with_llama(summary)

            self.logger.info("Report generation completed successfully.")
            return final_report
        except Exception as e:
            self.logger.error(f"Error during report generation: {e}")
            return "An error occurred during report generation."
