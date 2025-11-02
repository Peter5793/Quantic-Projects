import tkinter as tk
from tkinter import messagebox
from typing import Optional
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.parking_controller import ParkingLotController
from models.vehicle import VehicleInfo

class ParkingLotView:
    """View class for the parking lot management system"""
    
    def __init__(self):
        self.controller = ParkingLotController()
        self.root = tk.Tk()
        self.root.geometry("650x850")
        self.root.resizable(0, 0)
        self.root.title("EasyPark Plus Parking Lot Manager")

        # Input variables
        self.regular_spaces = tk.StringVar()
        self.ev_spaces = tk.StringVar()
        self.level = tk.StringVar(value="1")
        self.make = tk.StringVar()
        self.model = tk.StringVar()
        self.color = tk.StringVar()
        self.registration = tk.StringVar()
        self.is_ev = tk.BooleanVar()
        self.is_motorcycle = tk.BooleanVar()
        self.space_id = tk.StringVar()
        self.search_term = tk.StringVar()

        # Output area
        self.output_area = tk.Text(self.root, width=70, height=15)

        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface"""
        # Lot Creation Section
        self._create_header("EasyPark Plus Parking Lot Manager", 0)
        self._create_header("Creation of new Parking Lot", 1)
        
        # Regular spaces input
        tk.Label(self.root, text="Regular Spaces:", font="Arial 12").grid(row=2, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.regular_spaces, width=6, font="Arial 12").grid(row=2, column=1)

        # EV spaces input
        tk.Label(self.root, text="EV Spaces:", font="Arial 12").grid(row=2, column=2, padx=5)
        tk.Entry(self.root, textvariable=self.ev_spaces, width=6, font="Arial 12").grid(row=2, column=3)

        # Level input
        tk.Label(self.root, text="Floor Level:", font="Arial 12").grid(row=3, column=0, padx=5)
        tk.Entry(self.root, textvariable=self.level, width=6, font="Arial 12").grid(row=3, column=1)

        # Create lot button
        tk.Button(self.root, text="Create Parking Lot", command=self._create_lot,
                 font="Arial 12", bg="lightblue").grid(row=4, column=0, columnspan=2, pady=10)

        # Vehicle Management Section
        self._create_header("Vehicle Management", 5)
        
        # Vehicle details inputs
        labels = ["Make:", "Model:", "Color:", "Registration:"]
        vars = [self.make, self.model, self.color, self.registration]
        
        for i, (label, var) in enumerate(zip(labels, vars)):
            row = 6 + (i // 2)
            col = (i % 2) * 2
            tk.Label(self.root, text=label, font="Arial 12").grid(row=row, column=col, padx=5)
            tk.Entry(self.root, textvariable=var, width=12, font="Arial 12").grid(row=row, column=col + 1)

        # Vehicle type checkboxes
        tk.Checkbutton(self.root, text="Electric Vehicle", variable=self.is_ev,
                      font="Arial 12").grid(row=8, column=0)
        tk.Checkbutton(self.root, text="Motorcycle", variable=self.is_motorcycle,
                      font="Arial 12").grid(row=8, column=1)

        # Action buttons
        tk.Button(self.root, text="Park Vehicle", command=self._park_vehicle,
                 font="Arial 12", bg="lightblue").grid(row=9, column=0, pady=5)
        
        tk.Label(self.root, text="Space ID:", font="Arial 12").grid(row=10, column=0)
        tk.Entry(self.root, textvariable=self.space_id, width=6, font="Arial 12").grid(row=10, column=1)
        
        tk.Button(self.root, text="Remove Vehicle", command=self._remove_vehicle,
                 font="Arial 12", bg="lightblue").grid(row=11, column=0, pady=5)

        # Status buttons
        tk.Button(self.root, text="Show Status", command=self._show_status,
                 font="Arial 12", bg="PaleGreen1").grid(row=12, column=0, pady=5)
        tk.Button(self.root, text="Show EV Status", command=self._show_ev_status,
                 font="Arial 12", bg="PaleGreen1").grid(row=12, column=1, pady=5)

        # Output area
        self.output_area.grid(row=13, column=0, columnspan=4, padx=10, pady=10)

    def _create_header(self, text: str, row: int):
        """Create a section header"""
        tk.Label(self.root, text=text, font="Arial 14 bold").grid(
            row=row, column=0, columnspan=4, pady=10)

    def _create_lot(self):
        """Handle lot creation"""
        try:
            regular = int(self.regular_spaces.get())
            ev = int(self.ev_spaces.get())
            level = int(self.level.get())
            
            self.controller.initialize_lot(regular, ev, level)
            self._show_message(f"Created parking lot with {regular} regular and {ev} EV spaces on level {level}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def _park_vehicle(self):
        """Handle vehicle parking"""
        info = VehicleInfo(
            self.registration.get(),
            self.make.get(),
            self.model.get(),
            self.color.get()
        )
        
        space_id = self.controller.park_vehicle(
            info, 
            self.is_ev.get(),
            self.is_motorcycle.get()
        )
        
        if space_id:
            self._show_message(f"Vehicle parked in space {space_id}")
        else:
            self._show_message("No available spaces")

    def _remove_vehicle(self):
        """Handle vehicle removal"""
        try:
            space_id = int(self.space_id.get())
            is_ev = self.is_ev.get()
            
            if self.controller.remove_vehicle(space_id, is_ev):
                self._show_message(f"Vehicle removed from space {space_id}")
            else:
                self._show_message(f"No vehicle in space {space_id}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid space ID")

    def _show_status(self):
        """Display current parking lot status"""
        status = self.controller.get_lot_status()
        
        output = "Regular Vehicles:\n"
        output += "Space\tRegistration\tMake\tModel\tColor\n"
        for space_id, vehicle in status['regular']:
            output += f"{space_id}\t{vehicle.registration}\t{vehicle.make}\t{vehicle.model}\t{vehicle.color}\n"
        
        output += "\nElectric Vehicles:\n"
        output += "Space\tRegistration\tMake\tModel\tColor\n"
        for space_id, vehicle in status['ev']:
            output += f"{space_id}\t{vehicle.registration}\t{vehicle.make}\t{vehicle.model}\t{vehicle.color}\n"
        
        self._show_message(output)

    def _show_ev_status(self):
        """Display EV charging status"""
        status = self.controller.get_ev_charge_status()
        
        output = "EV Charging Status:\n"
        output += "Space\tCharge Level\n"
        for space_id, charge in status:
            output += f"{space_id}\t{charge}%\n"
        
        self._show_message(output)

    def _show_message(self, message: str):
        """Display a message in the output area"""
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, message)

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    app = ParkingLotView()
    app.run()

if __name__ == "__main__":
    main()