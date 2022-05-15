"""
Classes for user information for the social network project
"""
# pylint: disable=R0903
import pysnooper
from loguru import logger
import peewee as pw
import socialnetwork_model as snm


logger.info("Logging activity from users.py...")
logger.add("out_users_status.log")


class UserCollection:
    """
    Placeholder text
    Something about functions that manipulate data in a SQL database
    """

    @staticmethod
    @pysnooper.snoop()
    def add_user(user_id, user_name, user_last_name, email):
        """
        Adds a new user to the collection
        """
        try:
            new_user = snm.Users.create(user_id=user_id, first_name=user_name,
                                        last_name=user_last_name, email=email)
            new_user.save()
            logger.info(f"New User, {user_id}, added to SQL database table = {snm.Users}.")
            return True
        except pw.IntegrityError:
            print("This user already exists and cannot be added to the database.")
            logger.info(f"New User, {user_id}, could not be added.")
            return False

    @staticmethod
    def modify_user(user_id, user_name, user_last_name, email):
        """
        Modifies an existing user ID's details
        """
        try:
            # if not snm.Users.get(snm.Users.user_id == user_id):
            #
            #     return False
            # need to retrieve user from table to modify it -- use .get method
            row = snm.Users.get(snm.Users.user_id == user_id)
            # updates the values of the corresponding fields
            row.first_name = user_name
            row.last_name = user_last_name
            row.email = email
            row.save()
            logger.info(f"User {user_id} successfully modified with the following values:"
                        f"{user_name}, {user_last_name}, {email}.")
            return True
        except pw.DoesNotExist:
            logger.info(f"User ID -- {user_id} -- not found, "
                        f"could not retrieve user for modification.")
            print("This user does not exist in the User table.")
            return False
        except Exception as generic_exception:
            logger.info(generic_exception)
            print(f"The following error occurred: {generic_exception}")

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user
        """
        row = snm.Users.select().where(user_id.in_snm.Users.user_id)
        if not row.user_name:
        # if not snm.Users.get(snm.Users.user_id == user_id):
        # if user_id not in snm.Users.user_id:
            logger.info(f"User ID not found, cannot delete {user_id}.")
            return False
        del_user = snm.Users.get(snm.Users.user_id == user_id)
        del_user.delete_instance()
        logger.info(f"User ID, {user_id}, found. User deleted from database.")
        return True

    @staticmethod
    @pysnooper.snoop()
    def search_user(user_id):
        """
        Searches for user data
        """
        # search contents of table column user_id, return None if it is not found
        try:
            # finder = snm.Users.select().where(snm.Users.user_id == user_id).get()
            snm.Users.get(snm.Users.user_id == user_id)
            # if not finder:
            #     print("If we can make it here, we'll make it anywhere...")
            #     logger.info(f"{user_id}, not found when searching database for this user ID.")
            #     return snm.Users.user_id
            # if snm.Users.get(snm.Users.user_id == user_id) not in snm.Users.user_id:
            logger.info(f"Searched database and found, {user_id}.")
            user_search = snm.Users.get(snm.Users.user_id == user_id)
            return user_search
        except AttributeError as att_err:
            logger.info(att_err)
        except Exception as generic_exception:
            print("User ID does not exist.")
            logger.info(generic_exception)
