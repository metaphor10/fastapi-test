from typing import List
import os
from fastapi import FastAPI, Header
from pydantic import BaseModel
import requests

app = FastAPI()



class User(BaseModel):
    name: str
    username: str
    avatar_url: str
    email: str
class Project(BaseModel):
    id: int
    name: str
    description: str
    web_url: str
    avatar_url: str = None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str = None
    homepage: str
    url: str
    ssh_url: str
    http_url: str

class TotalTimeSpent(BaseModel):
    previous: int = None
    current: int = None

class Person(BaseModel):
    name: str
    username: str
    avatar_url: str
    email: str
class Assignees(BaseModel):
    previous: List[Person] = []
    current: List[Person] = []

class MergeParams(BaseModel):
    force_remove_source_branch: str

class Repo(BaseModel):
    id: int
    name: str
    description: str
    web_url: str
    avatar_url: str = None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str = None
    homepage: str
    url: str
    ssh_url: str
    http_url: str


class Author(BaseModel):
    name: str
    email: str

class Repository(BaseModel):
    name: str
    url: str
    description: str
    homepage: str
class Changes(BaseModel):
    assignees: Assignees
    total_time_spent: TotalTimeSpent
class LastCommit(BaseModel):
    id: str
    message: str
    timestamp: str
    url: str
    author: Author
class ObjectAttributes(BaseModel):
    assignee_id: int
    author_id: int
    created_at: str
    description: str
    head_pipeline_id: int
    id: int
    iid: int
    last_edited_at: str = None
    last_edited_by_id: str = None
    merge_commit_sha: str
    merge_error: str = None
    merge_params: MergeParams
    merge_status: str
    merge_user_id: int = None
    merge_when_pipeline_succeeds: bool = False
    milestone_id: int = None
    source_branch: str
    source_project_id: int = None
    state_id: int 
    target_branch: str
    target_project_id: int 
    time_estimate: int
    title: str
    updated_at: str
    updated_by_id: int = None
    url: str
    source: Repo
    target: Repo
    last_commit: LastCommit
    work_in_progress: bool
    total_time_spent: int
    human_total_time_spent: int = None
    human_time_estimate: int = None
    assignee_ids: List[int] = []
    state: str
class Project(BaseModel):
    id: int
    name: str
    description: str
    web_url: str
    avatar_url: str = None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str = None
    homepage: str
    url: str
    ssh_url: str
    http_url: str
class GitlabWebhook(BaseModel):
    object_kind: str
    event_type: str
    user: User
    project: Project
    object_attributes: ObjectAttributes
    lables: List[str] = []
    changes: Changes
    repository: Repository
    assignees: List[Person] = []


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/")
async def post_root(body: GitlabWebhook):
    print(body.object_attributes.merge_status)
    headers = {'PRIVATE-TOKEN': os.environ['AB_PRIVATE_TOKEN']}
    url = str(os.environ['AB_GITLAB_URL']) +'projects/' +str(body.object_attributes.target_project_id)
    print(headers)
    print(url)
    # r = requests.get(url, headers=headers)
    return {"Hello": "World post"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
