def clearLayout(layout, nhead=0):
    """Clears all widgets from a layout

    TODO: Do this recursively with sublayouts too
    """

    while layout.count() > nhead:
        widget = layout.takeAt(nhead)
        widget.widget().setParent(None)
        del widget
