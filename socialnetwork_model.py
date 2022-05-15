"""
Placeholder header information
"""

from pathlib import Path
import peewee as pw
from loguru import logger

# pylint: disable=R0903

file = Path('socialnetwork.db')
if Path.exists(file):
    Path.unlink(file)
    logger.info(f"The existing file, {file}, was deleted.")

db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    """
    created for inheritance in Users and Status models
    """
    logger.info("Created BaseModel for Model classes to inherit from...inherits from peewee Model")

    class Meta:
        """
        Set up for database inheritance
        """
        database = db


# Create table 1 - Users
class Users(BaseModel):
    """
    This class defines Users, which maintains details of users of a social network
    platform for which we want to store basic profile information.
    """
    logger.info("peewee model -- 'Users' created.")
    user_id = pw.CharField(primary_key=True, max_length=30,
                           constraints=[pw.Check("LENGTH(user_id) < 30")])
    first_name = pw.CharField(max_length=30, null=True)
    last_name = pw.CharField(max_length=100, null=True)
    email = pw.CharField(max_length=30, null=True)

    def show(self):
        """ Display an instance """
        print(self.user_id, self.first_name, self.last_name, self.email)


# Create table 2 - User Status
class Status(BaseModel):
    """
    This class defines Status, which maintains status details of past statuses entered by a User.
    """
    logger.info("peewee model -- 'Status' created.")
    status_id = pw.CharField(primary_key=True, max_length=30)
    user_id = pw.ForeignKeyField(Users, to_field='user_id', on_delete='CASCADE')  # lazy load?
    status_text = pw.CharField(max_length=100, null=True)


def main_social_network():
    """
    Connect to established database
    """

    db.connect()
    logger.info(f"Connected to the database: {db}")
    db.execute_sql('PRAGMA foreign_keys = ON;')
    # Creates the tables in the database ready for us to use
    logger.info("Users and Status tables being created...")
    db.create_tables([Users, Status])
    # db.create_tables([StatusCollection])
    logger.info("Users and Status tables were created.")


if __name__ == '__main__':
    main_social_network()
