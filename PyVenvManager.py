import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog
import subprocess
import sys
import json
import shutil
from pathlib import Path
import threading
import time

class VirtualEnvManager:
    # Application version
    VERSION = "1.0.0"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Python Virtual Environment Manager")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set icon if it exists
        try:
            # When running as exe, the icon is at the same level as the executable
            icon_path = os.path.join(os.path.dirname(sys.executable), "icon.ico")
            if not os.path.exists(icon_path):
                # When running as script, the icon might be at the same level
                icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set icon: {e}")
        
        # Create a menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Set theme colors
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "background": "#f5f5f5",
            "text": "#333333",
            "accent": "#e74c3c"
        }
        
        # Initialize animation variables
        self.animation_running = False
        self.animation_thread = None
        self.loading = False
        self.loading_thread = None
        
        # Load settings or set defaults
        self.settings_file = os.path.join(os.path.expanduser("~"), ".pyenvmanager", "settings.json")
        self.load_settings()
        
        # Create GUI components
        self.setup_ui()
        
        # Populate the listbox with available environments
        self.refresh_env_list()
    
    def load_settings(self):
        """Load settings from JSON file or create defaults"""
        # Create app data directory in AppData/Local (Windows) or .local/share (Linux)
        if os.name == 'nt':
            app_data_dir = os.path.join(os.getenv('LOCALAPPDATA'), "PyVenvManager")
        else:
            app_data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "PyVenvManager")
        
        # Create directory if it doesn't exist
        os.makedirs(app_data_dir, exist_ok=True)
        
        # Default settings
        self.settings = {
            "venv_dir": app_data_dir,
            "python_path": sys.executable,
            "theme": "light"
        }
        
        # Create settings directory if it doesn't exist
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # Try to load existing settings
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Ensure venv directory exists
        os.makedirs(self.settings["venv_dir"], exist_ok=True)
        
        # Set working directory
        self.venv_dir = self.settings["venv_dir"]
    
    def save_settings(self):
        """Save current settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save settings: {e}")
            return False
    
    def setup_ui(self):
        # Set style
        self.style = ttk.Style()
        self.apply_theme()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with animation effect
        self.title_frame = ttk.Frame(main_frame)
        self.title_frame.pack(fill=tk.X, pady=5)
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="Python Virtual Environment Manager", 
            font=("Helvetica", 16, "bold"),
            foreground=self.colors["primary"]
        )
        self.title_label.pack(pady=5)
        
        # Path display
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="Environments Path:").pack(side=tk.LEFT)
        self.path_label = ttk.Label(path_frame, text=self.venv_dir, font=("Courier", 9))
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Environments tab
        env_tab = ttk.Frame(self.notebook)
        self.notebook.add(env_tab, text="Environments")
        
        # Environment listbox with scrollbar
        list_frame = ttk.LabelFrame(env_tab, text="Available Environments")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        self.env_listbox = tk.Listbox(
            list_frame, 
            font=("Courier", 10), 
            height=10,
            bg=self.colors["background"],
            fg=self.colors["text"],
            selectbackground=self.colors["primary"],
            activestyle="dotbox"
        )
        self.env_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.env_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.env_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Double-click to activate
        self.env_listbox.bind("<Double-1>", lambda e: self.activate_environment())
        
        # Buttons frame for environment actions
        btn_frame = ttk.Frame(env_tab)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            btn_frame, 
            text="Activate",
            command=self.activate_environment,
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=2)
        
        tk.Button(
            btn_frame, 
            text="Create New",
            command=self.show_create_dialog,
            bg=self.colors["secondary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=2)
        
        tk.Button(
            btn_frame, 
            text="Import",
            command=self.import_environment,
            bg=self.colors["secondary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=2)
        
        tk.Button(
            btn_frame, 
            text="Delete",
            command=self.delete_environment,
            bg=self.colors["accent"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=2)
        
        tk.Button(
            btn_frame, 
            text="Refresh",
            command=self.refresh_env_list,
            bg=self.colors["background"],
            fg=self.colors["text"],
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.LEFT, padx=5, pady=2)
        
        # Settings tab
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        
        # Environment directory settings
        dir_frame = ttk.LabelFrame(settings_tab, text="Environment Directory")
        dir_frame.pack(fill=tk.X, expand=False, pady=10, padx=10)
        
        ttk.Label(dir_frame, text="Current Directory:").pack(anchor=tk.W, padx=5, pady=5)
        ttk.Label(dir_frame, text=self.venv_dir, font=("Courier", 9)).pack(anchor=tk.W, padx=15, pady=2)
        
        tk.Button(
            dir_frame,
            text="Change Directory",
            command=self.change_venv_dir,
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(anchor=tk.W, padx=5, pady=5)
        
        # Python executable settings
        py_frame = ttk.LabelFrame(settings_tab, text="Python Executable")
        py_frame.pack(fill=tk.X, expand=False, pady=10, padx=10)
        
        self.python_path_var = tk.StringVar(value=self.settings["python_path"])
        py_entry = ttk.Entry(py_frame, textvariable=self.python_path_var, width=50)
        py_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        
        tk.Button(
            py_frame, 
            text="Browse",
            command=self.browse_python_executable,
            bg=self.colors["background"],
            fg=self.colors["text"],
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.RIGHT, padx=5)
        
        # Theme settings
        theme_frame = ttk.LabelFrame(settings_tab, text="Theme Settings")
        theme_frame.pack(fill=tk.X, expand=False, pady=10, padx=10)
        
        ttk.Label(theme_frame, text="Choose Theme:").pack(anchor=tk.W, padx=5, pady=5)
        
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        ttk.Radiobutton(
            theme_frame, 
            text="Light", 
            variable=self.theme_var, 
            value="light",
            command=self.change_theme
        ).pack(anchor=tk.W, padx=20, pady=2)
        
        ttk.Radiobutton(
            theme_frame, 
            text="Dark", 
            variable=self.theme_var, 
            value="dark",
            command=self.change_theme
        ).pack(anchor=tk.W, padx=20, pady=2)
        
        tk.Button(
            theme_frame,
            text="Customize Colors",
            command=self.customize_colors,
            bg=self.colors["background"],
            fg=self.colors["text"],
            relief=tk.RAISED,
            padx=10
        ).pack(anchor=tk.W, padx=5, pady=10)
        
        tk.Button(
            settings_tab,
            text="Save Settings",
            command=self.save_settings_from_ui,
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.BOTTOM, pady=10)
        
        # Status bar with animation capability
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        # Remove the inline progress bar from the main window
        self.progress = None
        self.progress_dialog = None

        # Start title animation
        self.start_title_animation()
    
    def apply_theme(self):
        """Apply the current theme to the UI"""
        if self.settings.get("theme") == "dark":
            self.colors = {
                "primary": "#3498db",
                "secondary": "#2ecc71",
                "background": "#333333",
                "text": "#f5f5f5",
                "accent": "#e74c3c"
            }
        else:  # Light theme
            self.colors = {
                "primary": "#3498db",
                "secondary": "#2ecc71",
                "background": "#f5f5f5",
                "text": "#333333",
                "accent": "#e74c3c"
            }
        
        # Override with custom colors if they exist
        if "custom_colors" in self.settings:
            self.colors.update(self.settings["custom_colors"])
        
        # Configure styles
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], foreground=self.colors["text"])
        
        # Fix button styling to ensure text is visible
        self.style.configure("TButton", 
                             background=self.colors["background"], 
                             foreground=self.colors["text"])
        
        # Create button styles with explicit foreground colors
        self.style.configure("Primary.TButton", 
                             background=self.colors["primary"], 
                             foreground="#ffffff")
        
        self.style.map("Primary.TButton",
                       foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                       background=[('active', self.colors["primary"]), ('pressed', self.colors["primary"])])
        
        self.style.configure("Secondary.TButton", 
                             background=self.colors["secondary"], 
                             foreground="#ffffff")
        
        self.style.map("Secondary.TButton",
                       foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                       background=[('active', self.colors["secondary"]), ('pressed', self.colors["secondary"])])
        
        self.style.configure("Accent.TButton", 
                             background=self.colors["accent"], 
                             foreground="#ffffff")
        
        self.style.map("Accent.TButton",
                       foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                       background=[('active', self.colors["accent"]), ('pressed', self.colors["accent"])])
        
        # Apply to root window
        self.root.configure(bg=self.colors["background"])
        
        # If env_listbox exists, update its colors
        if hasattr(self, "env_listbox"):
            self.env_listbox.configure(
                bg=self.colors["background"],
                fg=self.colors["text"],
                selectbackground=self.colors["primary"]
            )
        
        # Update button colors
        self.update_button_colors()
    
    def update_button_colors(self):
        """Update colors for all tk buttons when theme changes"""
        def update_buttons(widget):
            if isinstance(widget, tk.Button):
                if "primary" in str(widget["bg"]):
                    widget.configure(bg=self.colors["primary"], fg="white")
                elif "secondary" in str(widget["bg"]):
                    widget.configure(bg=self.colors["secondary"], fg="white")
                elif "accent" in str(widget["bg"]):
                    widget.configure(bg=self.colors["accent"], fg="white")
                else:
                    widget.configure(bg=self.colors["background"], fg=self.colors["text"])
            
            # Recursively update children
            for child in widget.winfo_children():
                update_buttons(child)
        
        # Start the recursive update from the root window
        update_buttons(self.root)
    
    def change_theme(self):
        """Change the UI theme"""
        self.settings["theme"] = self.theme_var.get()
        self.apply_theme()
    
    def customize_colors(self):
        """Let the user customize UI colors"""
        color_window = tk.Toplevel(self.root)
        color_window.title("Customize Colors")
        color_window.geometry("400x300")
        
        color_frame = ttk.Frame(color_window, padding=10)
        color_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create color pickers for each color
        color_keys = ["primary", "secondary", "background", "text", "accent"]
        color_vars = {}
        
        for i, key in enumerate(color_keys):
            row_frame = ttk.Frame(color_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(row_frame, text=f"{key.capitalize()} Color:").pack(side=tk.LEFT, padx=5)
            
            color_vars[key] = tk.StringVar(value=self.colors[key])
            color_entry = ttk.Entry(row_frame, textvariable=color_vars[key], width=10)
            color_entry.pack(side=tk.LEFT, padx=5)
            
            color_button = ttk.Button(
                row_frame, 
                text="Pick Color",
                command=lambda k=key, v=color_vars[key]: self.pick_color(v)
            )
            color_button.pack(side=tk.LEFT, padx=5)
            
            # Color preview
            preview = tk.Canvas(row_frame, width=20, height=20, bg=self.colors[key])
            preview.pack(side=tk.LEFT, padx=5)
            
            # Update preview when color changes
            color_vars[key].trace_add("write", lambda *args, c=preview, v=color_vars[key]: c.config(bg=v.get()))
        
        button_frame = ttk.Frame(color_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text="Apply Colors",
            command=lambda: self.apply_custom_colors(color_vars, color_window),
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=color_window.destroy,
            bg=self.colors["background"],
            fg=self.colors["text"],
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.RIGHT, padx=5)
    
    def pick_color(self, color_var):
        """Open color chooser and update the color variable"""
        color = colorchooser.askcolor(color_var.get())[1]
        if color:
            color_var.set(color)
    
    def apply_custom_colors(self, color_vars, window):
        """Apply the custom colors to the UI"""
        custom_colors = {k: v.get() for k, v in color_vars.items()}
        self.settings["custom_colors"] = custom_colors
        self.colors.update(custom_colors)
        self.apply_theme()
        window.destroy()
    
    def start_title_animation(self):
        """Start an animation for the title"""
        if not self.animation_running:
            self.animation_running = True
            self.animation_thread = threading.Thread(target=self.run_title_animation)
            self.animation_thread.daemon = True
            self.animation_thread.start()
    
    def run_title_animation(self):
        """Run the title animation"""
        colors = [self.colors["primary"], self.colors["secondary"], self.colors["accent"]]
        i = 0
        try:
            while self.animation_running and hasattr(self, "title_label"):
                color = colors[i % len(colors)]
                self.root.after(0, lambda c=color: self.title_label.config(foreground=c))
                time.sleep(2)
                i += 1
        except Exception as e:
            print(f"Animation error: {e}")
        finally:
            self.animation_running = False
    
    def show_loading(self, message="Loading..."):
        """Show a modal progress dialog with a progress bar"""
        if getattr(self, 'progress_dialog', None) is not None:
            return  # Already showing
        def create_dialog():
            self.progress_dialog = tk.Toplevel(self.root)
            self.progress_dialog.title("Please Wait")
            self.progress_dialog.geometry("350x100")
            self.progress_dialog.resizable(False, False)
            self.progress_dialog.transient(self.root)
            self.progress_dialog.grab_set()
            self.progress_dialog.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close
            label = ttk.Label(self.progress_dialog, text=message, anchor=tk.CENTER, font=("Segoe UI", 11))
            label.pack(pady=(20, 10), padx=10)
            self.progress = ttk.Progressbar(self.progress_dialog, mode="indeterminate")
            self.progress.pack(fill=tk.X, padx=20, pady=(0, 15))
            self.progress.start(10)
        self.root.after(0, create_dialog)
        self.loading = True
        self.loading_thread = threading.Thread(target=self.run_loading_animation, args=(message,))
        self.loading_thread.daemon = True
        self.loading_thread.start()

    def stop_loading(self):
        """Stop the loading animation and close the progress dialog"""
        self.loading = False
        def close_dialog():
            if getattr(self, 'progress', None) is not None:
                self.progress.stop()
            if getattr(self, 'progress_dialog', None) is not None:
                self.progress_dialog.grab_release()
                self.progress_dialog.destroy()
                self.progress_dialog = None
            self.progress = None
        self.root.after(0, close_dialog)
    
    def run_loading_animation(self, message):
        """Run the loading animation for the modal progress dialog"""
        dots = [".", "..", "..."]
        i = 0
        try:
            while self.loading and getattr(self, 'progress_dialog', None) is not None:
                if getattr(self, 'progress_dialog', None) is not None:
                    for widget in self.progress_dialog.winfo_children():
                        if isinstance(widget, ttk.Label):
                            widget.config(text=f"{message} {dots[i % len(dots)]}")
                time.sleep(0.3)
                i += 1
        except Exception:
            pass
    
    def refresh_env_list(self):
        """Refresh the list of available virtual environments"""
        self.show_loading("Refreshing environment list")
        self.env_listbox.delete(0, tk.END)
        self.envs = []
        
        try:
            # List all directories in the venv_dir
            if os.path.exists(self.venv_dir):
                for d in os.listdir(self.venv_dir):
                    full_path = os.path.join(self.venv_dir, d)
                    # Check if it's a directory and has activation script (basic check)
                    if os.path.isdir(full_path):
                        scripts_dir = os.path.join(full_path, "Scripts" if os.name == "nt" else "bin")
                        if os.path.exists(scripts_dir):
                            self.envs.append(d)
                
                for i, env in enumerate(self.envs, 1):
                    self.env_listbox.insert(tk.END, f"{i}. {env}")
                    # Add alternating row colors
                    if i % 2 == 0:
                        self.env_listbox.itemconfig(i-1, bg="#f0f0f0" if self.settings.get("theme") == "light" else "#3a3a3a")
                
                self.stop_loading()
                if not self.envs:
                    self.status_var.set("No virtual environments found")
                else:
                    self.status_var.set(f"Found {len(self.envs)} virtual environments")
            else:
                self.stop_loading()
                self.status_var.set(f"Directory not found: {self.venv_dir}")
        except Exception as e:
            self.stop_loading()
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to list environments: {str(e)}")
    
    def activate_environment(self):
        """Activate the selected virtual environment"""
        selection = self.env_listbox.curselection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a virtual environment to activate")
            return
        
        # Get the selected environment name (removing the number prefix)
        selected_idx = selection[0]
        env_name = self.envs[selected_idx]
        
        # Find activation script based on OS
        if os.name == "nt":  # Windows
            activate_script = os.path.join(self.venv_dir, env_name, "Scripts", "activate.bat")
        else:  # Unix/Linux/Mac
            activate_script = os.path.join(self.venv_dir, env_name, "bin", "activate")
        
        if not os.path.exists(activate_script):
            messagebox.showerror("Error", f"Activation script not found at:\n{activate_script}")
            return
        
        try:
            self.show_loading(f"Activating {env_name}")
            
            # Check if environment has a main file
            env_settings_file = os.path.join(self.venv_dir, env_name, ".env_settings", "settings.json")
            main_file = None
            
            if os.path.exists(env_settings_file):
                try:
                    with open(env_settings_file, 'r') as f:
                        env_settings = json.load(f)
                        main_file = env_settings.get("main_file")
                except:
                    pass
            
            # Start a new terminal window with the activated environment
            if os.name == "nt":  # Windows
                if main_file and os.path.exists(main_file):
                    # Run with main file
                    cmd_command = f'start cmd.exe /K "{activate_script} && echo Virtual environment \'{env_name}\' activated. && python "{main_file}""'
                else:
                    # Normal activation without main file
                    cmd_command = f'start cmd.exe /K "{activate_script} && echo Virtual environment \'{env_name}\' activated. Type \'deactivate\' to exit."'
                
                subprocess.run(cmd_command, shell=True)
            else:  # Unix/Linux/Mac
                terminal_cmd = f"gnome-terminal --" if shutil.which("gnome-terminal") else "xterm -e"
                
                if main_file and os.path.exists(main_file):
                    # Run with main file
                    cmd = f'{terminal_cmd} bash -c \'source "{activate_script}"; echo "Virtual environment \'{env_name}\' activated."; python "{main_file}"; exec bash\''
                else:
                    # Normal activation without main file
                    cmd = f'{terminal_cmd} bash -c \'source "{activate_script}"; echo "Virtual environment \'{env_name}\' activated. Type \'deactivate\' to exit."; exec bash\''
                
                subprocess.run(cmd, shell=True)
            
            self.stop_loading()
            self.status_var.set(f"Activated '{env_name}' environment")
            
            # Add message if main file was executed
            if main_file and os.path.exists(main_file):
                self.status_var.set(f"Activated '{env_name}' and running {os.path.basename(main_file)}")
                
        except Exception as e:
            self.stop_loading()
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Activation Error", f"Failed to activate environment: {str(e)}")
    
    def show_create_dialog(self):
        """Show dialog to create a new virtual environment"""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create New Virtual Environment")
        create_window.geometry("450x300")
        create_window.transient(self.root)
        create_window.grab_set()
        
        frame = ttk.Frame(create_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Environment name
        ttk.Label(frame, text="Environment Name:").pack(anchor=tk.W, pady=(10, 5))
        name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, padx=5, pady=5)
        name_entry.focus()
        
        # Python version selection
        ttk.Label(frame, text="Python Executable:").pack(anchor=tk.W, pady=(10, 5))
        
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        py_path_var = tk.StringVar(value=self.settings["python_path"])
        py_entry = ttk.Entry(path_frame, textvariable=py_path_var, width=40)
        py_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_file(py_path_var, [("Python", "python.exe"), ("All files", "*.*")])
        ).pack(side=tk.RIGHT, padx=5)
        
        # Packages to install
        ttk.Label(frame, text="Packages to Install (space separated):").pack(anchor=tk.W, pady=(10, 5))
        packages_var = tk.StringVar()
        packages_entry = ttk.Entry(frame, textvariable=packages_var, width=40)
        packages_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Options
        options_frame = ttk.Frame(frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        system_site_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text="System site packages", 
            variable=system_site_var
        ).pack(side=tk.LEFT, padx=5)
        
        no_pip_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame, 
            text="Without pip", 
            variable=no_pip_var
        ).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)
        
        tk.Button(
            btn_frame,
            text="Create",
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=10,
            command=lambda: self.create_environment(
                name_var.get().strip(),
                py_path_var.get(),
                packages_var.get(),
                system_site_var.get(),
                no_pip_var.get(),
                create_window
            )
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=create_window.destroy,
            bg=self.colors["background"],
            fg=self.colors["text"],
            relief=tk.RAISED,
            padx=10
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_environment(self, name, python_path, packages, system_site, no_pip, window):
        """Create a new virtual environment"""
        if not name:
            messagebox.showerror("Error", "Please enter a name for the environment")
            return
        
        # Check if environment already exists
        env_path = os.path.join(self.venv_dir, name)
        if os.path.exists(env_path):
            messagebox.showerror("Error", f"Environment '{name}' already exists")
            return
        
        # Build command
        cmd = [python_path, "-m", "venv"]
        
        if system_site:
            cmd.append("--system-site-packages")
            
        if no_pip:
            cmd.append("--without-pip")
            
        cmd.append(env_path)
        
        # Close the window
        window.destroy()
        
        # Start creation in a separate thread
        threading.Thread(target=self._create_env_thread, args=(cmd, name, packages)).start()
    
    def _create_env_thread(self, cmd, name, packages):
        """Thread function to create environment and install packages"""
        self.show_loading(f"Creating environment '{name}'")
        
        try:
            # Create the environment
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Install packages if specified
            if packages.strip():
                self.status_var.set(f"Installing packages in '{name}'...")
                
                # Get pip path
                if os.name == "nt":
                    pip_path = os.path.join(self.venv_dir, name, "Scripts", "pip.exe")
                else:
                    pip_path = os.path.join(self.venv_dir, name, "bin", "pip")
                
                package_list = packages.split()
                pip_cmd = [pip_path, "install"] + package_list
                
                process = subprocess.run(pip_cmd, check=True, capture_output=True, text=True)
            
            self.root.after(0, lambda: self.status_var.set(f"Environment '{name}' created successfully"))
            self.root.after(0, self.refresh_env_list)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Error creating environment: {e}\n{e.stderr}"
            self.root.after(0, lambda: messagebox.showerror("Creation Failed", error_msg))
            self.root.after(0, lambda: self.status_var.set("Environment creation failed"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_var.set("Environment creation failed"))
        finally:
            self.stop_loading()
    
    def browse_file(self, var, filetypes):
        """Browse for a file and update the variable"""
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            var.set(filename)
    
    def browse_python_executable(self):
        """Browse for Python executable"""
        if os.name == "nt":
            filetypes = [("Python", "python.exe"), ("All files", "*.*")]
        else:
            filetypes = [("Python", "*python*"), ("All files", "*")]
            
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.python_path_var.set(filename)
    
    def import_environment(self):
        """Import an existing virtual environment"""
        source_dir = filedialog.askdirectory(title="Select Virtual Environment Directory")
        if not source_dir:
            return
        
        # Ask for a name
        name = simpledialog.askstring("Import Environment", "Enter name for imported environment:")
        if not name:
            return
            
        # Check if environment already exists
        target_dir = os.path.join(self.venv_dir, name)
        if os.path.exists(target_dir):
            messagebox.showerror("Error", f"Environment '{name}' already exists")
            return
            
        # Start import in a separate thread
        threading.Thread(target=self._import_env_thread, args=(source_dir, target_dir, name)).start()
    
    def _import_env_thread(self, source_dir, target_dir, name):
        """Thread function to import environment"""
        # Always show loading from main thread
        self.root.after(0, lambda: self.show_loading(f"Importing environment as '{name}'"))
        try:
            # Small delay to ensure loading animation appears
            time.sleep(0.5)
            # Copy the environment (this can take time for larger environments)
            shutil.copytree(source_dir, target_dir)
            
            # Find main Python file if exists (common names)
            main_file = None
            for common_name in ["main.py", "app.py", "run.py", "start.py", "__main__.py"]:
                potential_main = os.path.join(target_dir, common_name)
                if os.path.exists(potential_main):
                    main_file = potential_main
                    break
                    
            # If found, store it in env settings
            if main_file:
                env_settings_dir = os.path.join(target_dir, ".env_settings")
                os.makedirs(env_settings_dir, exist_ok=True)
                
                env_settings = {
                    "main_file": main_file
                }
                
                with open(os.path.join(env_settings_dir, "settings.json"), 'w') as f:
                    json.dump(env_settings, f)
            
            # Stop loading and update UI in the main thread
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: self.status_var.set(f"Environment imported as '{name}'"))
            self.root.after(0, self.refresh_env_list)
            
            # Ask if user wants to delete the original environment
            self.root.after(100, lambda: self._ask_delete_original(source_dir, name))
            
        except Exception as e:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Import Failed", str(e)))
            self.root.after(0, lambda: self.status_var.set("Environment import failed"))
        
    def _ask_delete_original(self, source_dir, env_name):
        """Ask if user wants to delete the original environment after import"""
        if messagebox.askyesno("Delete Original", 
                               f"Environment '{env_name}' has been imported successfully. "
                               f"Do you want to delete the original environment at:\n{source_dir}?"):
            # Show loading animation before starting deletion
            self.root.after(0, lambda: self.show_loading(f"Deleting original environment at {source_dir}"))
            
            # Use a separate thread for deletion to keep UI responsive
            threading.Thread(target=self._delete_original_thread, args=(source_dir, env_name)).start()
    
    def _delete_original_thread(self, source_dir, env_name):
        """Thread to delete original environment after import"""
        try:
            # Small delay to ensure loading animation appears
            time.sleep(0.5)
            
            # Delete the environment
            shutil.rmtree(source_dir)
            
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: self.status_var.set(f"Original environment deleted. '{env_name}' imported successfully."))
        except Exception as e:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Deletion Error", f"Could not delete original environment: {e}"))
            self.root.after(0, lambda: self.status_var.set(f"Import successful, but could not delete original environment."))
    
    def delete_environment(self):
        """Delete the selected environment"""
        selection = self.env_listbox.curselection()
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a virtual environment to delete")
            return
            
        selected_idx = selection[0]
        env_name = self.envs[selected_idx]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{env_name}'?"):
            return
            
        env_path = os.path.join(self.venv_dir, env_name)
        
        # Start deletion in a separate thread
        threading.Thread(target=self._delete_env_thread, args=(env_path, env_name)).start()
    
    def _delete_env_thread(self, env_path, env_name):
        """Thread function to delete environment"""
        # Always show loading from main thread
        self.root.after(0, lambda: self.show_loading(f"Deleting environment '{env_name}'"))
        try:
            # Small delay to ensure loading animation appears
            time.sleep(0.5)
            
            # Delete the environment
            shutil.rmtree(env_path)
            
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: self.status_var.set(f"Environment '{env_name}' deleted"))
            self.root.after(0, self.refresh_env_list)
            
        except Exception as e:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Deletion Failed", str(e)))
            self.root.after(0, lambda: self.status_var.set("Environment deletion failed"))
    
    def change_venv_dir(self):
        """Change the directory where virtual environments are stored"""
        new_dir = filedialog.askdirectory(title="Select Directory for Virtual Environments")
        if not new_dir:
            return
            
        # Update settings
        self.venv_dir = new_dir
        self.settings["venv_dir"] = new_dir
        
        # Update UI
        self.path_label.config(text=self.venv_dir)
        
        # Save settings
        if self.save_settings():
            self.status_var.set(f"Environment directory changed to {new_dir}")
            self.refresh_env_list()
              # Update the display in settings tab
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Notebook):
                    for tab in child.winfo_children():
                        for frame in tab.winfo_children():
                            if isinstance(frame, ttk.LabelFrame) and frame.winfo_children():
                                for label in frame.winfo_children():
                                    if isinstance(label, ttk.Label) and self.venv_dir in str(label.cget("text")):
                                        label.config(text=self.venv_dir)
    
    def save_settings_from_ui(self):
        """Save settings from UI elements"""
        self.settings["python_path"] = self.python_path_var.get()
        self.settings["theme"] = self.theme_var.get()
        
        if self.save_settings():
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully")
            self.status_var.set("Settings saved")
    
    def show_about(self):
        """Show the About dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Python Virtual Environment Manager")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Try to use the same icon
        try:
            if hasattr(self.root, 'iconbitmap') and self.root._w + "Icon" in self.root.children:
                about_window.iconbitmap(self.root.iconbitmap())
        except:
            pass
        
        frame = ttk.Frame(about_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            frame, 
            text="Python Virtual Environment Manager", 
            font=("Helvetica", 14, "bold"),
            foreground=self.colors["primary"]
        ).pack(pady=(0, 10))
        
        # Version
        ttk.Label(
            frame,
            text=f"Version {self.VERSION}",
            font=("Helvetica", 10)
        ).pack()
        
        # Description
        description = """
A tool to create, manage, and activate Python virtual environments
with an easy-to-use graphical interface.
        """
        ttk.Label(
            frame,
            text=description,
            justify=tk.CENTER,
            wraplength=350
        ).pack(pady=10)
        
        # Copyright
        ttk.Label(
            frame,
            text=f"© {time.strftime('%Y')} PyVenvManager",
            font=("Helvetica", 8)
        ).pack(pady=(10, 5))
        
        # Close button
        tk.Button(
            frame,
            text="OK",
            command=about_window.destroy,
            bg=self.colors["primary"],
            fg="white",
            relief=tk.RAISED,
            padx=20
        ).pack(pady=10)

        # To build a standalone Windows executable for non-Python users:
        # 1. Install pyinstaller: pip install pyinstaller
        # 2. Run: pyinstaller --onefile --windowed --icon=icon.ico PyVenvManager.py
        # 3. The .exe will be in the 'dist' folder.

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualEnvManager(root)
    root.mainloop()
