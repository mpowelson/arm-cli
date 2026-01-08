from typing import Optional

import click
import inquirer
from arm_robotics_sdk import application, project


@click.group()
def connection():
    """Manage connections between stacks in the active application"""
    pass


@connection.command("add")
@click.argument("source", required=False)
@click.argument("target", required=False)
@click.pass_context
def add(ctx, source: Optional[str] = None, target: Optional[str] = None):
    """Add a connection between two capability nodes

    Format: <instance_id>:<capability_name>:<handle>
    Example: inst-123:camera:image_publisher

    If no arguments provided, shows interactive selection.
    """
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load application state
        state = application.load(active_path)

        if not state.instances:
            print("No stacks in application. Add stacks first with 'arm app stack add'")
            return

        # Interactive mode if no arguments
        if source is None or target is None:
            # Build list of available capability nodes
            capability_nodes = []
            for node_id in state.graph.nodes():
                if ":" in node_id:  # Capability nodes have format instance_id:capability_name
                    node_data = state.graph.nodes[node_id]
                    capability_nodes.append(
                        (f"{node_id} ({node_data.get('type', 'capability')})", node_id)
                    )

            if not capability_nodes:
                print("No capability nodes found in application")
                return

            # Select source
            if source is None:
                questions = [
                    inquirer.List(
                        "source",
                        message="Select source node",
                        choices=capability_nodes,
                        carousel=True,
                    )
                ]
                answers = inquirer.prompt(questions)
                if not answers:
                    print("Cancelled")
                    return
                source = answers["source"]

            # Select target
            if target is None:
                questions = [
                    inquirer.List(
                        "target",
                        message="Select target node",
                        choices=capability_nodes,
                        carousel=True,
                    )
                ]
                answers = inquirer.prompt(questions)
                if not answers:
                    print("Cancelled")
                    return
                target = answers["target"]

            print(f"\nNote: Full connection with handle selection coming soon")
            print(f"Selected: {source} -> {target}")
            print("For now, specify full connection strings:")
            print("  arm app connection add <inst>:<cap>:<handle> <inst>:<cap>:<handle>")
            return

        # Parse source and target
        src_parts = source.split(":")
        tgt_parts = target.split(":")

        if len(src_parts) != 3 or len(tgt_parts) != 3:
            print("Error: Connection format must be <instance_id>:<capability>:<handle>")
            print(
                "Example: arm app connection add inst-123:camera:image_pub inst-456:detector:image_sub"
            )
            raise click.Abort()

        src_instance, src_capability, src_handle = src_parts
        tgt_instance, tgt_capability, tgt_handle = tgt_parts

        # Create connection using SDK
        full_source_handle = f"{src_capability}:{src_handle}"
        full_target_handle = f"{tgt_capability}:{tgt_handle}"

        edge_id = application.connect_node(
            state, src_instance, full_source_handle, tgt_instance, full_target_handle
        )

        # Save the updated state
        application.save(state, active_path)

        print(f"Connected {source} -> {target}")
        print(f"Edge ID: {edge_id}")

    except KeyboardInterrupt:
        print("\nCancelled")
    except Exception as e:
        print(f"Error adding connection: {e}")
        raise click.Abort()


@connection.command("remove")
@click.argument("edge_id", required=False)
@click.pass_context
def remove(ctx, edge_id: Optional[str] = None):
    """Remove a connection between nodes

    If no edge_id provided, shows interactive selection of existing connections.
    """
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load application state
        state = application.load(active_path)

        # Interactive mode if no edge_id
        if edge_id is None:
            # Build list of existing edges
            edges = []
            for u, v, key, data in state.graph.edges(keys=True, data=True):
                eid = data.get("id", key)
                edge_type = data.get("type", "unknown")
                src_handle = data.get("source_handle", "")
                tgt_handle = data.get("target_handle", "")

                display = f"{u} -> {v}"
                if src_handle and tgt_handle:
                    display = f"{src_handle} -> {tgt_handle}"
                display += f" ({edge_type})"

                edges.append((display, eid))

            if not edges:
                print("No connections found in application")
                return

            # Select edge to disconnect
            questions = [
                inquirer.List(
                    "edge",
                    message="Select connection to remove",
                    choices=edges,
                    carousel=True,
                )
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return

            edge_id = answers["edge"]

        # Disconnect using SDK
        success = application.disconnect_node(state, edge_id)

        if success:
            # Save the updated state
            application.save(state, active_path)
            print(f"Removed connection: {edge_id}")
        else:
            print(f"Connection not found: {edge_id}")

    except KeyboardInterrupt:
        print("\nCancelled")
    except Exception as e:
        print(f"Error removing connection: {e}")
        raise click.Abort()


@connection.command("list")
@click.pass_context
def list_connections(ctx):
    """List all connections in the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load application state
        state = application.load(active_path)

        # Get all edges
        edges = list(state.graph.edges(keys=True, data=True))

        if not edges:
            print("No connections in application")
            return

        print("Connections:")
        for u, v, key, data in edges:
            edge_id = data.get("id", key)
            edge_type = data.get("type", "unknown")
            src_handle = data.get("source_handle", "")
            tgt_handle = data.get("target_handle", "")

            print(f"\n  {edge_id}:")
            if src_handle and tgt_handle:
                print(f"    {src_handle} -> {tgt_handle}")
            else:
                print(f"    {u} -> {v}")
            print(f"    Type: {edge_type}")

    except Exception as e:
        print(f"Error listing connections: {e}")
        raise click.Abort()


@connection.command("info")
@click.argument("edge_id")
@click.pass_context
def info(ctx, edge_id: str):
    """Show detailed information about a specific connection"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load application state
        state = application.load(active_path)

        # Find the edge
        found = False
        for u, v, key, data in state.graph.edges(keys=True, data=True):
            if data.get("id") == edge_id:
                found = True
                print(f"Connection: {edge_id}")
                print(f"  Source node: {u}")
                print(f"  Target node: {v}")
                print(f"  Type: {data.get('type', 'unknown')}")

                if "source_handle" in data:
                    print(f"  Source handle: {data['source_handle']}")
                if "target_handle" in data:
                    print(f"  Target handle: {data['target_handle']}")

                # Show any additional metadata
                metadata = {
                    k: v
                    for k, v in data.items()
                    if k not in ["id", "type", "source_handle", "target_handle"]
                }
                if metadata:
                    print("  Metadata:")
                    for k, v in metadata.items():
                        print(f"    {k}: {v}")
                break

        if not found:
            print(f"Connection not found: {edge_id}")

    except Exception as e:
        print(f"Error getting connection info: {e}")
        raise click.Abort()
