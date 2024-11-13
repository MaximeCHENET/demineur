# replay_dialog.py
import tkinter as tk
from tkinter import ttk


class ReplayDialog:
    """Dialog for selecting a previous game to replay.

    Displays a list of recent games with their configurations
    and allows the user to select one for replay.
    """

    def __init__(self, root, recent_seeds, on_select):
        """Initialize the replay dialog.

        Args:
            root (tk.Tk): Tkinter root window
            recent_seeds (list): List of dictionaries containing recent game data
                Each dict contains: width, height, mines, date
            on_select (callable): Callback for when a game is selected for replay
        """
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Replay Game")
        self.dialog.geometry("500x400")
        self.dialog.transient(root)
        self.dialog.grab_set()

        # Create main frame for seed list
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Add dialog title
        ttk.Label(frame, text="Select a game to replay:",
                  font=('TkDefaultFont', 12, 'bold')).pack(pady=10)

        # Create buttons for each recent game
        for seed_data in recent_seeds:
            seed_frame = ttk.Frame(frame)
            seed_frame.pack(fill=tk.X, pady=5)

            # Format button text with game information
            button_text = (f"Grid: {seed_data['width']}x{seed_data['height']}, "
                           f"Mines: {seed_data['mines']}\n"
                           f"Date: {seed_data['date']}")

            ttk.Button(
                seed_frame,
                text=button_text,
                command=lambda sd=seed_data: self._select_and_close(sd, on_select)
            ).pack(fill=tk.X)

        # Add cancel button
        ttk.Button(frame, text="Cancel",
                   command=self.dialog.destroy).pack(pady=10)

    def _select_and_close(self, seed_data, on_select):
        """Handle game selection and close the dialog.

        Args:
            seed_data (dict): Selected game configuration data
            on_select (callable): Callback function to handle selection
        """
        on_select(seed_data)
        self.dialog.destroy()