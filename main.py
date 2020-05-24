from typing import List
import os
from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
import requests

app = FastAPI()



class User(BaseModel):
    name: str = None
    username: str = None
    avatar_url: str = None
    email: str = None
class Project(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    web_url: str = None
    avatar_url: str = None
    git_ssh_url: str = None
    git_http_url: str = None
    namespace: str = None
    visibility_level: int = None
    path_with_namespace: str = None
    default_branch: str = None
    ci_config_path: str = None
    homepage: str = None
    url: str = None
    ssh_url: str = None
    http_url: str = None

class TotalTimeSpent(BaseModel):
    previous: int = None
    current: int = None

class Person(BaseModel):
    name: str = None
    username: str = None
    avatar_url: str = None
    email: str = None
class Assignees(BaseModel):
    previous: List[Person] = []
    current: List[Person] = []

class MergeParams(BaseModel):
    force_remove_source_branch: str = None

class Repo(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    web_url: str = None
    avatar_url: str = None
    git_ssh_url: str = None
    git_http_url: str = None
    namespace: str = None
    visibility_level: int = None
    path_with_namespace: str = None
    default_branch: str = None
    ci_config_path: str = None
    homepage: str = None
    url: str = None
    ssh_url: str = None
    http_url: str = None


class Author(BaseModel):
    name: str = None
    email: str = None

class Repository(BaseModel):
    name: str = None
    url: str = None
    description: str = None
    homepage: str = None
class Changes(BaseModel):
    assignees: Assignees = None
    total_time_spent: TotalTimeSpent = None
class LastCommit(BaseModel):
    id: str = None
    message: str = None
    timestamp: str = None
    url: str = None
    author: Author = None
class ObjectAttributes(BaseModel):
    assignee_id: int = None
    author_id: int = None
    created_at: str = None
    description: str = None
    head_pipeline_id: int = None
    id: int = None
    iid: int = None
    last_edited_at: str = None
    last_edited_by_id: str = None
    merge_commit_sha: str = None
    merge_error: str = None
    merge_params: MergeParams = None
    merge_status: str = None
    merge_user_id: int = None
    merge_when_pipeline_succeeds: bool = False
    milestone_id: int = None
    source_branch: str = None
    source_project_id: int = None
    state_id: int  = None
    target_branch: str = None
    target_project_id: int  = None
    time_estimate: int = None
    title: str = None
    updated_at: str = None
    updated_by_id: int = None
    url: str = None
    source: Repo = None
    target: Repo = None
    last_commit: LastCommit = None
    work_in_progress: bool = None
    total_time_spent: int = None
    human_total_time_spent: int = None
    human_time_estimate: int = None
    assignee_ids: List[int] = []
    state: str = None
    action: str = None
    oldrev: str = None
class Project(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    web_url: str = None
    avatar_url: str = None
    git_ssh_url: str = None
    git_http_url: str = None
    namespace: str = None
    visibility_level: int = None
    path_with_namespace: str = None
    default_branch: str = None
    ci_config_path: str = None
    homepage: str = None
    url: str = None
    ssh_url: str = None
    http_url: str = None
class GitlabWebhook(BaseModel):
    object_kind: str = None
    event_type: str = None
    user: User = None
    project: Project = None
    object_attributes: ObjectAttributes = None
    lables: List[str] = []
    changes: Changes = None
    repository: Repository = None
    assignees: List[Person] = []


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/")
async def post_root(body: GitlabWebhook):
    project_id = 6484
    component_name_to_delete = 'canary-' + body.project.name + '-' + body.object_attributes.source_branch + '-9-6'
    mr_action = body.object_attributes.action
    print(body.object_attributes.action)
    if mr_action != "closed" or mr_action != "merged":
        payload = {'ref': 'delete-pods', 'variables[][key]': 'COMPONENT_TO_DELETE','variables[][value]' : component_name_to_delete }
        headers = {'PRIVATE-TOKEN': os.environ['AB_PRIVATE_TOKEN']}
        url = str(os.environ['AB_GITLAB_URL']) +'projects/' + str(project_id) + '/pipeline'
        r = requests.post(url, headers=headers, params=payload)
    return {"Hello": "World post"}
