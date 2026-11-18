import os

class Event:
    def __init__(self, title, date, capacity):
        # تغليف البيانات باستخدام سمات خاصة لمنع التعديل المباشر
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        self.__title = title
        self.__date = date
        self.__capacity = capacity

    def get_title(self):
        return self.__title
    def get_date(self):
        return self.__date
    def get_capacity(self):
        return self.__capacity

    def set_title(self, title):
        self.__title = title
    def set_date(self, date):
        self.__date = date
    def set_capacity(self, capacity):
        self.__set_capacity = capacity

    def decrease_capacity(self):
        # تقليل السعة بمقدار 1 عند التسجيل
        if self.__capacity <= 0:
            raise ValueError("Event is full.")
        self.__capacity -= 1

    def increase_capacity(self):
        # استعادة السعة عند إلغاء التسجيل
        self.__capacity += 1

    def __str__(self):
        return f"Title: {self.__title} | Date: {self.__date} | Capacity: {self.__capacity}"

class Student:
    def __init__(self, name, student_id):
        self.__name = name
        self.__student_id = student_id
        self.__registered_events = []  # قائمة بأسماء الفعاليات

    def get_name(self):
        return self.__name
    def get_student_id(self):
        return self.__student_id
    def get_registered_events(self):
        return self.__registered_events

    def set_name(self, name):
        self.__name = name
    def set_student_id(self, student_id):
        if not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        self.__student_id = student_id
    def set_registered_events(self, registered_events):
        self.__registered_events = registered_events

    def can_register(self):
        # الطالب العادي يسجل في 3 فعاليات كحد أقصى
        if len(self.__registered_events) >= 3:
            raise ValueError("Registration limit reached.")

    def register(self, event_title):
        if event_title in self.__registered_events:
            raise ValueError("Already registered in this event.")
        self.__registered_events.append(event_title)

    def cancel(self, event_title):
        if event_title in self.__registered_events:
            self.__registered_events.remove(event_title)
            return True
        return False

    def __str__(self):
        return f"{self.__name} ({self.__student_id}) | Registered Events: {self.__registered_events}"


# --- Phase 3 ---
class ClubManager(Student):  # الوراثة من كلاس Student
    def can_register(self):
        # تخطي الدالة (Overriding): المدير يسجل في 6 فعاليات
        if len(self.get_registered_events()) >= 6:
            raise ValueError("Registration limit reached.")

    def __str__(self):
        # إظهار المسمى الوظيفي "Club Manager"
        return f"{self.get_name()} | Club Manager | {self.get_student_id()}"


# --- Phase 2 & 3 ---
class Club:
    def __init__(self, club_name):
        self.__club_name = club_name
        self.__students = []  # قائمة كائنات الطلاب
        self.__events = []    # قائمة كائنات الفعاليات
        self.__transactions = []  # سجل العمليات للمرحلة الثانية

    def get_club_name(self):
        return self.__club_name
    def get_students(self):
        return self.__students
    def get_events(self):
        return self.__events
    def get_transactions(self):
        return self.__transactions

    def set_club_name(self, club_name):
        self.__club_name = club_name
    def set_students(self, students):
        self.__students = students
    def set_events(self, events):
        self.__events = events
    def set_transactions(self, transactions):
        self.__transactions = transactions

    def add_event(self, event_obj):
        self.__events.append(event_obj)

    def enroll_student(self, student_obj):
        self.__students.append(student_obj)

    def save_data(self):
        # حفظ البيانات في ملف نصي عند الخروج
        try:
            with open("club_data.txt", "w", encoding="utf-8") as f:
                for e in self.__events:
                    f.write(f"E|{e.get_title()}|{e.get_date()}|{e.get_capacity()}\n")
                for s in self.__students:
                    stype = "M" if isinstance(s, ClubManager) else "R"
                    evs = ",".join(s.get_registered_events())
                    f.write(f"S|{stype}|{s.get_name()}|{s.get_student_id()}|{evs}\n")
                for t in self.__transactions:
                    f.write(f"L|{t}\n")
            print("Data saved successfully.")
        except Exception :
            print("Error saving data:")

    def load_data(self):
        # تحميل البيانات تلقائياً ومعالجة حالة عدم وجود ملف
        if not os.path.exists("club_data.txt"):
            print("No saved data found. Starting fresh.")
            return
        try:
            with open("club_data.txt", "r", encoding="utf-8") as f:
                for line in f:
                    p = line.strip().split("|")
                    if p[0] == "E":
                        self.add_event(Event(p[1], p[2], int(p[3])))
                    elif p[0] == "S":
                        s = ClubManager(p[2], p[3]) if p[1] == "M" else Student(p[2], p[3])
                        if p[4]:
                            for ev in p[4].split(","): s.register(ev)
                        self.enroll_student(s)
                    elif p[0] == "L":
                        self.__transactions.append(p[1])
            print("Data loaded successfully.")
        except Exception:
            print("Error loading saved data.")


