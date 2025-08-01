import json
import os
import logging

class Storage:
    def __init__(self, storage_file="storage/data.json"):
        self.storage_file = storage_file
        self.logger = logging.getLogger(__name__)
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({}, f)

    def store_output(self, agent_type, output_data, idea_id):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            if idea_id not in data:
                data[idea_id] = {}
            data[idea_id][agent_type] = output_data
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Stored {agent_type} output for idea_id: {idea_id}")
        except Exception as e:
            self.logger.error(f"Failed to store output: {e}")

    def retrieve_outputs(self, idea_id):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            return data.get(idea_id, {})
        except Exception as e:
            self.logger.error(f"Failed to retrieve outputs: {e}")
            return {}

    def store_report(self, report_content, idea_id):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            if idea_id not in data:
                data[idea_id] = {}
            data[idea_id]['report'] = report_content
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Stored report for idea_id: {idea_id}")
        except Exception as e:
            self.logger.error(f"Failed to store report: {e}")

    def retrieve_report(self, idea_id):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            return data.get(idea_id, {}).get('report', "No report available.")
        except Exception as e:
            self.logger.error(f"Failed to retrieve report: {e}")
            return "Error retrieving report."
