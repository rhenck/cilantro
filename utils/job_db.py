import os
import datetime

from pymongo import MongoClient, DESCENDING


client = MongoClient(os.environ['JOB_DB_URL'], int(os.environ['JOB_DB_PORT']))
db = client[os.environ['JOB_DB_NAME']]


def create_index():
    """
    Create index for faster lookup in database.

    The 2 fields that are used for lookup/update are indexed.
    """
    db.jobs.create_index([("job_id", DESCENDING),
                          ("user", DESCENDING)])


def get_jobs_for_user(user):
    """
    Find all jobs of the passed user in the job database.

    :param str user: username to find jobs belonging to
    :return: list of job objects
    """
    job_list = []
    for job in db.jobs.find({"user": user}, {'_id': False}):
        job_list.append(job)
    return (job_list)


def add_job(job_id, user, job_type, task_ids):
    """
    Add a job to the job database.

    :param str job_id: Cilantro-ID of the job
    :param str user: username which started the job
    :param str job_type: type of job, i.e. 'ingest_journal'
    :param list task_ids: Cilantro-IDs of all tasks belonging to that job
    :return: None
    """
    timestamp = datetime.datetime.now()
    job = {'job_id': job_id,
           'user': user,
           'job_type': job_type,
           'task_ids': task_ids,
           'state': 'new',
           'created': timestamp,
           'updated': timestamp,
           'errors': []
           }

    db.jobs.insert_one(job)


def update_job(job_id, state, error_text=''):
    """
    Update a job to the job database with new state and updated timestamp.

    If there is text passed in 'error_text' then that is added to the list
    of error messages of that task. The error mesages are a list to  make it
    possible to keep executing the task chain even though some tasks
    throw errors. The messages are put into the job entry in the database
    and can be collected later.

    :param str job_id: Cilantro-ID of the job
    :param str state: new state of the job
    :param str error_text: (optional) text containig details about thrown error
    :return: None
    """
    timestamp = datetime.datetime.now()
    db.jobs.update_many({"job_id": job_id},
                        {'$set': {'state': state, 'updated': timestamp}})
    if error_text != '':
        db.jobs.update_many({"job_id": job_id},
                            {'$push': {'errors': error_text}})