import os
import requests
from dotenv import load_dotenv
from git import Repo

class GitHubPusher:
    def __init__(self, project_path=None):
        load_dotenv()
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise Exception("❌ GITHUB_TOKEN not found in .env")

        # Use parent folder of current script if not provided
        if not project_path:
            project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        self.project_path = os.path.abspath(project_path)
        self.repo_name = os.path.basename(self.project_path).lower()
        self.username = "oagengmotlapele"
        self.base_url = "https://api.github.com"

        if not os.path.isdir(self.project_path):
            raise Exception(f"❌ Invalid path: {self.project_path}")

        if not self.has_internet():
            raise Exception("❌ No internet connection. Aborting!")

        self.push_to_github()

    def has_internet(self, url="https://api.github.com"):
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def push_to_github(self):
        if self.repo_exists():
            print(f"⚠️ Repo '{self.repo_name}' already exists. Proceeding to push...")
        elif not self.create_github_repo():
            return
        self.git_init_and_push()

    def repo_exists(self):
        url = f"{self.base_url}/repos/{self.username}/{self.repo_name}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    def create_github_repo(self):
        print(f"🔧 Creating GitHub repo '{self.repo_name}'...")
        headers = {"Authorization": f"token {self.token}"}
        data = {"name": self.repo_name, "private": False}
        response = requests.post(f"{self.base_url}/user/repos", headers=headers, json=data)

        if response.status_code == 201:
            print("✅ GitHub repository created.")
            return True
        else:
            print(f"❌ Failed to create repository: {response.status_code} {response.text}")
            return False

    def git_init_and_push(self):
        try:
            print("📦 Initializing local Git repository...")
            repo = Repo.init(self.project_path)

            # Ignore unwanted files/folders
            ignore_dirs = {'.idea', '__pycache__', '.venv'}
            ignore_files = {'.env'}

            for root, dirs, files in os.walk(self.project_path):
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                for file in files:
                    if file in ignore_files or file.endswith(".pyc") or file.endswith(".env"):
                        continue
                    repo.git.add(os.path.join(root, file))

            repo.index.commit("Initial commit")

            remote_url = f"https://{self.username}:{self.token}@github.com/{self.username}/{self.repo_name}.git"
            if 'origin' not in [remote.name for remote in repo.remotes]:
                repo.create_remote("origin", remote_url)
            else:
                repo.delete_remote("origin")
                repo.create_remote("origin", remote_url)

            print("🚀 Pushing to GitHub...")
            repo.remotes.origin.push(refspec="master:master")
            print("✅ Successfully pushed project to GitHub.")
        except Exception as e:
            print(f"❌ Git error: {e}")


# ====== Example Usage ======
if __name__ == "__main__":
    GitHubPusher()  # Uses parent folder of current working directory
