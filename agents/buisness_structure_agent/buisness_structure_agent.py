import yaml
import logging
from .buisness_structure_agent_helper import BusinessStructureAgentHelper


class BusinessStructureAgent:
    def __init__(self, config_path='config/config.yaml'):
        # Load configuration
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Extract API key for Groq (assuming it's stored here)
        llama_api_key = config['agents']['business_structure_agent']['llama_api_key']

        # Initialize helper functions
        self.helper = BusinessStructureAgentHelper(llama_api_key=llama_api_key)

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def process(self, input_data):
        """
        Processes the input data to perform business structure analysis.
        """
        try:
            self.logger.info("Starting business structure analysis.")

            # Extract relevant information from input_data
            # Ensure that input_data contains 'industry', 'business_model_type', and 'company_size'
            industry = input_data.get('industry', 'General')
            business_model_type = input_data.get('business_model_type', 'Standard')  # e.g., Subscription, Freemium
            company_size = input_data.get('company_size', 'Startup')  # e.g., Startup, Small, Medium, Large

            # Propose business models
            proposed_models = self.helper.propose_business_models(industry, business_model_type)

            # Map organizational structure
            organizational_structure = self.helper.map_organizational_structure(company_size)

            # Plan scalability
            scalability_plan = self.helper.plan_scalability(business_model_type, organizational_structure)

            # Compile the analysis
            analysis = {
                "proposed_business_models": proposed_models,
                "organizational_structure": organizational_structure,
                "scalability_plan": scalability_plan
            }

            # Format the analysis into a readable string
            formatted_analysis = self.format_analysis(analysis)

            self.logger.info("Business structure analysis completed successfully.")
            return formatted_analysis
        except Exception as e:
            self.logger.error(f"Error during business structure analysis: {e}")
            return "An error occurred during business structure analysis."

    def format_analysis(self, analysis):
        """
        Formats the analysis dictionary into a readable string.
        """
        try:
            formatted = "**Proposed Business Models:**\n"
            formatted += f"{analysis['proposed_business_models']}\n"
            # for idx, model in enumerate(analysis['proposed_business_models'], 1):
            #     formatted += f"{idx}. {model}\n"

            formatted += "\n**Organizational Structure:**\n"
            formatted += f"{analysis['organizational_structure']}\n"
            # for role, responsibility in analysis['organizational_structure'].items():
            #     formatted += f"- **{role}**: {responsibility}\n"

            formatted += "\n**Scalability Plan:**\n"
            formatted += f"{analysis['scalability_plan']}\n"

            return formatted
        except Exception as e:
            self.logger.error(f"Error formatting analysis: {e}")
            return "Unable to format business structure analysis at this time."
