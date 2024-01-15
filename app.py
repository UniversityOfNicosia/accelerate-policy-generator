import pandas as pd
import json
import os
from datetime import datetime

class PolicyGenerator:
    def __init__(self, df):
        self.df = df

    def process_dataframe(self):
        policies = {}
        for _, row in self.df.iterrows():
            resource = row['App Route'].replace('-', '').replace('_', '').replace('/', '').lower()
            roles = row['Roles'].split(',')
            if resource not in policies:
                policies[resource] = set()
            policies[resource].update(roles)

        return {resource: self.generate_policy(resource, roles) for resource, roles in policies.items()}

    def generate_policy(self, resource, roles):
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
        policies = self.process_dataframe()
        for resource, policy in policies.items():
            print(json.dumps(policy, indent=2))

# Usage example:
df = pd.read_csv('api_endpoints.csv')
generator = PolicyGenerator(df)
generator.generate()