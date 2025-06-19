#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Set
import uuid
import time
from datetime import datetime
import hashlib
import json

app = FastAPI(title="Git Simulator API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class CommitRequest(BaseModel):
    message: str
    content: str = ""
    session_id: str

class CheckoutRequest(BaseModel):
    branch_name: str
    session_id: str

class MergeRequest(BaseModel):
    source_branch: str
    target_branch: str
    session_id: str

class ClearRequest(BaseModel):
    session_id: str

# Core Git Simulator Classes
class GitCommit:
    def __init__(self, commit_id: str, message: str, content: str = "", parents: List[str] = None):
        self.id = commit_id
        self.message = message
        self.content = content
        self.parents = parents or []
        self.timestamp = datetime.now().isoformat()
        self.author = "Git Simulator User"
        
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "content": self.content,
            "parents": self.parents,
            "timestamp": self.timestamp,
            "author": self.author
        }

class GitBranch:
    def __init__(self, name: str, head_commit: str):
        self.name = name
        self.head_commit = head_commit
        
    def to_dict(self):
        return {
            "name": self.name,
            "head_commit": self.head_commit
        }

class GitRepository:
    def __init__(self):
        self.commits: Dict[str, GitCommit] = {}
        self.branches: Dict[str, GitBranch] = {}
        self.current_branch = "main"
        self._initialize_repo()
    
    def _initialize_repo(self):
        """Initialize repository with initial commit"""
        init_commit_id = self._generate_commit_id("Initial commit", "")
        init_commit = GitCommit(init_commit_id, "Initial commit", "")
        self.commits[init_commit_id] = init_commit
        self.branches["main"] = GitBranch("main", init_commit_id)
    
    def _generate_commit_id(self, message: str, content: str) -> str:
        """Generate a unique commit ID based on content and timestamp"""
        data = f"{message}{content}{time.time()}"
        return hashlib.sha1(data.encode()).hexdigest()[:8]
    
    def create_commit(self, message: str, content: str = "") -> str:
        """Create a new commit on the current branch"""
        current_branch_obj = self.branches[self.current_branch]
        parent_commit_id = current_branch_obj.head_commit
        
        commit_id = self._generate_commit_id(message, content)
        new_commit = GitCommit(commit_id, message, content, [parent_commit_id])
        
        self.commits[commit_id] = new_commit
        current_branch_obj.head_commit = commit_id
        
        return commit_id
    
    def create_branch(self, branch_name: str) -> bool:
        """Create a new branch from current HEAD"""
        if branch_name in self.branches:
            return False
        
        current_head = self.branches[self.current_branch].head_commit
        self.branches[branch_name] = GitBranch(branch_name, current_head)
        return True
    
    def checkout_branch(self, branch_name: str) -> bool:
        """Switch to an existing branch or create a new one"""
        if branch_name not in self.branches:
            if self.create_branch(branch_name):
                self.current_branch = branch_name
                return True
            return False
        
        self.current_branch = branch_name
        return True
    
    def merge_branches(self, source_branch: str, target_branch: str) -> Optional[str]:
        """Merge source branch into target branch"""
        if source_branch not in self.branches or target_branch not in self.branches:
            return None
        
        source_head = self.branches[source_branch].head_commit
        target_head = self.branches[target_branch].head_commit
        
        # Create merge commit
        merge_message = f"Merge {source_branch} into {target_branch}"
        merge_commit_id = self._generate_commit_id(merge_message, "")
        merge_commit = GitCommit(
            merge_commit_id, 
            merge_message, 
            "", 
            [target_head, source_head]
        )
        
        self.commits[merge_commit_id] = merge_commit
        self.branches[target_branch].head_commit = merge_commit_id
        
        # Switch to target branch
        self.current_branch = target_branch
        
        return merge_commit_id
    
    def get_commit_history(self) -> List[Dict]:
        """Get all commits with their relationships for graph visualization"""
        commits_data = []
        for commit in self.commits.values():
            commit_data = commit.to_dict()
            # Add branch information
            commit_data["branches"] = []
            for branch_name, branch in self.branches.items():
                if branch.head_commit == commit.id:
                    commit_data["branches"].append(branch_name)
            commits_data.append(commit_data)
        
        return commits_data
    
    def get_branches(self) -> List[Dict]:
        """Get all branches"""
        return [branch.to_dict() for branch in self.branches.values()]
    
    def clear_repository(self):
        """Reset repository to initial state"""
        self.commits.clear()
        self.branches.clear()
        self.current_branch = "main"
        self._initialize_repo()

# In-memory storage for multiple sessions
repositories: Dict[str, GitRepository] = {}

def get_or_create_repository(session_id: str) -> GitRepository:
    """Get existing repository or create new one for session"""
    if session_id not in repositories:
        repositories[session_id] = GitRepository()
    return repositories[session_id]

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Git Simulator API is running!"}

@app.get("/session/new")
async def create_new_session():
    """Create a new session ID"""
    session_id = str(uuid.uuid4())
    return {"session_id": session_id}

@app.post("/newcommit")
async def create_commit(request: CommitRequest):
    """Create a new commit"""
    try:
        repo = get_or_create_repository(request.session_id)
        commit_id = repo.create_commit(request.message, request.content)
        
        return {
            "success": True,
            "commit_id": commit_id,
            "message": f"Created commit: {commit_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/checkout")
async def checkout_branch(request: CheckoutRequest):
    """Create or switch to a branch"""
    try:
        repo = get_or_create_repository(request.session_id)
        success = repo.checkout_branch(request.branch_name)
        
        if success:
            return {
                "success": True,
                "current_branch": repo.current_branch,
                "message": f"Switched to branch: {request.branch_name}"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to create/checkout branch")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/merge")
async def merge_branches(request: MergeRequest):
    """Merge two branches"""
    try:
        repo = get_or_create_repository(request.session_id)
        merge_commit_id = repo.merge_branches(request.source_branch, request.target_branch)
        
        if merge_commit_id:
            return {
                "success": True,
                "merge_commit_id": merge_commit_id,
                "current_branch": repo.current_branch,
                "message": f"Merged {request.source_branch} into {request.target_branch}"
            }
        else:
            raise HTTPException(status_code=400, detail="Merge failed - branches not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/log/{session_id}")
async def get_commit_log(session_id: str):
    """Get commit history and branches for visualization"""
    try:
        repo = get_or_create_repository(session_id)
        commits = repo.get_commit_history()
        branches = repo.get_branches()
        
        return {
            "success": True,
            "commits": commits,
            "branches": branches,
            "current_branch": repo.current_branch
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/clear")
async def clear_repository(request: ClearRequest):
    """Clear/reset repository state"""
    try:
        repo = get_or_create_repository(request.session_id)
        repo.clear_repository()
        
        return {
            "success": True,
            "message": "Repository cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status/{session_id}")
async def get_status(session_id: str):
    """Get current repository status"""
    try:
        repo = get_or_create_repository(session_id)
        
        return {
            "success": True,
            "current_branch": repo.current_branch,
            "total_commits": len(repo.commits),
            "total_branches": len(repo.branches),
            "branches": list(repo.branches.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)