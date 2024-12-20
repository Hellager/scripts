import os
import csv
import socket
import pandas as pd


def get_environment_variables():
    # Get all environment variables and hostname
    env_vars = dict(os.environ)
    hostname = socket.gethostname()

    # Prepare data list
    env_data = []
    for key, value in env_vars.items():
        env_data.append({
            'Hostname': hostname,
            'Variable': key,
            'Value': value,
            'Type': 'System/User Environment Variable'
        })

    return env_data


def export_to_csv(data):
    filename = 'windows_environment.csv'

    try:
        # If file exists, read existing data
        if os.path.exists(filename):
            df_existing = pd.read_csv(filename)
            df_new = pd.DataFrame(data)

            # Remove old records with the same hostname
            hostname = data[0]['Hostname']
            df_existing = df_existing[df_existing['Hostname'] != hostname]

            # Merge new and existing data
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(filename, index=False)
        else:
            # If file doesn't exist, write new data directly
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Hostname', 'Variable', 'Value', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    except Exception:
        print(f"${Exception}")

    return filename


def get_available_hosts():
    filename = 'windows_environment.csv'
    if not os.path.exists(filename):
        return []
    df = pd.read_csv(filename)
    return df['Hostname'].unique().tolist()


def compare_environments(host1, host2):
    df = pd.read_csv('windows_environment.csv')

    # Get environment variables for both hosts
    env1 = df[df['Hostname'] == host1].set_index('Variable')['Value']
    env2 = df[df['Hostname'] == host2].set_index('Variable')['Value']

    # Compare differences
    all_vars = sorted(set(env1.index) | set(env2.index))
    differences = []

    for var in all_vars:
        val1 = env1.get(var, 'Not Set')
        val2 = env2.get(var, 'Not Set')
        if val1 != val2:
            differences.append({
                'Variable': var,
                f'{host1}': val1,
                f'{host2}': val2
            })

    return differences


def main():
    try:
        while True:
            print("\nPlease select an operation:")
            print("1. Export local environment variables")
            print("2. Compare host environment variables")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                env_data = get_environment_variables()
                output_file = export_to_csv(env_data)
                print(f'Environment variables successfully exported to: {output_file}')

            elif choice == '2':
                hosts = get_available_hosts()
                if not hosts:
                    print("No saved environment variable data found. Please export environment variables first.")
                    continue

                update_local = input("Update local environment variables? (y/n): ").lower()
                if update_local == 'y':
                    env_data = get_environment_variables()
                    export_to_csv(env_data)
                    print("Local environment variables updated")

                print("\nAvailable hosts:")
                for i, host in enumerate(hosts, 1):
                    print(f"{i}. {host}")

                host1 = socket.gethostname()
                host2_idx = int(input("\nSelect host number to compare: ")) - 1
                host2 = hosts[host2_idx]

                differences = compare_environments(host1, host2)
                if differences:
                    print(f"\nEnvironment variable differences between {host1} and {host2}:")
                    for diff in differences:
                        print(f"\nVariable: {diff['Variable']}")
                        print(f"{host1}: {diff[host1]}")
                        print(f"{host2}: {diff[host2]}")
                else:
                    print("\nEnvironment variables are identical between the two hosts")

            elif choice == '3':
                print("Program terminated")
                break

            else:
                print("Invalid option, please try again")

    except Exception as e:
        print(f'Error occurred: {str(e)}')


if __name__ == '__main__':
    main()
