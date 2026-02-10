"""
Maya script with a GUI containing a blue button that creates a locator.
"""

import maya.cmds as cmds


def create_locator():
    """Create a locator at the origin."""
    cmds.spaceLocator()
    print("Locator created.")


def show_window():
    """Create and display the locator GUI window."""
    window_name = "locatorCreatorWindow"

    # Delete window if it already exists
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create the main window
    window = cmds.window(window_name, title="Create Locator", sizeable=True)
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=("both", 20))

    cmds.text(label="", height=10)
    cmds.text(label="Click the button to create a locator at the origin", align="center")

    # Blue button - Maya uses RGB values 0-1
    cmds.button(
        label="Create Locator",
        backgroundColor=(0.2, 0.4, 0.8),  # Blue
        height=40,
        command=lambda x: create_locator(),
    )

    cmds.text(label="", height=10)
    cmds.separator(style="none", height=5)

    cmds.showWindow(window)


if __name__ == "__main__":
    show_window()
