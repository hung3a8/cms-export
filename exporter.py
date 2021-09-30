import json
import shutil
from shutil import copy
import os

WORKDIR = "dataset"
OUTPUT = "contest"
DIGEST = os.path.join(WORKDIR, "files")

shutil.rmtree(OUTPUT) # Clear old output

os.makedirs(OUTPUT)

contest = json.load(open(os.path.join(WORKDIR, "contest.json")))

base_info = contest["0"]
CONTEST_NAME = base_info['name']

task_id = base_info['tasks']  # id of task in db

def get_file_from_digest(idx, parrent_dir):
    attachment_data = contest[idx]
    name = attachment_data['filename']
    digest = attachment_data['digest']
    copy(os.path.join(DIGEST, digest), os.path.join(parrent_dir, name))

def get_testcase_from_digest(idx, parrent_dir):
    testcase = contest[idx]
    codename = testcase['codename']
    fin = testcase['input']
    fout = testcase['output']
    inp_name = (codename + ".inp").replace('/', '_')
    out_name = (codename + ".out").replace('/', '_')

    copy(os.path.join(DIGEST, fin), os.path.join(parrent_dir, inp_name))
    copy(os.path.join(DIGEST, fout), os.path.join(parrent_dir, out_name))

def get_submission_from_digest(idx, parrent_dir):
    submission = contest[idx]
    for x in contest[idx]["files"]:
        file_idx = contest[idx]["files"][x]
        digest = contest[file_idx]['digest']
    copy(os.path.join(DIGEST, digest), os.path.join(parrent_dir, idx))


for idx in task_id:
    task = contest[idx]
    problem_name = task['name']
    dataset_id = task['active_dataset']
    attachment = contest[idx]['attachments']
    submissions = contest[idx]['submissions']
    task_dir = os.path.join(OUTPUT, 'task', problem_name)

    os.makedirs(task_dir)

    dataset = contest[dataset_id]

    # Get attachment
    for item in attachment:
        get_file_from_digest(attachment[item], task_dir)

    # Get manager (checker, etc.)
    for item in dataset['managers']:
        get_file_from_digest(dataset['managers'][item], task_dir)

    # Get testcases
    testcases = dataset['testcases']
    testcase_dir = os.path.join(task_dir, 'testcase')
    os.makedirs(testcase_dir)
    for item in testcases:
        get_testcase_from_digest(testcases[item], testcase_dir)

    # Get submissions
    submission_dir = os.path.join(task_dir, 'submission')
    os.makedirs(submission_dir)
    for sub in submissions:
        get_submission_from_digest(sub, submission_dir)

    print("Get problem %s" % problem_name)
