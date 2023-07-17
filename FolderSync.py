import os, shutil, filecmp, time, argparse, logging, hashlib

def calculate_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536) # 64 KB Block
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def synchronize_folders(src_dir, repl_dir, interval, log_file):
    # Check folders
    if not os.path.exists(src_dir):
        print(f"Source folder '{src_dir}' does not exist.")
        return
    if not os.path.exists(repl_dir):
        os.makedirs(repl_dir)

    # First run then repeat
    synchronize(src_dir, repl_dir, log_file)
    while True:
        time.sleep(interval)
        synchronize(src_dir, repl_dir, log_file)

def synchronize(src_dir, repl_dir, log_file):
    log_entries = []

    # Delete dirs if not in source
    for root, dirs, files in os.walk(repl_dir, topdown=False):
        source_root = os.path.join(src_dir, os.path.relpath(root, repl_dir))
        replica_dirs = [d for d in dirs if not os.path.exists(os.path.join(source_root, d))]
        for dir in replica_dirs:
            replica_dir = os.path.join(root, dir)
            shutil.rmtree(replica_dir)
            log_entries.append(f"Folder deleted: {replica_dir}")

    # Recursive through source
    for root, dirs, files in os.walk(src_dir):
        replica_root = os.path.join(repl_dir, os.path.relpath(root, src_dir))

        # Delete files if not in source
        replica_files = [f for f in os.listdir(replica_root) if os.path.isfile(os.path.join(replica_root, f))]
        for replica_file in replica_files:
            src_file = os.path.join(root, replica_file)
            replica_file = os.path.join(replica_root, replica_file)
            if not os.path.exists(src_file) or calculate_hash(src_file) != calculate_hash(replica_file):
                os.remove(replica_file)
                log_entries.append(f"File deleted: {replica_file}")

        # Make dirs if not in replica
        for dir in dirs:
            replica_dir = os.path.join(replica_root, dir)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                log_entries.append(f"Folder created: {replica_dir}")

        # Copy files if not the same
        for file in files:
            src_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)
            if not os.path.exists(replica_file) or calculate_hash(src_file) != calculate_hash(replica_file):
                shutil.copy2(src_file, replica_file)
                log_entries.append(f"File copied: {src_file} -> {replica_file}")

    # Log the changes
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    for entry in log_entries:
        logging.info(entry)
        print(entry)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Folder synchronization script')
    parser.add_argument('source', help='Source folder')
    parser.add_argument('replica', help='Replica folder')
    parser.add_argument('interval', type=int, help='Sync interval (seconds)')
    parser.add_argument('log', help='Log file')

    args = parser.parse_args()
    src_dir = args.source
    repl_dir = args.replica
    interval = args.interval
    log_file = args.log

    synchronize_folders(src_dir, repl_dir, interval, log_file)