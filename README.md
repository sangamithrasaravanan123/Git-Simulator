# Git Simulator - Python 

##  Overview
This is a Python-based conversion of the original C++ Git Simulator. It provides an interactive web interface to visualize Git operations like commits, branching, and merging through a beautiful graphical interface.

##  Technology Stack
- **Backend**: Python with FastAPI
- **Frontend**: React with Cytoscape.js for graph visualization
- **API Communication**: Axios for HTTP requests
- **Visualization**: Cytoscape.js for interactive commit graphs

##  Prerequisites
- Python 3.8 or higher
- Node.js and npm (optional, for frontend development)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation Steps

### Step 1: Clone or Download the Project
```bash
# Create a new directory for the project
mkdir git-simulator-python
cd git-simulator-python
```

### Step 2: Set Up Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
# Install required packages
pip install fastapi uvicorn python-multipart
```

### Step 4: Create Project Structure
```
git-simulator-python/
├── backend/
│   ├── main.py          # Backend API server
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Frontend application
└── README.md           # This file
```

### Step 5: Save the Backend Code
1. Create a `backend` folder
2. Save the Python backend code as `backend/main.py`
3. Create `backend/requirements.txt` with the following content:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
```

### Step 6: Save the Frontend Code
1. Create a `frontend` folder
2. Save the HTML frontend code as `frontend/index.html`

##  Running the Application

### Step 1: Start the Backend Server
```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py  (or)
uvicorn main:app --reload  
```

The backend server will start on `http://localhost:8000`

### Step 2: Open the Frontend
1. Navigate to the `frontend` directory
2. Open `index.html` in your web browser
3. Or serve it using a simple HTTP server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000

# Then open http://localhost:3000 in your browser
```

## How to Use

### 1. **Creating Commits**
- Enter a commit message in the "Create Commit" section
- Optionally add file content
- Click "Create Commit" to add a new commit to the current branch

### 2. **Branch Operations**
- Enter a branch name in the "Branch Operations" section
- Click "Create/Checkout Branch" to create a new branch or switch to an existing one
- The current branch is displayed in the status section

### 3. **Merging Branches**
- Select a source branch and target branch from the dropdowns
- Click "Merge Branches" to create a merge commit
- The merge will combine the histories of both branches

### 4. **Visualization**
- The commit graph is automatically updated after each operation
- **Blue nodes**: Regular commits
- **Orange nodes**: Branch head commits
- **Green nodes**: Merge commits
- Click on any commit node to see its details

### 5. **Repository Management**
- Use "Clear Repository" to reset everything to the initial state
- The status panel shows current branch and commit/branch counts

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

- `GET /session/new` - Create a new session ID
- `POST /newcommit` - Create a new commit
- `POST /checkout` - Create or switch to a branch
- `POST /merge` - Merge two branches
- `GET /log/{session_id}` - Get commit history and branches
- `GET /status/{session_id}` - Get repository status
- `POST /clear` - Clear repository state

## Troubleshooting

### Backend Issues
1. **Port 8000 already in use**:
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   # Or change the port in main.py
   ```

2. **Import errors**:
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

### Frontend Issues
1. **CORS errors**: Make sure the backend is running on localhost:8000
2. **Graph not displaying**: Check browser console for JavaScript errors
3. **API connection failed**: Verify backend server is running and accessible


### Features:
-  Session-based isolation (multiple users can use simultaneously)
-  Interactive commit graph visualization
-  Real-time updates
-  Branch creation and switching
-  Merge operations with proper commit parents
-  Repository status tracking
-  Responsive design for different screen sizes

##  Advanced Usage

### Development Mode
```bash
# Run backend with auto-reload for development
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment
```bash
# Install gunicorn for production
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Custom Configuration
You can modify the following in `main.py`:
- Change default port (line with `uvicorn.run`)
- Modify CORS settings for specific domains
- Add authentication if needed
- Extend with additional Git operations

##  Next Steps

1. **Try the Basic Operations**:
   - Create a few commits
   - Make a new branch
   - Switch between branches
   - Perform a merge

2. **Experiment with Complex Workflows**:
   - Create multiple branches
   - Make commits on different branches
   - Merge branches in different orders

3. **Extend the Functionality**:
   - Add rebase operations
   - Implement tag creation
   - Add commit diff visualization
   - Include file tree representation

