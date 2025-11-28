import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import shutil
import argparse
from pathlib import Path


class GUI:
    def __init__(self, cfg_loc, bak_loc, bak2_loc) -> None:
        # key file locations - absolute paths
        self.CFG_LOCATION = cfg_loc
        self.BACKUP_LOCATION = bak_loc
        self.BACKUP_BACKUP_LOCATION = bak2_loc

        # used to flip between the keypad screen and the custom event
        # name screen
        self.use_custom_event_name = False

        self.__window = tk.Tk()
        self.__window.title("SLUGScan Setup")

        self.__lan_number = tk.StringVar()
        self.__num_input_frame = self.__create_num_input_frame()
        self.__num_input_frame.pack(padx=10, pady=10)

        self.__event_name = tk.StringVar()
        self.__custom_event_frame = ttk.Frame(self.__window)
        self.__custom_event_frame = self.__create_custom_event_frame()

        self.__window.protocol("WM_DELETE_WINDOW", self.__window.destroy)

        self.__window.mainloop()

    def __create_num_input_frame(self) -> ttk.Frame:
        frame = ttk.Frame(self.__window)

        self.__ask_lan_number_label = ttk.Label(
            master=frame,
            text="Please enter the LAN number via the keypad:",
        )
        self.__ask_lan_number_label.pack(padx=5, pady=5)

        self.__lan_number_box = ttk.Entry(
            master=frame,
            textvariable=self.__lan_number,
            state=tk.DISABLED,
        )
        self.__lan_number_box.pack(padx=5, pady=5)

        self.__keypad_frame = ttk.Frame(master=frame)
        self.__one_button = ttk.Button(
            master=self.__keypad_frame, text="1", command=lambda: self.__add_number(1)
        )
        self.__one_button.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=15)
        self.__two_button = ttk.Button(
            master=self.__keypad_frame, text="2", command=lambda: self.__add_number(2)
        )
        self.__two_button.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=15)
        self.__three_button = ttk.Button(
            master=self.__keypad_frame, text="3", command=lambda: self.__add_number(3)
        )
        self.__three_button.grid(column=2, row=0, padx=5, pady=5, ipadx=5, ipady=15)
        self.__four_button = ttk.Button(
            master=self.__keypad_frame, text="4", command=lambda: self.__add_number(4)
        )
        self.__four_button.grid(column=0, row=1, padx=5, pady=5, ipadx=5, ipady=15)
        self.__five_button = ttk.Button(
            master=self.__keypad_frame, text="5", command=lambda: self.__add_number(5)
        )
        self.__five_button.grid(column=1, row=1, padx=5, pady=5, ipadx=5, ipady=15)
        self.__six_button = ttk.Button(
            master=self.__keypad_frame, text="6", command=lambda: self.__add_number(6)
        )
        self.__six_button.grid(column=2, row=1, padx=5, pady=5, ipadx=5, ipady=15)
        self.__seven_button = ttk.Button(
            master=self.__keypad_frame, text="7", command=lambda: self.__add_number(7)
        )
        self.__seven_button.grid(column=0, row=2, padx=5, pady=5, ipadx=5, ipady=15)
        self.__eight_button = ttk.Button(
            master=self.__keypad_frame, text="8", command=lambda: self.__add_number(8)
        )
        self.__eight_button.grid(column=1, row=2, padx=5, pady=5, ipadx=5, ipady=15)
        self.__nine_button = ttk.Button(
            master=self.__keypad_frame, text="9", command=lambda: self.__add_number(9)
        )
        self.__nine_button.grid(column=2, row=2, padx=5, pady=5, ipadx=5, ipady=15)
        self.__zero_button = ttk.Button(
            master=self.__keypad_frame, text="0", command=lambda: self.__add_number(0)
        )

        self.__backspace_button = ttk.Button(
            master=self.__keypad_frame, text="\u232b", command=self.__remove_char
        )
        self.__backspace_button.grid(column=0, row=3, padx=5, pady=5, ipadx=5, ipady=15)

        self.__zero_button.grid(column=1, row=3, padx=5, pady=5, ipadx=5, ipady=15)

        self.__confirm_button = ttk.Button(
            master=self.__keypad_frame, text="\u2713", command=self.__write_file
        )
        self.__confirm_button.grid(column=2, row=3, padx=5, pady=5, ipadx=5, ipady=15)

        self.__custom_event_button = ttk.Button(
            master=self.__keypad_frame,
            text="Custom event name",
            command=self.__toggle_custom_event_name,
        )
        self.__custom_event_button.grid(
            column=0, row=4, padx=5, pady=5, ipadx=10, ipady=5, columnspan=3
        )

        self.__keypad_frame.pack()

        return frame

    def __create_custom_event_frame(self) -> ttk.Frame:
        frame = ttk.Frame(self.__window)

        self.__on_screen_kb_label = ttk.Label(
            master=frame, text="The on-screen-keyboard is required for this menu."
        )
        self.__on_screen_kb_label.pack(padx=5, pady=5)

        self.__ask_lan_number_label = ttk.Label(
            master=frame, text="Please enter the LAN number:"
        )
        self.__ask_lan_number_label.pack(padx=5, pady=5)

        self.__lan_number_box = ttk.Entry(master=frame, textvariable=self.__lan_number)
        self.__lan_number_box.pack(padx=5, pady=5)

        self.__ask_event_name_label = ttk.Label(
            master=frame, text="Please enter the event name:"
        )
        self.__ask_event_name_label.pack(padx=5, pady=5)
        self.__event_name_box = ttk.Entry(master=frame, textvariable=self.__event_name)
        # enter to search
        self.__event_name_box.bind("<Return>", self.__write_file)
        self.__event_name_box.pack(padx=5, pady=5)

        self.__submit_button = ttk.Button(
            master=frame, text="Submit", command=self.__write_file
        )
        self.__submit_button.pack(padx=5, pady=5)

        self.__keypad_button = ttk.Button(
            master=frame, text="Back to keypad", command=self.__toggle_custom_event_name
        )
        self.__keypad_button.pack(padx=5, pady=5)

        return frame

    def __toggle_custom_event_name(self) -> None:
        self.use_custom_event_name = not self.use_custom_event_name
        if self.use_custom_event_name:
            self.__num_input_frame.forget()
            self.__custom_event_frame.pack(padx=10, pady=10)
        else:
            self.__custom_event_frame.forget()
            self.__num_input_frame.pack(padx=10, pady=10)

    def __add_number(self, num: int) -> None:
        self.__lan_number.set(self.__lan_number.get() + str(num))

    def __remove_char(self) -> None:
        self.__lan_number.set(self.__lan_number.get()[:-1])

    def __validate_int(self) -> bool:
        try:
            int(self.__lan_number.get())
            return True
        except ValueError:
            messagebox.showerror(
                "Invalid LAN number", "Please enter a valid integer for the LAN number."
            )
            return False

    # We ignore any additional parameters as they can only be generated
    # from someone hitting return on the custom event name screen
    def __write_file(self, *a) -> None:
        if os.path.exists(self.BACKUP_LOCATION):
            try:
                shutil.copy(self.BACKUP_LOCATION, self.BACKUP_BACKUP_LOCATION)
            except Exception as ex:
                messagebox.showerror(
                    "File copy failed",
                    "Failed to make a copy of the backup slugscan.cfg file. Exception: {0}".format(
                        repr(ex)
                    ),
                )
        if os.path.exists(self.CFG_LOCATION):
            try:
                shutil.copy(self.CFG_LOCATION, self.BACKUP_LOCATION)
            except Exception as ex:
                messagebox.showerror(
                    "File copy failed",
                    "Failed to make a copy of the slugscan.cfg file. Exception: {0}".format(
                        repr(ex)
                    ),
                )
        else:
            os.makedirs(os.path.dirname(self.CFG_LOCATION))

        with open(self.CFG_LOCATION, "w", encoding="utf-8") as file:
            file.write("[Session]\n")
            if self.use_custom_event_name:
                file.write("event = {name}\n".format(name=self.__event_name.get()))
            else:
                file.write("event = LAN {num}\n".format(num=self.__lan_number.get()))
            file.write("eventnum = {num}\n\n".format(num=self.__lan_number.get()))

            file.write("[MySQL]\n")
            file.write("username = user\n")
            file.write("password = pass\n")
            file.write("host = ip\n")
            file.write("db = db\n")

        # TODO: change message to give instructions for launching the scanner?
        messagebox.showinfo(
            "File written successfully",
            "Config file has been written successfully.",
        )
        # else:
        #     messagebox.showinfo(
        #         "Config file doesn't exist.",
        #         "Config file has been written successfully.",
        #     )
        quit()


# Helper function defines the CLI arguments and parses them too
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("{fn}".format(fn=os.path.basename(__file__)))
    parser.add_argument(
        "-c",
        "--cfg_location",
        help="Absolute location of the slugscan.cfg config file.",
        type=str,
    )
    parser.add_argument(
        "-b",
        "--backup_location",
        help="Absolute location of the slugscan.cfg.backup config file.",
        type=str,
    )
    parser.add_argument(
        "-b2",
        "--backup_2_location",
        help="Absolute location of the slugscan.cfg.backup.backup config file.",
        type=str,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    cfg_location = "~/slugscan/db/slugscan.cfg"
    backup_location = "~/slugscan/db/slugscan.cfg.backup"
    backup_2_location = "~/slugscan/db/slugscan.cfg.backup.backup"

    if args.cfg_location is not None:
        cfg_location = args.cfg_location
    if args.backup_location is not None:
        backup_location = args.backup_location
    if args.backup_2_location is not None:
        backup_2_location = args.backup_2_location

    gui = GUI(
        str(Path(cfg_location).expanduser()),
        str(Path(backup_location).expanduser()),
        str(Path(backup_2_location).expanduser())
    )
