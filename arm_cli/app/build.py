import click

from arm_robotics_sdk import build, project


def _build(ctx, clean: bool = False):
    """Build deployment artifacts for the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()
        
        print(f"Building application at {active_path}...")
        
        # Build the project
        success, built_dirs, errors = build.build_project(active_path, [], clean=clean)
        
        if success:
            print("\nBuild successful!")
            if built_dirs:
                print("\nGenerated stack directories:")
                for stack_dir in built_dirs:
                    print(f"  {stack_dir}")
        else:
            print("\nBuild failed!")
            if errors:
                print("\nErrors:")
                for error in errors:
                    print(f"  {error}")
            raise click.Abort()
        
    except Exception as e:
        print(f"Error building application: {e}")
        raise click.Abort()


# Create the command object
build = click.command(name="build")(
    click.option("--clean", is_flag=True, help="Clean build (remove existing artifacts)")(
        click.pass_context(_build)
    )
)

