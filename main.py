"""
main driver for a simple social network project
"""

# pylint: disable=W1514
# pylint: disable=W0703

import csv
import peewee as pw
from loguru import logger

import socialnetwork_model as snm
import users as u
import user_status as us


def load_users(filename, database):
    """
    Loads users from file into an existing SQL database
    """

    try:
        with open(filename, newline='') as csv_file:
            file_contents = csv.DictReader(csv_file)
            for dict_row in file_contents:
                try:
                    with database.transaction():  # transaction promotes safety
                        user_record = snm.Users.create(
                            user_id=dict_row['USER_ID'],
                            first_name=dict_row['NAME'],
                            last_name=dict_row['LASTNAME'],
                            email=dict_row['EMAIL'])
                        user_record.save()

                except Exception as generic_error:
                    logger.info(f"Error creating user record for user ID = {dict_row['USER_ID']}")
                    logger.info(generic_error)

    except FileNotFoundError:
        print(f"File named, \'{filename}\' does not exist.")


def load_status_updates(filename, database):
    """
    Loads users' status data from file into an existing SQL database
    """
    try:
        with open(filename, newline='') as csv_file:
            file_contents = csv.DictReader(csv_file)
            for dict_row in file_contents:
                try:
                    with database.transaction():
                        status_record = snm.Status.create(
                            status_id=dict_row['STATUS_ID'],
                            user_id=dict_row['USER_ID'],
                            status_text=dict_row['STATUS_TEXT']
                        )
                        status_record.save()
                except pw.IntegrityError:
                    logger.info("FOREIGN KEY constraint failed.")
                    # logger.info(f"Error creating status record for status ID = "
                    #             f"{dict_row['STATUS_ID']}, user ID = {dict_row['USER_ID']}")
                except Exception as generic_exception:
                    logger.exception("Exception!")
                    logger.info(generic_exception)

    except FileNotFoundError:
        print(f"File named, \'{filename}\' does not exist.")


def add_user(user_id, user_name, user_last_name, email):
    """
    Creates a new user database entry
    """

    new_user = u.UserCollection.add_user(user_id, user_name, user_last_name, email)
    return new_user


def update_user(user_id, user_name, user_last_name, email):
    """
    Updates the record of a user in a database

    Placeholder for return types and params
    """

    mod_user = u.UserCollection.modify_user(user_id, user_name, user_last_name, email)
    return mod_user


def delete_user(user_id):
    """
    Deletes a user from a database
    """

    purge_user = u.UserCollection.delete_user(user_id)
    return purge_user


def search_user(user_id):
    """
    Searches for a user in a database

    Requirements:
    - If the user is found, returns the corresponding User record.
    - Otherwise, it returns None.
    """

    find_user = u.UserCollection.search_user(user_id)
    return find_user


def add_status(status_id, user_id, status_text):
    """
    Creates a new status entry for a user

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors
    - Otherwise, it returns True.
    """

    another_status = us.UserStatusCollection.add_status(status_id, user_id, status_text)
    return another_status


def update_status(status_id, user_id, status_text):
    """
    Updates the values of an existing status_id in a database table

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """

    modify_status = us.UserStatusCollection.modify_status(status_id, user_id, status_text)
    return modify_status


def delete_status(status_id):
    """
    Deletes a status_id from a database

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """

    purge_status = us.UserStatusCollection.delete_status(status_id)
    return purge_status


def search_status(status_id):
    """
    Searches for a status in a database

    Requirements:
    - If the status is found, returns the corresponding
    Status instance.
    - Otherwise, it returns None.
    """

    find_status = us.UserStatusCollection.search_status(status_id)
    return find_status


def search_all_status_updates(user_id):
    """

    :param user_id:
    :return:
    """
    search_all = us.UserStatusCollection.search_all_status_updates(user_id)
    return search_all


def filter_status_by_string(string_to_search_for):
    """

    :param string_to_search_for:
    :return:
    """
    filter_statuses = us.UserStatusCollection.filter_status_by_string(string_to_search_for)
    return filter_statuses
