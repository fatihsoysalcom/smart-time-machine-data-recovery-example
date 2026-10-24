import os
import shutil
from datetime import datetime
import time

# --- Configuration ---
PROJECT_FILE = "my_project_data.txt"
HISTORY_DIR = "project_history"

# --- Helper Functions ---
def init_project():
    """Initializes the project file and history directory."""
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
        print(f"Created history directory: {HISTORY_DIR}")

    if not os.path.exists(PROJECT_FILE):
        with open(PROJECT_FILE, "w") as f:
            f.write("Initial project state.\n")
        print(f"Created initial project file: {PROJECT_FILE}")

def save_snapshot(message=""):
    """
    Saves the current state of the project file as a timestamped snapshot.
    This simulates the "Smart Time Machine" saving a version.
    """
    if not os.path.exists(PROJECT_FILE):
        print(f"Error: Project file '{PROJECT_FILE}' does not exist to save.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize message for filename
    sanitized_message = ''.join(c if c.isalnum() else '_' for c in message).strip('_')
    snapshot_filename = f"{timestamp}_{sanitized_message}.txt"
    snapshot_path = os.path.join(HISTORY_DIR, snapshot_filename)

    shutil.copy(PROJECT_FILE, snapshot_path)
    print(f"Snapshot saved: {snapshot_filename}")
    return snapshot_filename # Return for easier restoration later

def list_snapshots():
    """
    Lists all available snapshots in the history directory.
    This shows the available points for data recovery.
    """
    print(f"\n--- Available Snapshots in '{HISTORY_DIR}' ---")
    snapshots = sorted(os.listdir(HISTORY_DIR))
    if not snapshots:
        print("No snapshots found.")
        return []
    for i, snapshot in enumerate(snapshots):
        print(f"  {i+1}. {snapshot}")
    return snapshots

def restore_snapshot(snapshot_name):
    """
    Restores the project file to a specific snapshot state.
    This demonstrates the "Smart Time Machine's" data recovery capability.
    """
    snapshot_path = os.path.join(HISTORY_DIR, snapshot_name)
    if not os.path.exists(snapshot_path):
        print(f"Error: Snapshot '{snapshot_name}' not found.")
        return False

    shutil.copy(snapshot_path, PROJECT_FILE)
    print(f"Project restored to snapshot: {snapshot_name}")
    return True

def read_project_file():
    """Reads and prints the current content of the project file."""
    if os.path.exists(PROJECT_FILE):
        with open(PROJECT_FILE, "r") as f:
            print(f"\n--- Current '{PROJECT_FILE}' Content ---")
            print(f.read().strip())
            print("---------------------------------------")
    else:
        print(f"'{PROJECT_FILE}' does not exist.")

def cleanup():
    """Removes the project file and history directory."""
    print("\n--- Cleaning up demo files ---")
    if os.path.exists(PROJECT_FILE):
        os.remove(PROJECT_FILE)
        print(f"Removed {PROJECT_FILE}")
    if os.path.exists(HISTORY_DIR):
        shutil.rmtree(HISTORY_DIR)
        print(f"Removed {HISTORY_DIR} directory")

# --- Main Demonstration ---
if __name__ == "__main__":
    cleanup() # Ensure a clean start for the demo
    init_project()

    print("\n--- Step 1: Initial State & First Snapshot ---")
    read_project_file()
    first_snapshot_name = save_snapshot("initial_version") # Illustrates saving a project state
    time.sleep(1) # Ensure unique timestamps

    print("\n--- Step 2: Modify Project & Second Snapshot ---")
    with open(PROJECT_FILE, "a") as f:
        f.write("Added feature A.\n")
    read_project_file()
    second_snapshot_name = save_snapshot("feature_A_added") # Illustrates saving another project state
    time.sleep(1)

    print("\n--- Step 3: Further Modify Project & Third Snapshot ---")
    with open(PROJECT_FILE, "a") as f:
        f.write("Fixed bug B and added feature C.\n")
    read_project_file()
    third_snapshot_name = save_snapshot("bug_B_fixed_feature_C_added") # Illustrates saving a final project state
    time.sleep(1)

    print("\n--- Step 4: List All Snapshots ---")
    all_snapshots = list_snapshots()

    print("\n--- Step 5: Simulate an error or undesired change ---")
    with open(PROJECT_FILE, "w") as f: # Overwrite with bad data
        f.write("Oops! This is bad data that overwrites everything.\n")
    read_project_file()

    print("\n--- Step 6: Restore to an earlier state (e.g., 'feature_A_added') ---")
    # Find the snapshot name for "feature_A_added"
    snapshot_to_restore = None
    for s in all_snapshots:
        if "feature_A_added" in s:
            snapshot_to_restore = s
            break

    if snapshot_to_restore:
        restore_snapshot(snapshot_to_restore) # This is the "Smart Time Machine" in action, restoring data
        read_project_file()
    else:
        print("Could not find 'feature_A_added' snapshot to restore.")

    print("\n--- Step 7: Restore to the very first state ('initial_version') ---")
    snapshot_to_restore_initial = None
    for s in all_snapshots:
        if "initial_version" in s:
            snapshot_to_restore_initial = s
            break

    if snapshot_to_restore_initial:
        restore_snapshot(snapshot_to_restore_initial) # Another demonstration of data recovery
        read_project_file()
    else:
        print("Could not find 'initial_version' snapshot to restore.")

    cleanup()
