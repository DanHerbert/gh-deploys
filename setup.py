from setuptools import setup

setup(
    name="gh-deploys",
    version="0.0.1",
    description="Deployments based on Github Repo changes.",
    author="Dan Herbert",
    author_email="gh-deploy-dan@hrbrt.co",
    license="Apache 2.0",
    packages=["gh_deploys"],
    install_requires=["github-webhook", "pyyaml", "gunicorn",],
)