import tkinter as tk
from tkinter import font

def show_thank_you_gui():
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("System Shutdown - Thank You")
    root.geometry("500x450")
    root.configure(bg="#f0f0f0")
    # تحديد الخطوط
    title_font = font.Font(family="Helvetica", size=14, weight="bold")
    text_font = font.Font(family="Helvetica", size=10)
    dev_font = font.Font(family="Courier", size=11, weight="bold")
    quote_font = font.Font(family="Helvetica", size=10, slant="italic")
    # إطار داخلي للتنظيم
    frame = tk.Frame(root, bg="white", bd=2, relief="groove", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    # محتوى الرسالة
    tk.Label(frame, text="🚀 CAMPUS STUDENT CLUB SYSTEM 🚀", font=title_font, fg="#2c3e50", bg="white").pack(pady=10)
    tk.Label(frame, text="Developed by the visionary programmers:", font=text_font, bg="white").pack()
    # أسماء المبرمجين
    devs_text = "✨ Hajar Algedeei \n✨ Basmah Fallatah"
    tk.Label(frame, text=devs_text, font=dev_font, fg="#2980b9", bg="white", justify="left").pack(pady=10)
    # الملاحظات التقنية
    notes = (
        "🛠️ Built with passion and logic.\n"
        "🛡️ Implements OOP principles, Inheritance,\n"
        "and Data Persistence."
    )
    tk.Label(frame, text=notes, font=text_font, bg="white", justify="center").pack(pady=5)
    quote = '"Code is like humor. When you have to explain it, it\'s bad."'
    tk.Label(frame, text=quote, font=quote_font, fg="#7f8c8d", bg="white", wraplength=400).pack(pady=15)
    # زر الإغلاق النهائي
    tk.Button(frame, text="Exit Application", command=root.destroy, bg="#e74c3c", fg="white",
              font=("Helvetica", 10, "bold"), padx=10, pady=5).pack(pady=10)
    # جعل النافذة تظهر في المقدمة وتعطيل التفاعل مع البرنامج الأصلي حتى تُغلق
    root.attributes('-topmost', True)
    root.mainloop()


def main():
    my_club = Club("AI Club")
    my_club.load_data()

    while True:
        # القائمة النهائية للمرحلة الثالثة
        print("\n=== Campus Student Club System ===")
        print("1. Add Event\n2. Enroll Student\n3. Register Student for Event\n4. Cancel Registration")
        print("5. View All Events\n6. View Student Activity\n7. View Transaction History\n8. Exit")

        try:
            # معالجة الأخطاء للمدخلات غير الرقمية
            choice = input("Enter choice: ")
            c = int(choice)
            if not (1 <= c <= 8):
                print("Error: Choice out of range. Please enter 1-8.")
                continue

            if c == 1:
                while True:
                    t = input("Enter title: ").strip()  # استخدام strip لإزالة المسافات الزائدة
                    if not t:
                        print("Error: Event title cannot be empty.")
                        continue
                    break

                d = input("Enter date: ")
                while True:
                    try:
                        cap = int(input("Enter capacity: "))
                        my_club.add_event(Event(t, d, cap))
                        print("Event added.")
                        break
                    except ValueError :
                        print("Error: Capacity must be greater than 0.")

            elif c == 2:
                while True:
                    try:
                        n = input("Enter name: ")
                        if not n.strip():
                            raise ValueError("Student name cannot be empty.")
                        i = input("Enter ID: ")
                        if not i.strip():
                            raise ValueError("Student ID cannot be empty.")
                        t = input("Type (1:Regular, 2:Manager): ")
                        if t not in ("1", "2"):
                            raise ValueError("Invalid type. Please enter 1 or 2.")
                        s = ClubManager(n, i) if t == "2" else Student(n, i)
                        my_club.enroll_student(s)
                        print(f"{s.get_name()} enrolled successfully.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}")


            elif c == 3:  # تسجيل الطالب في فعالية
                sid = input("Enter student ID: ")
                et = input("Enter event title: ")
                # البحث عن الطالب والفعالية
                std = next((s for s in my_club.get_students()
                            if s.get_student_id() == sid), None)
                evt = next((e for e in my_club.get_events()
                            if e.get_title() == et), None)
                if std and evt:
                    try:
                        # 1. التحقق من السعة قبل أي شيء
                        if evt.get_capacity() <= 0:
                            print("Error: Event is full. No more registrations allowed.")
                        else:
                            # 2. التحقق من قيود تسجيل الطالب
                            std.can_register()
                            # 3. خصم المقعد وإتمام التسجيل
                            evt.decrease_capacity()
                            std.register(et)
                            msg = f"{std.get_name()} registered for: {et}"
                            my_club.get_transactions().append(msg)
                            print("Registered successfully.")
                    except ValueError :
                        # هنا سيتم التقاط أي خطأ (مثل وصول الطالب للحد الأقصى)
                        print("Error")
                else:
                    print("Error: Student or Event not found.")

            elif c == 4:  # منطق إلغاء التسجيل (Phase 2)
                sid = input("Enter student ID: ")
                et = input("Enter event title: ")

                # البحث عن الطالب والفعالية
                std = next((s for s in my_club.get_students() if s.get_student_id() == sid), None)
                evt = next((e for e in my_club.get_events() if e.get_title() == et), None)

                # التأكد من وجود الطالب وإتمام عملية الإلغاء من قائمته
                if std and std.cancel(et):
                    if evt:
                        evt.increase_capacity()  # استعادة مقعد في الفعالية

                    # تسجيل العملية في السجل (Phase 2 Requirements)
                    msg = f"{std.get_name()} cancelled: {et}"
                    my_club.get_transactions().append(msg)
                    print(f"Success: {msg}")
                else:
                    print("Error: Registration not found for this student.")

            elif c == 5:  # عرض كافة الفعاليات (Phase 2 & 3)
                print("\n" + "-" * 10 + " All Events " + "-" * 10)
                # التأكد أولاً إذا كانت القائمة تحتوي على فعاليات
                if not my_club.get_events():
                    print("No events added yet.")
                else:
                    # المرور على كل كائن فعالية وطباعته باستخدام دالة __str__
                    for event in my_club.get_events():
                        print(event)

            elif c == 6:  # عرض نشاط طالب محدد (Phase 3)
                sid = input("Enter student ID: ")
                # البحث عن الطالب باستخدام الرقم الجامعي
                std = next((s for s in my_club.get_students() if s.get_student_id() == sid), None)

                if std:
                    print(f"\n{std}")  # يطبع الاسم والآيدي والنوع (مدير أو عادي)
                    print("Registered Events:", std.get_registered_events())
                else:
                    print("Error: Student not found.")

            elif c == 7:  # عرض سجل العمليات
                print("\n--- Transaction History ---")
                for idx, log in enumerate(my_club.get_transactions(), 1):
                    print(f"{idx}. {log}")

            elif c == 8:
                my_club.save_data()
                print("Closing system...")
                # استدعاء دالة الـ GUI التي أضفناها بالأعلى
                show_thank_you_gui()
                print("Goodbye!")
                break

        except ValueError:
            print("Error: Please enter a valid number.")


if __name__ == "__main__":
    main()


