# main.py

import yaml
import logging
from agents.legal_agent.legal_agent import LegalAgent
from agents.economics_agent.economics_agent import EconomicsAgent
from agents.buisness_structure_agent.buisness_structure_agent import BusinessStructureAgent
from agents.generalised_agent.generalised_agent import GeneralizedAgent
from storage.storage import Storage
from dotenv import load_dotenv  # For loading environment variables from .env file


def setup_logging(config):
    logging.basicConfig(
        filename=config['langgraph']['logging']['file'],
        level=getattr(logging, config['langgraph']['logging']['level']),
        format='%(asctime)s %(levelname)s:%(message)s'
    )


def main():
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Load configuration
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    logger.info("Starting StartupGPT Workflow")

    # Initialize storage
    storage = Storage()

    # Example user input
    user_input = {
        "industry": "Technology",
        "business_model_type": "Subscription",
        "company_size": "Startup",
        "business_model": "Subscription"  # Added for EconomicsAgent's financial projections
    }

    idea_id = "idea_007"  # Unique identifier for the startup idea

    # Initialize and run LegalAgent
    legal_agent = LegalAgent(config_path='config/config.yaml')
    legal_analysis = legal_agent.process(user_input)
    storage.store_output(agent_type="Legal", output_data=legal_analysis, idea_id=idea_id)
    logger.info("Legal analysis stored successfully.")

    # Initialize and run EconomicsAgent
    economics_agent = EconomicsAgent(config_path='config/config.yaml')
    economic_analysis = economics_agent.process(input_data=user_input)
    storage.store_output(agent_type="Economics", output_data=economic_analysis, idea_id=idea_id)
    logger.info("Economic analysis stored successfully.")

    # Initialize and run BusinessStructureAgent
    business_structure_agent = BusinessStructureAgent(config_path='config/config.yaml')
    business_structure_analysis = business_structure_agent.process(input_data=user_input)
    storage.store_output(agent_type="BusinessStructure", output_data=business_structure_analysis, idea_id=idea_id)
    logger.info("Business structure analysis stored successfully.")

    # Initialize and run GeneralizedAgent
    generalized_agent = GeneralizedAgent(config_path='config/config.yaml')
    comprehensive_report = generalized_agent.process(storage, idea_id)
    storage.store_output(agent_type="ComprehensiveReport", output_data=comprehensive_report, idea_id=idea_id)
    logger.info("Comprehensive report stored successfully.")

    # Retrieve and print the comprehensive report
    retrieved_report = storage.retrieve_outputs(idea_id).get("ComprehensiveReport", "No report found.")
    print("----- Comprehensive StartupGPT Report -----")
    print(retrieved_report)


if __name__ == "__main__":
    main()
