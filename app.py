"""
This file contains classes and methods for generating policies.
"""

# Import libraries
import json
import os
from datetime import datetime
import pandas as pd


class PolicyGenerator:
    """
    A class for generating policies based on a dataframe.
    """

    def __init__(self, df):
        """
        Initializes the PolicyGenerator object.

        Args:
            df (pandas.DataFrame): The input dataframe.
        """
        self.df = df

    def process_dataframe(self):
        """
        Processes the dataframe and generates policies.

        Returns:
            dict: A dictionary of generated policies.
        """
        policies = {}
        for _, row in self.df.iterrows():
            resource = row['App Route'].replace('-', '').replace('_', '').replace('/', '').lower()
            roles = row['Roles'].replace(' ', '').split(',')
            if resource not in policies:
                policies[resource] = set()
            policies[resource].update(roles)

        return {resource: self.generate_policy(resource, roles) for resource, roles in policies.items()}

    def generate_policy(self, resource, roles):
        """
        Generates a policy for a specific resource and roles.

        Args:
            resource (str): The resource name.
            roles (list): The list of roles.

        Returns:
            dict: The generated policy.
        """
        return {
            "apiVersion": "api.cerbos.dev/v1",
            "resourcePolicy": {
                "resource": resource,
                "version": "default",
                "rules": [
                    {
                        "actions": ["create", "read", "update", "delete"],
                        "roles": list(roles),
                        "effect": "EFFECT_ALLOW",
                    },
                    {
                        "actions": ["create", "read", "update", "delete"],
                        "roles": ["*"],
                        "effect": "EFFECT_DENY"
                    }
                ]
            }
        }

    def generate(self):
        """
        Generates and prints the policies.
        """
        policies = self.process_dataframe()
        for resource, policy in policies.items():
            print(json.dumps(policy, indent=2))


class PolicyGeneratorDirectory(PolicyGenerator):
    """
    A class for generating policies and saving them in a directory.
    """

    def generate(self):
        """
        Generates and saves the policies in a directory.

        Returns:
            str: The path where the policies are saved.
        """
        policies = self.process_dataframe()
        dir_name = f"generated-policies/policies-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.makedirs(dir_name, exist_ok=True)

        for resource, policy in policies.items():
            with open(f"{dir_name}/{resource}.json", 'w') as f:
                json.dump(policy, f, indent=2)

        return f"Policies generated in {dir_name}"


class PolicyGeneratorFile(PolicyGenerator):
    """
    A class for generating policies and saving them in a file.
    """

    def generate(self):
        """
        Generates and saves all policies in a file.

        Returns:
            str: The path where the policies are saved.
        """
        policies = self.process_dataframe()
        combined_policies = {"policies": [policy['resourcePolicy'] for policy in policies.values()]}

        file_name = f"generated-policies/cerbos-policies-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w') as f:
            json.dump(combined_policies, f, indent=2)

        return f"All policies generated in {file_name}"


# Usage example:
df = pd.read_csv('api_endpoints.csv')
generator = PolicyGeneratorFile(df)
generator.generate()
