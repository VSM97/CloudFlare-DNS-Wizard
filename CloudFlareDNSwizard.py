import CloudFlare
import os
import requests

def get_api_details():
    if not os.path.isfile('config.txt'):
        print("Welcome to Cloudflare DNS Wizard!")
        email = input("Enter your Cloudflare email: ").strip()
        api_token = input("Enter your Cloudflare API token: ").strip()
        zone_id = input("Enter your Cloudflare Zone ID: ").strip()
        identifier = input("Enter your Cloudflare Account ID: ").strip()

        # Save API details to a config file
        with open('config.txt', 'w') as config_file:
            config_file.write(f"email={email}\n")
            config_file.write(f"api_token={api_token}\n")
            config_file.write(f"zone_id={zone_id}\n")
            config_file.write(f"identifier={identifier}\n")
    else:
        # Load API details from the config file
        with open('config.txt', 'r') as config_file:
            lines = config_file.readlines()
            email = lines[0].strip().split('=')[1]
            api_token = lines[1].strip().split('=')[1]
            zone_id = lines[2].strip().split('=')[1]
            identifier = lines[3].strip().split('=')[1]

    return email, api_token, zone_id, identifier

def display_zone_info(email, api_token, zone_id):
    try:
        # Initialize Cloudflare client
        cf = CloudFlare.CloudFlare(email=email, token=api_token)

        # Fetch and display zone information using Cloudflare API
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            zone_info = response.json()["result"]
            print("Zone Information:")
            print(f"Name: {zone_info['name']}")
            print(f"Status: {zone_info['status']}")
            print(f"Development Mode: {zone_info['development_mode']}")
        else:
            print(f"Failed to fetch zone information. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while fetching zone information: {str(e)}")

def display_account_info(email, api_token, identifier):
    try:
        # Initialize Cloudflare client
        cf = CloudFlare.CloudFlare(email=email, token=api_token)

        # Fetch account information using Cloudflare API with the provided account identifier
        url = f"https://api.cloudflare.com/client/v4/accounts/{identifier}"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        #print("Request Headers:")
        #print(headers)  # Log the headers being sent

        if response.status_code == 200:
            account_info = response.json()["result"]
            print("Account Information:")
            print(f"Name: {account_info['name']}")
            print(f"Type: {account_info['type']}")
            print(f"Two factor enabled: {account_info['settings']['enforce_twofactor']}")
            print(f"Default nameservers: {account_info['settings']['default_nameservers']}")
            print(f"Created on: {account_info['created_on']}")
        else:
            print(f"Failed to fetch account information. Status code: {response.status_code}")
            print("Response Headers:")
            print(response.headers)  # Log the response headers
            print("Response Content:")
            print(response.text)  # Log the response content

    except Exception as e:
        print(f"An error occurred while fetching account information: {str(e)}")
        
def fetch_dns_records(email, api_token, zone_id):
    try:
        # Initialize Cloudflare client
        cf = CloudFlare.CloudFlare(email=email, token=api_token)

        # Fetch DNS records using Cloudflare API
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse and display DNS records
            dns_records = response.json()["result"]
            print("DNS Records:")
            for record in dns_records:
                print(f"Type: {record['type']}, Name: {record['name']}, Content: {record['content']}")
        else:
            print(f"Failed to fetch DNS records. Status code: {response.status_code}")
            print("Response Headers:")
            print(response.headers)  # Log the response headers
            print("Response Content:")
            print(response.text)  # Log the response content

    except Exception as e:
        print(f"An error occurred while fetching DNS records: {str(e)}")

def update_dns_records(email, api_token, zone_id, record_type, new_content):
    try:
        # Fetch DNS records for the specified record type
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dns_records = response.json()["result"]

            # Loop through the DNS records and update their content
            for record in dns_records:
                record_id = record["id"]
                record_name = record["name"]
                update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
                data = {
                    "content": new_content
                }
                update_response = requests.patch(update_url, json=data, headers=headers)

                if update_response.status_code == 200:
                    print(f"Updated DNS record {record_name} with new content: {new_content}")
                else:
                    print(f"Failed to update DNS record {record_name}. Status code: {update_response.status_code}")
                    print("Response Headers:")
                    print(response.headers)  # Log the response headers
                    print("Response Content:")
                    print(response.text)  # Log the response content
        else:
            print(f"Failed to fetch DNS records. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while updating DNS records: {str(e)}")



def add_dns_records(email, api_token, zone_id, record_type, new_records):
    try:
        # Loop through the new records and add them to the DNS zone
        for new_record in new_records:
            content, name = new_record.split(' ')
            data = {
                "type": record_type,
                "name": name,
                "content": content,
                "ttl": 1,
                "proxied": False
            }

            # Add the new DNS record using Cloudflare API
            url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                print(f"Added DNS record: Type - {record_type}, Name - {name}, Content - {content}")
            else:
                print(f"Failed to add DNS record: Type - {record_type}, Name - {name}, Content - {content}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while adding DNS records: {str(e)}")


