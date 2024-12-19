import wmi
import socket
import csv
import os
from datetime import datetime
from tqdm import tqdm

def get_installed_programs():
    """Get all installed programs information on this machine"""
    computer = wmi.WMI()
    programs = []
    hostname = socket.gethostname()

    # First get total program count for progress bar
    print("Counting installed programs...")
    # Wrap WMI query process with tqdm
    with tqdm(desc="Counting progress", unit="items") as pbar:
        all_programs = []
        for prog in computer.Win32_Product():
            all_programs.append(prog)
            pbar.update(1)
    
    total_programs = len(all_programs)
    print(f"Found {total_programs} installed programs")
    print("-" * 50)
    
    print("Getting program details...")
    # 使用tqdm创建进度条
    for program in tqdm(all_programs, total=total_programs, desc="Progress"):
        if program.Name:
            install_date = None
            if program.InstallDate:
                # 转换安装日期格式 (YYYYMMDD to YYYY-MM-DD)
                install_date = f"{program.InstallDate[0:4]}-{program.InstallDate[4:6]}-{program.InstallDate[6:8]}"

            programs.append({
                'hostname': hostname,
                'name': program.Name,
                'version': program.Version,
                'install_date': install_date,
                'vendor': program.Vendor,
                'install_location': program.InstallLocation
            })

    return programs

def save_to_csv(programs, output_file, mode='w'):
    """Save program information to CSV file"""
    fieldnames = ['hostname', 'name', 'version', 'install_date', 'vendor', 'install_location']
    
    file_exists = os.path.exists(output_file)
    
    print("Saving data...")
    with open(output_file, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w' or not file_exists:
            writer.writeheader()
        # 使用tqdm显示保存进度
        for program in tqdm(programs, desc="Save progress"):
            writer.writerow(program)

def read_csv_data(file_path):
    """Read CSV file data"""
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    return data

def update_host_data(data, new_programs, hostname):
    """Update specified host data"""
    return [prog for prog in data if prog['hostname'] != hostname] + new_programs

def get_unique_hosts(data):
    """Get all unique hostnames from CSV file"""
    return sorted(list(set(prog['hostname'] for prog in data)))

def select_hosts(hosts):
    """Let user select hosts to compare"""
    selected_hosts = []
    
    while True:
        print("\nAvailable hosts:")
        for i, host in enumerate(hosts, 1):
            if host in selected_hosts:
                print(f"{i}. [Selected] {host}")
            else:
                print(f"{i}. {host}")
        
        print("\nCurrently selected:", ", ".join(selected_hosts) if selected_hosts else "None")
        print("\nSelect host number to compare (enter 0 to finish):")
        
        try:
            choice = int(input("Enter number: "))
            if choice == 0:
                if len(selected_hosts) < 2:
                    print("Please select at least two hosts to compare!")
                    continue
                break
            elif 1 <= choice <= len(hosts):
                host = hosts[choice-1]
                if host in selected_hosts:
                    selected_hosts.remove(host)
                    print(f"Unselected: {host}")
                else:
                    selected_hosts.append(host)
                    print(f"Selected: {host}")
            else:
                print("Invalid choice, please try again!")
        except ValueError:
            print("Please enter a valid number!")
    
    return selected_hosts

def compare_programs(data, selected_hosts, compare_type):
    """Compare programs between selected hosts"""
    # Group programs by hostname
    programs_by_host = {host: [] for host in selected_hosts}
    for prog in data:
        if prog['hostname'] in selected_hosts:
            programs_by_host[prog['hostname']].append(prog)
    
    # Create program name sets
    program_sets = {
        host: set(prog['name'] for prog in programs)
        for host, programs in programs_by_host.items()
    }
    
    if compare_type == 'common':
        # Find common programs
        common_programs = set.intersection(*program_sets.values())
        result_programs = []
        for prog in data:
            if prog['hostname'] in selected_hosts and prog['name'] in common_programs:
                result_programs.append(prog)
    else:  # compare_type == 'different'
        # Find different programs
        all_programs = set.union(*program_sets.values())
        common_programs = set.intersection(*program_sets.values())
        different_programs = all_programs - common_programs
        result_programs = []
        for prog in data:
            if prog['hostname'] in selected_hosts and prog['name'] in different_programs:
                result_programs.append(prog)
    
    return result_programs

def compare_mode():
    """Compare mode handler"""
    compare_file = "installed_programs_compare.csv"
    hostname = socket.gethostname()
    
    # Read existing data
    print("Reading comparison file...")
    existing_data = read_csv_data(compare_file)
    
    if not existing_data:
        print("Comparison file is empty or doesn't exist. Please add host data first!")
        return
    
    # Check if current host exists in data
    host_exists = any(prog['hostname'] == hostname for prog in existing_data)
    
    if host_exists:
        update = input(f"Found existing data for {hostname}. Update? (y/n): ").lower() == 'y'
        if update:
            print("Getting current host program information...")
            new_programs = get_installed_programs()
            print("Updating data...")
            existing_data = update_host_data(existing_data, new_programs, hostname)
            save_to_csv(existing_data, compare_file, 'w')
    else:
        add_current = input("Current host data not found. Add it? (y/n): ").lower() == 'y'
        if add_current:
            print("Getting current host program information...")
            new_programs = get_installed_programs()
            existing_data.extend(new_programs)
            save_to_csv(existing_data, compare_file, 'w')
    
    # Get all available hosts
    available_hosts = get_unique_hosts(existing_data)
    if len(available_hosts) < 2:
        print("Need at least two hosts' data to compare!")
        return
    
    # Select hosts to compare
    selected_hosts = select_hosts(available_hosts)
    
    # Select comparison type
    while True:
        print("\nSelect comparison type:")
        print("1. Compare common programs")
        print("2. Compare different programs")
        choice = input("Enter option (1/2): ").strip()
        
        if choice in ['1', '2']:
            compare_type = 'common' if choice == '1' else 'different'
            break
        print("Invalid choice, please try again!")
    
    # Execute comparison
    result_programs = compare_programs(existing_data, selected_hosts, compare_type)
    
    # Save comparison results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    compare_type_str = 'common' if compare_type == 'common' else 'different'
    output_file = f"compare_result_{compare_type_str}_{timestamp}.csv"
    
    save_to_csv(result_programs, output_file)
    print(f"\nComparison complete! Found {len(result_programs)} {compare_type_str} programs.")
    print(f"Results saved to: {output_file}")

def single_mode():
    """Single mode handler"""
    output_file = f"installed_programs_{datetime.now().strftime('%Y%m%d')}.csv"
    
    print("Getting installed program information...")
    programs = get_installed_programs()
    
    save_to_csv(programs, output_file)
    
    print(f"Complete! Found {len(programs)} installed programs.")
    print(f"Data saved to: {output_file}")

def main():
    try:
        print("\nSelect operation mode:")
        print("1. Get current host program information")
        print("2. Compare different hosts program information")
        print("3. Exit")
        
        choice = input("Enter option (1-3): ").strip()
        
        if choice == '1':
            single_mode()
        elif choice == '2':
            compare_mode()
        elif choice == '3':
            print("Program exited.")
        else:
            print("Invalid choice!")
            return
        
        if choice in ['1', '2']:
            print("\nOperation complete, program exited.")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
