"""
This file contains classes and methods for generating policies.
"""

# Import libraries
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd


class PolicyGenerator:
    """
    A class for generating policies based on a dataframe.
    """
    def __init__(self, df):
        self.df = df
    
    def validate(self):
        load_dotenv()
        body = {
            "email": os.getenv('API_username'),
            "password": os.getenv('API_password')
            }
        headers = {
            "Content-Type": "application/json", 
            }
        response = requests.post(os.getenv('API_URL')+'/auth/login', data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            # return (json.loads(response.text)['accessToken'])
            self.jwt = json.loads(response.text)['accessToken']
        else:
            raise Exception("Invalid credentials")


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
  "policies": [
    {
      "apiVersion": "api.cerbos.dev/v1",
     
      "resourcePolicy": {
        "resource": resource,
        "version": "1",
        "rules": [
        {
          "actions": ["create", "read", "update", "delete"],
          "roles": ["DEVELOPER", "SYS_ADMIN"],
          "effect": "EFFECT_ALLOW"
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

    #def basic_auth(username, password):
        #token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        #return f'Basic {token}'

    def add_update_local_cerbos(self, policy_data):
        load_dotenv()
    # Convert the policy data to JSON
        policy_json = json.dumps(policy_data)
    # Set the appropriate headers, if required
        headers = {
        "Content-Type": "application/json",
        #"Authorization" : basic_auth(username, password)   
        }
    # Make the POST request
        response = requests.post(os.getenv('CERBOS_URL')+'/admin/policy', data=policy_json, headers=headers, auth=('cerbos', 'cerbosAdmin'))
    # Check the response
        print(response.text)       
        if response.status_code == 200:
            return (1) # Success
        else:
            print(json.dumps(policy_data, indent=2))
            return (0) # Failure



    def add_update_accelerate_cerbos(self, policy_data):
        load_dotenv()
    # Convert the policy data to JSON
        policy_json = json.dumps(policy_data)
    # Set the appropriate headers, if required
        headers = {
        "Content-Type": "application/json",
        "Authorization" : "bearer " + self.jwt
        }

    # Make the POST request
        response = requests.post(os.getenv('API_URL')+'/authorization-admin', data=policy_json, headers=headers)
    # Check the response
        print(response.text)
        if response.status_code == 200:
            return (1) # Success
        else:
            print(json.dumps(policy_data, indent=2))
            return (0) # Failure



    def generate(self):
        """
        Generates and prints the policies.
        """
        policies = self.process_dataframe()
        for resource, policy in policies.items():
            #print(json.dumps(policy, indent=2))
            #self.add_update_local_cerbos(policy)
            self.add_update_accelerate_cerbos(policy)

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
generator = PolicyGenerator(df)

generator.validate()

generator.generate()