"""
Maya script with a GUI containing a blue button that creates locators.
Supports + and - buttons to adjust the quantity with a visual count display.
"""

import maya.cmds as cmds

# Module-level count for locator quantity (persists across callbacks)
_locator_count = 1


def update_count(delta, count_text):
    """Increase or decrease the locator count and update the display."""
    global _locator_count
    _locator_count = max(1, _locator_count + delta)
    cmds.text(count_text, edit=True, label=str(_locator_count))


def create_locators(*args):
    """Create locators at the origin. Quantity is determined by the current count."""
    global _locator_count
    for _ in range(_locator_count):
        cmds.spaceLocator()
    print(f"Created {_locator_count} locator(s).")


def show_window():
    """Create and display the locator GUI window."""
    global _locator_count
    _locator_count = 1

    window_name = "locatorCreatorWindow"

    # Delete window if it already exists
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create the main window
    window = cmds.window(window_name, title="Create Locator", sizeable=True)
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=("both", 20))

    cmds.text(label="", height=10)
    cmds.text(label="Click the button to create locator(s) at the origin", align="center")

    # Row: [ - ] [ count ] [ + ] with red buttons
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(50, 60, 50), columnAttach=(1, "both", 5))
    count_text = cmds.text(label="1", align="center", font="boldLabelFont")
    cmds.button(
        label="-",
        backgroundColor=(0.8, 0.2, 0.2),  # Red
        height=30,
        command=lambda x, ct=count_text: update_count(-1, ct),
    )
    cmds.button(
        label="+",
        backgroundColor=(0.8, 0.2, 0.2),  # Red
        height=30,
        command=lambda x, ct=count_text: update_count(1, ct),
    )
    cmds.setParent("..")

    cmds.text(label="", height=5)

    # Blue button - Maya uses RGB values 0-1
    cmds.button(
        label="Create Locator",
        backgroundColor=(0.2, 0.4, 0.8),  # Blue
        height=40,
        command=lambda x: create_locators(),
    )

    cmds.text(label="", height=10)
    cmds.separator(style="none", height=5)

    cmds.showWindow(window)


if __name__ == "__main__":
    show_window()
