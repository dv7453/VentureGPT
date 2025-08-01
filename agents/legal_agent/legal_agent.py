# agents/legal_agent.py

import yaml
import logging
from .legal_agent_helper import LegalAgentHelper


class LegalAgent:
    def __init__(self, config_path='config/config.yaml'):
        # Load configuration
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Extract API key for Groq (assuming it's stored here)
        llama_api_key = config['agents']['legal_agent']['llama_api_key']

        # Initialize helper functions
        self.helper = LegalAgentHelper(llama_api_key_env_var='LEGAL_AGENT_API_KEY')

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def process(self, input_data):
        """
        Processes the input data to perform legal analysis.
        """
        try:
            self.logger.info("Starting legal analysis.")

            # Extract relevant information from input_data
            # Ensure that input_data contains 'industry' and 'business_model'
            industry = input_data.get('industry', 'General')
            business_model = input_data.get('business_model', 'Standard')  # e.g., Subscription, Freemium

            # Fetch regulations
            regulations = self.helper.fetch_regulations(industry)

            # Generate compliance checklist
            compliance_checklist = self.helper.generate_compliance_checklist(regulations)

            # Assess legal risks
            legal_risks = self.helper.assess_legal_risks(business_model)

            # Compile the analysis
            analysis = {
                "regulations": regulations,
                "compliance_checklist": compliance_checklist,
                "legal_risks": legal_risks
            }

            # Format the analysis into a readable string
            formatted_analysis = self.format_analysis(analysis)

            self.logger.info("Legal analysis completed successfully.")
            return formatted_analysis
        except Exception as e:
            self.logger.error(f"Error during legal analysis: {e}")
            return "An error occurred during legal analysis."

    def format_analysis(self, analysis):
        """
        Formats the analysis dictionary into a readable string.
        """
        try:
            formatted = "**Regulations:**\n"
            formatted += f"\n{analysis['regulations']}\n"
            # formatted += f"Data Protection Laws: {analysis['regulations'].get('data_protection_laws', 'N/A')}\n"
            # formatted += f"Licensing Requirements: {analysis['regulations'].get('licensing_requirements', 'N/A')}\n"
            # formatted += f"Compliance Standards: {analysis['regulations'].get('compliance_standards', 'N/A')}\n"
            # formatted += f"Other Regulations: {', '.join(analysis['regulations'].get('other_regulations', []))}\n"

            formatted += "\n**Compliance Checklist:**\n"
            formatted += f"{analysis['compliance_checklist']}\n"
            # for idx, item in enumerate(analysis['compliance_checklist'], 1):
            #     formatted += f"{idx}. {item}\n"

            formatted += "\n**Legal Risks:**\n"
            formatted += f"{analysis['legal_risks']}\n"
            # for idx, risk in enumerate(analysis['legal_risks'], 1):
            #     formatted += f"{idx}. {risk}\n"

            return formatted
        except Exception as e:
            self.logger.error(f"Error formatting analysis: {e}")
            return "Unable to format legal analysis at this time."
