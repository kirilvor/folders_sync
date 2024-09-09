import os
import shutil
import time
import argparse
import hashlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def file_copy(source_path, replica_path):
    """
    Copying or replace item from source path.

    Args:
        source_path (str): Path to the item in source folder.
        replica_path (str): Path to the item in replica folder.
    """
    if not os.path.exists(replica_path):
        replica_hash = None
    else:
        file_r = open(replica_path, 'rb')
        replica_hash = hashlib.sha256(file_r.read()).hexdigest()

    file_s = open(source_path, 'rb')
    hash_s = hashlib.sha256(file_s.read()).hexdigest()

    if replica_hash is None:
        logger.info(f"Copied {source_path} to {replica_path}")
    elif hash_s != replica_hash:
        logger.info(f"Replace {source_path} with {replica_path}")
    shutil.copy2(source_path, replica_path)


def delete_item(source_items, replica_items, replica_folder):
    """
    Remove files from the replica folder
    that don't exist in the source folder

    Args:
        source_items (list[str]): List of items from source folder.
        replica_items (list[str]): List of items from replica folder.
        replica_folder (str): Path to the replica folder.
    """
    for item in replica_items:
        if item not in source_items:
            replica_path = os.path.join(replica_folder, item)
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
            else:
                os.remove(replica_path)
            logger.info(f"Removed {replica_path}")


def folders_sync(source_folder, replica_folder):
    """Synchronizes the source folder with the replica folder.

    Args:
        source_folder (str): Path to the source folder.
        replica_folder (str): Path to the replica folder.
    """

    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        logger.info(f"Copied {source_folder} to {replica_folder}")

    source_items = os.listdir(source_folder)

    for item in source_items:
        source_path = os.path.join(source_folder, item)
        replica_path = os.path.join(replica_folder, item)

        if os.path.isdir(source_path):
            folders_sync(source_path, replica_path)
        else:
            file_copy(source_path, replica_path)

    replica_items = os.listdir(replica_folder)
    delete_item(source_items, replica_items, replica_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_folder")
    parser.add_argument("replica_folder")
    parser.add_argument("interval", type=int)
    parser.add_argument("log_file")
    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        with open(args.log_file, 'w') as log:
            pass

    file_h = logging.FileHandler(args.log_file)
    file_h.setLevel(logging.DEBUG)

    console_h = logging.StreamHandler()
    console_h.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_h.setFormatter(formatter)
    console_h.setFormatter(formatter)
    logger.addHandler(file_h)
    logger.addHandler(console_h)

    while True:
        try:
            folders_sync(args.source_folder, args.replica_folder)
        except Exception as e:
            logger.error(f"Error: {e}")
        time.sleep(args.interval)
