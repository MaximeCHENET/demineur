import tkinter as tk
from tkinter import ttk

class ReplayDialog:
    """Dialog for selecting a previous game to replay."""

    def __init__(self, root, recent_seeds, on_select):
        """Initialize the replay dialog.

        Args:
            root: Tkinter root window
            recent_seeds (list): List of recent seed data
            on_select: Callback for when a seed is selected
        """
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Rejouer une partie")
        self.dialog.geometry("500x400")
        self.dialog.transient(root)
        self.dialog.grab_set()

        # Create frame for seeds list
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(frame, text="Sélectionnez une partie à rejouer:",
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=10)

        # Create buttons for each recent seed
        for seed_data in recent_seeds:
            seed_frame = ttk.Frame(frame)
            seed_frame.pack(fill=tk.X, pady=5)

            # Format the button text
            button_text = (f"Grille: {seed_data['width']}x{seed_data['height']}, "
                         f"Mines: {seed_data['mines']}\n"
                         f"Date: {seed_data['date']}")

            ttk.Button(
                seed_frame,
                text=button_text,
                command=lambda sd=seed_data: self._select_and_close(sd, on_select)
            ).pack(fill=tk.X)

        # Cancel button
        ttk.Button(frame, text="Annuler",
                  command=self.dialog.destroy).pack(pady=10)

    def _select_and_close(self, seed_data, on_select):
        """Handle seed selection and close the dialog.

        Args:
            seed_data (dict): Selected seed data
            on_select: Callback function
        """
        on_select(seed_data)
        self.dialog.destroy()