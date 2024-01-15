import pandas as pd
import json
import os
from datetime import datetime

def policy_generator(df):
    # Process the DataFrame to get unique routes and associated roles
    policies = {}
    for _, row in df.iterrows():
        resource = row['App Route'].replace('-', '').replace('_', '').lower()
        roles = row['Roles'].split(',')
        if resource not in policies:
            policies[resource] = set()
        policies[resource].update(roles)

    # Create the directory for policies
    dir_name = f"generated-policies/policies-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    os.makedirs(dir_name, exist_ok=True)

    # Generate and save policy files
    for resource, roles in policies.items():
        policy = {
            "policies": [
                {
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
            ]
        }
        with open(f"{dir_name}/{resource}.json", 'w') as f:
            json.dump(policy, f, indent=2)

    return f"Policies generated in {dir_name}"

# Usage example:
# df = pd.read_csv('path_to_your_csv_file.csv')
# response = policy_generator(df)
# print(response)