"""
Provides a basic frontend
"""

import sys
from loguru import logger
import main
import socialnetwork_model as snm

logger.info("Let's get to logging and debugging!")
logger.add("out.log", backtrace=True, diagnose=True)


def load_users():
    """
    Loads user accounts from a file
    """
    filename = input('Enter filename of user file: ')
    main.load_users(filename, database=snm.db)


def load_status_updates():
    """
    Loads status updates from a file
    """
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, database=snm.db)


def add_user():
    """
    Adds a new user into the database
    """
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')
    if not main.add_user(user_id,
                         user_name,
                         user_last_name,
                         email):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    """
    Updates information for an existing user
    """
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')

    if not main.update_user(user_id, user_name, user_last_name, email):
        print(f"An error occurred while trying to update user with user ID: {user_id}")
    else:
        print(f"User ID, {user_id}, was successfully updated")


def search_user():
    """
    Searches a user in the database
    """
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id)

    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Name: {result.first_name}")
        print(f"Last name: {result.last_name}")
        print(f"Email: {result.email}")


def delete_user():
    """
    Deletes user from the database
    """
    user_id = input('User ID: ')
    if not main.delete_user(user_id):
        print(f"An error occurred while trying to delete user record for user_id: {user_id}")
    else:
        print(f"User record for -- {user_id} -- was successfully deleted")


def add_status():
    """
    Adds a new status into the database
    """
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(status_id, user_id, status_text):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    """
    Updates information for an existing status
    """
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    """
    Searches a status in the database
    """
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id)
    # try:
    # if not result.status_id:
    #     print("ERROR: Status does not exist")
    if result is None:
        print("ERROR: Status does not exist.")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")
    # except AttributeError as e:
    #     logger.info(e)
    #     print(e)


def search_all_status_updates():
    """
    Searches for all a user's status updates through the user's ID
    :return:
    """
    user_id = input('Enter user ID to search: ')
    results = main.search_all_status_updates(user_id)
    count_statuses = len(results)
    generator = status_generator(results)
    try:
        print(f"{count_statuses} status update(s) was/were found for {user_id}.")
        while True:
            report_option = input("Would you like to see the next status? (Y/N): ")
            if report_option.upper().strip() == 'Y':
                # print(status_generator(results).__next__())
                print(generator.__next__())
            if report_option.upper().strip() == 'N':
                print("That was a fun walk down memory lane.")
                break
    except StopIteration as query_end:
        logger.info(f"Reached {query_end}.")
        print(f"INFO: End of query results. "
              f"You have reached the last status for {user_id}.")


def status_generator(status_list):
    """
    Custom generator function
    :return:
    """
    status_count = len(status_list)
    index = 0
    while index < status_count:
        yield status_list[index]
        index += 1


# @pysnooper.snoop(depth=3)
def filter_status_by_string():
    """

    :return:
    """
    string_to_search = input('Enter the string to search for: ')
    results = main.filter_status_by_string(string_to_search)
    # count_results = len(list(results))
    # count_results = sum(1 for _ in results)
    try:
        while True:
            # print(f"{count_results} statuses contain that string.")
            next_result = next(results)
            # print(f"You are currently viewing the status: "
            #       f"{next_result.status_text}")
            report_option = input("Review the status? (Y/N): ")
            if report_option.upper().strip() == 'Y':
                # next_result = next(results)
                print(f"Status: {next_result.status_text}")
                delete_choice = input("Delete this status? (Y/N): ")
                if delete_choice.upper().strip() == 'Y':
                    next_result.delete_instance()
                    print(f"Status: {next_result.status_text} -- deleted.")
                    logger.info("Status deleted.")
                if delete_choice.upper().strip() == 'N':
                    print("The status will not be deleted.")
                    continue
            if report_option.upper().strip() == 'N':
                print("It was fun while it lasted.")
                break
    except StopIteration as query_end:
        logger.info(f"Reached {query_end}.")
        print(f"INFO: End of query results. "
              f"You have reached the last status containing {string_to_search}.")


def flagged_status_updates():
    """
    Asks user for string to search, filters the statuses by string, use list comprehension
    :return:
    """
    string_to_search = input('Enter the string to search for: ')
    results = main.filter_status_by_string(string_to_search)
    all_results = [(row.status_id, row.status_text) for row in results]
    for tup in all_results:
        print(tup)
    return all_results


def delete_status():
    """
    Deletes status from the database
    """
    status_id = input('Status ID: ')
    if not main.delete_status(status_id):
        print(f"An error occurred while trying to delete status with ID: {status_id}")
    else:
        print("Status was successfully deleted")


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == '__main__':
    snm.main_social_network()
    logger.info("Made it to the menu options printed to user.")
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': add_status,
        'H': update_status,
        'I': search_status,
        'J': search_all_status_updates,
        'K': delete_status,
        'L': filter_status_by_string,
        'M': flagged_status_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Add status
                            H: Update status
                            I: Search status
                            J: Search All statuses
                            K: Delete status
                            L: Search all status updates matching a string
                            M: Show all flagged status updates
                            Q: Quit
                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
