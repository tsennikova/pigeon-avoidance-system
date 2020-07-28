#!/usr/bin/python3
import os, shutil, time
import syslog
import config

def logger(message):
    """
    Write status into a log file located in /var/log/messages
    :param message: Message to write into the log file. format: str
    :return:
    """
    syslog.syslog(message)
    print(message)
    return


def clean_trash():
    """
    Removes files in the trash folder specified in the config.py
    :return:
    """
    path = config.trash_path
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger('WARNING: Failed to delete. ' + file_path + 'Reason: ' + str(e))
    logger("INFO: Removed trash files")
    return


def remove_old_files(days=config.max_file_age):
    """
    Removes files that are older then max_file_age specified in the config.py
    :param days: max number of days to store an image in the image_path folder.
    :return:
    """
    path = config.image_path
    now = time.time()
    counter = 0
    try:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.stat(file_path).st_mtime < now - days * 86400:

                if os.path.isfile(file_path):
                    counter +=1
                    os.remove(os.path.join(path, file_path))
        logger("INFO: Removed " + str(counter) + " old files")
    except Exception as e:
        logger('WARNING: Failed to delete. ' + file_path + 'Reason: ' + str(e))
    return

if __name__ == "__main__":
    remove_old_files()
    clean_trash()
