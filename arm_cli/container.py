import click
import docker
import inquirer
import subprocess

@click.group()
def container():
    """Manage Docker containers"""
    pass

@container.command('list')
def list_containers():
    """List all Docker containers"""
    client = docker.from_env()

    # Get only running containers
    containers = client.containers.list(filters={"status": "running"})
    
    if containers:
        for container in containers:
            print(f"{container.id[:12]}: {container.name}")
    else:
        print("No running containers found.")

@container.command('attach')
def attach_container():
    """Interactively select a running Docker container and attach to it"""
    client = docker.from_env()
    containers = client.containers.list(filters={"status": "running"})
    
    if not containers:
        print("No running containers found.")
        return
    
    container_choices = [
        inquirer.List('container',
                      message="Select a container to attach to",
                      choices=[f"{container.name} ({container.id[:12]})" for container in containers],
                      carousel=True)
    ]
    
    answers = inquirer.prompt(container_choices)
    selected_container_name = answers['container'].split(" ")[0]  # Extract container name

    print(f"Attaching to {selected_container_name}...")
    
    try:
        subprocess.run([
            "docker", "exec", "-it",
            selected_container_name, "/bin/bash"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error attaching to container: {e}")
    except KeyboardInterrupt:
        print("\nExiting interactive session...")