def remove_dns_records(email, api_token, zone_id, identifier):
    try:
        # Fetch DNS records using Cloudflare API
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dns_records = response.json()["result"]

            # Display DNS records for selection
            print("Select DNS records to remove:")
            for index, record in enumerate(dns_records, start=1):
                print(f"{index}. Type - {record['type']}, Name - {record['name']}, Content - {record['content']}")

            selection = input("Enter the numbers corresponding to the records to remove (e.g., 1-3,5,10-15): ").strip()

            # Parse the selection input into individual indices
            selected_indices = []
            ranges = selection.split(',')
            for r in ranges:
                if '-' in r:
                    start, end = map(int, r.split('-'))
                    selected_indices.extend(range(start, end + 1))
                else:
                    selected_indices.append(int(r))

            # Remove selected DNS records using Cloudflare API
            for index in selected_indices:
                if 1 <= index <= len(dns_records):
                    record_id = dns_records[index - 1]["id"]
                    delete_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
                    delete_response = requests.delete(delete_url, headers=headers)

                    if delete_response.status_code == 200:
                        print(f"Removed DNS record: Type - {dns_records[index - 1]['type']}, Name - {dns_records[index - 1]['name']}, Content - {dns_records[index - 1]['content']}")
                    else:
                        print(f"Failed to remove DNS record: Type - {dns_records[index - 1]['type']}, Name - {dns_records[index - 1]['name']}, Content - {dns_records[index - 1]['content']}. Status code: {delete_response.status_code}")
                        print("Response Headers:")
                        print(response.headers)  # Log the response headers
                        print("Response Content:")
                        print(response.text)  # Log the response content
                else:
                    print(f"Invalid selection: {index}")

        else:
            print(f"Failed to fetch DNS records. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred while removing DNS records: {str(e)}")


def purge_api_details():
    if os.path.isfile('config.txt'):
        os.remove('config.txt')
        print("API details purged. You can now start the script from the beginning.")

def main():
    email, api_token, zone_id, identifier = get_api_details()

    while True:
        print("\n")
        print("Welcome to the CloudFlare DNS wizard by VSM")
        print("\n")
        print("Select an action:")
        print("1. Fetch DNS Records")
        print("2. Display Zone Information")
        print("3. Display Account Information")
        print("4. Update DNS Records")
        print("5. Add New DNS Records")
        print("6. Remove DNS Records")
        print("7. Purge API Details and Start Over")
        print("8. Exit")

        action = input("Enter the number corresponding to the action: ").strip()

        if action == '1':
            fetch_dns_records(email, api_token, zone_id)
        elif action == '2':
            display_zone_info(email, api_token, zone_id)
        elif action == '3':
            display_account_info(email, api_token, identifier)
        elif action == '4':
            print("Select a DNS record type:")
            print("1. A records")
            print("2. AAAA records")
            print("3. CNAME records")
            print("4. MX records")
            print("5. TXT records")
            print("6. NS records")

            record_type_input = input("Enter the number corresponding to the DNS record type: ").strip()

            if record_type_input == '1':
                record_type = 'A'
            elif record_type_input == '2':
                record_type = 'AAAA'
            elif record_type_input == '3':
                record_type = 'CNAME'
            elif record_type_input == '4':
                record_type = 'MX'
            elif record_type_input == '5':
                record_type = 'TXT'
            elif record_type_input == '6':
                record_type = 'NS'
            else:
                print("Invalid DNS record type selection.")
                continue  # Return to the main menu

            new_content = input("Enter the new content for the records: ").strip()
            update_dns_records(email, api_token, zone_id, record_type, new_content)
        elif action == '5':
            print("Select a DNS record type:")
            print("1. A records")
            print("2. AAAA records")
            print("3. CNAME records")
            print("4. MX records")
            print("5. TXT records")
            print("6. NS records")

            record_type_input = input("Enter the number corresponding to the DNS record type: ").strip()

            if record_type_input == '1':
                record_type = 'A'
            elif record_type_input == '2':
                record_type = 'AAAA'
            elif record_type_input == '3':
                record_type = 'CNAME'
            elif record_type_input == '4':
                record_type = 'MX'
            elif record_type_input == '5':
                record_type = 'TXT'
            elif record_type_input == '6':
                record_type = 'NS'
            else:
                print("Invalid DNS record type selection.")
                input("Press Enter to continue...")  # Wait for user input to clear the input buffer
                continue  # Return to the main menu

            new_records = []
            while True:
                print("Enter the new DNS record (IP Address followed by domain, separated by a space):")
                new_record_input = input().strip()
                if not new_record_input:
                    break  # If the user enters an empty line, exit the loop
                new_records.append(new_record_input)
            add_dns_records(email, api_token, zone_id, record_type, new_records)
        elif action == '6':
            remove_dns_records(email, api_token, zone_id, identifier)
        elif action == '7':
            purge_api_details()
        elif action == '8':
            break
        else:
            print("Invalid action selection.")

if __name__ == "__main__":
    main()








