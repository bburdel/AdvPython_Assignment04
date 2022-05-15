"""
Classes to manage the user status messages
"""

# pylint: disable=R0903
# pylint: disable=R1710
# pylint: disable=W0703

import peewee as pw
from loguru import logger
import socialnetwork_model as snm

logger.info("Logging activity from user_status.py...")
logger.add("out_users_status.log", backtrace=True, diagnose=True)


class UserStatusCollection:
    """
    Collection of UserStatusCollection messages
    """

    @staticmethod
    def add_status(status_id, user_id, status_text):
        """
        add a new status message to the collection
        """
        try:
            # if status_id.not_in.snm.Status.status_id:
            new_status = snm.Status.create(status_id=status_id, user_id=user_id,
                                           status_text=status_text)
            new_status.save()
            logger.info(f"New User Status, {status_id}, added to database.")
            return True
        except pw.IntegrityError:
            print("This user status already exists and cannot be added to the database.")
            logger.info(f"Status ID -- {status_id} -- already exists, "
                        f"cannot add status with this ID.")
            return False

    @staticmethod
    def modify_status(status_id, user_id, status_text):
        """
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        """
        try:
            row = snm.Status.get(snm.Status.status_id == status_id)
            search_user = snm.Users.get(snm.Users.user_id == user_id)
            if search_user == row.user_id:
                row.status_text = status_text
                row.save()
                logger.info(f"Status ID, {status_id}, found. User status modified.")
                return True
            # else:
            #     print(f"This user ID, {user_id}, does not match "
            #           f"the known user ID for this status: {row.user_id}")
        except pw.DoesNotExist:
            logger.info(f"Status ID -- {status_id} -- not found. Could not modify status")
            return False
        except pw.IntegrityError:
            logger.info("The user ID you entered is not associated with this status ID.")
        except TypeError as type_err:
            print(type_err)

    @staticmethod
    def delete_status(status_id):
        """
        deletes the status message with id, status_id
        """
        try:
            del_status = snm.Status.get(snm.Status.status_id == status_id)
            del_status.delete_instance()
            logger.info(f"Status ID, {status_id}, found. Status deleted.")
            return True
        except pw.DoesNotExist:
            logger.info(f"Status ID, {status_id}, not found. Could not delete status.")
            return False

    @staticmethod
    def search_status(status_id):
        """
        Find and return a status message by its status_id

        Returns an empty UserStatusCollection object if status_id does not exist
        """
        try:
            logger.info(f"Searched database for {status_id}.")
            status_search = snm.Status.get(snm.Status.status_id == status_id)
            return status_search
        except AttributeError as att_err:
            logger.info(att_err)
        except pw.DoesNotExist as dne:
            # print("Status ID does not exist.")
            logger.info(dne)
        except Exception as generic_exception:
            # print("Status ID does not exist.")
            logger.info(f"The following error message was triggered: {generic_exception}")

    @staticmethod
    def search_all_status_updates(user_id):
        """
        Takes a user ID and returns all status updates for that user
        :param user_id:
        :return:
        """
        try:
            # get all statuses into a list
            query_user = snm.Users.get(snm.Users.user_id == user_id)
            logger.info(query_user)
            query = snm.Status.select().where(snm.Status.user_id == query_user)
            status_list = [status.status_text for status in query]
            logger.info(f"Status list: {status_list}")
            return status_list
        except pw.DoesNotExist:
            print(f"This user ID: {user_id} does not exist.")
        except Exception as generic_error:
            logger.info(f"{Exception} occurred: {generic_error}")

    @staticmethod
    def filter_status_by_string(string_to_search):
        """
        Queries entire database for any status updates matching the string parameter
        :param string_to_search:
        :return:
        """
        try:
            query_string = \
                snm.Status.select() \
                .where(snm.Status.status_text.contains(string_to_search)).iterator()
            logger.info(query_string)
            return query_string
        except pw.DoesNotExist:
            logger.info("The pw.DoesNotExist exception was triggered.")
        except Exception as generic_error:
            logger.info(f"{Exception} occurred: {generic_error}")
