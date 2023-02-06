from prefect.deployments import Deployment
from etl_web_to_git import etl_web_to_git
from prefect.filesystems import GitHub

github_block = GitHub.load("homework2")

github_dep = Deployment.build_from_flow(
    flow=etl_web_to_git,
    name="git-flow",
    storage=github_block
)

if __name__ == "__main__":
    github_dep.apply()
