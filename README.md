# Campus Student Club System

A CS112 final project by   **Basmah Fallatah**. This Python application manages club events and student registrations through a terminal menu, with a Tkinter thank-you window on exit.

## Features

- Add events with a title, free-text date and positive initial capacity.
- Enroll regular students and club managers.
- Register and cancel event attendance; track remaining seats.
- Enforce registration limits through the menu: 3 events for regular students, 6 for managers.
- View events, individual student activity and registration/cancellation history.
- Load local text data on startup and save when choosing **8. Exit**.
- Demonstrate classes, encapsulation, inheritance and method overriding.

## Requirements and running

Use Python 3 with Tkinter and a desktop display. The reviewed copy was checked with Python **3.12.14 on Windows**. No third-party Python packages are needed.

1. Download or clone the repository and open a terminal in its folder.
2. Check Tkinter: `python -m tkinter` (a small window should open; close it).
3. Start: `python club_system.py` (use `python3` if that is your Python command).
4. Choose menu options 1–8. Choose **8** to save, then close the thank-you window using **Exit Application**.

If Python is not found, install/configure Python first. If Tkinter is unavailable, install the Tk support supplied for your Python distribution or operating system. A terminal-only server without a display cannot show the exit window.

### Example workflow

Choose **1** and enter `Python Workshop`, `2026-12-01`, capacity `5`. Choose **2**, enter `Demo Student`, ID `DEMO-001`, type `1`. Choose **3** with that ID and the exact event title. Use **5**, **6** and **7** to inspect results, **4** to cancel, and **8** to save and exit. Use invented data for public demonstrations.

## Local data and privacy

`club_data.txt` is read/written in the **terminal's current working directory**. Run from this repository folder to keep the location predictable. It is created on saving and excluded by `.gitignore`; the original student data is not distributed.

The plain-text records are `E|title|date|remaining_capacity`, `S|R-or-M|name|student_id|comma-separated-event-titles`, and `L|transaction`. Names, IDs and activity are stored without encryption. There is no login or role authorization; manager status is chosen during enrollment. Avoid real personal data in shared copies. Ignore rules do not protect files already tracked or manually uploaded.

## Known limitations

This is an educational project with confirmed defects retained from the original:

- A duplicate registration through the menu can reduce the remaining capacity before being rejected.
- An event saved with zero remaining seats cannot be reloaded: the constructor rejects zero, loading stops, and later records are skipped. Earlier records may remain loaded; saving afterwards can overwrite data incompletely.
- `Event.set_capacity()` assigns the wrong attribute and does not update the capacity.
- Duplicate IDs/event titles are allowed; lookups use the first match. Dates are not validated. `|`, commas and line breaks in inputs can corrupt the text format.
- Registration limits are checked by the menu, not by `Student.register()` itself. Loading data does not enforce those limits.
- Save/load errors are generic, saving is not atomic, and abrupt termination does not save changes. The quit window is required by the current exit path.

Back up local data before experimenting. See [REVIEW_AR.md](REVIEW_AR.md) for review scope and [VALIDATION.txt](VALIDATION.txt) for actual executed checks. No claim is made that all inputs or the desktop window were tested.

## Authorship and publication changes

Original authors:  **Basmah  (بسمة)**, as credited in the source. No individual division of contributions is asserted.

Publication preparation renamed `CS112 Project.py` to `club_system.py`, removed the authors' student IDs from the thank-you message, omitted the original saved student records, and added documentation and ignore rules. Source logic is otherwise unchanged; UTF-8 text and line endings were normalized. The exit message still credits both authors. No open-source license has been added because the authors have not selected one.
