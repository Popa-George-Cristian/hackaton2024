import customtkinter as ctk
from db import connect_to_db

class InterfaceAdmin():
    def __init__(self, window, switch_page_callback):
        self.window = window
        self.switch_page_callback = switch_page_callback
        self.mainFrame = None
        self.db = connect_to_db()
        self.initPanel()
        
    def initPanel(self):
        self.mainPanel = ctk.CTkFrame(self.window, fg_color='#2586d5', corner_radius=0)
        self.mainPanel.pack(fill='both', expand=True)

        # Configure the grid to have two columns, one for the label and one for the entry
        self.mainPanel.grid_rowconfigure(0, weight=1)
        self.mainPanel.grid_rowconfigure(1, weight=1)
        self.mainPanel.grid_columnconfigure(0, weight=1)
        self.mainPanel.grid_columnconfigure(1, weight=2)

        # Creating and packing the student name label and entry
        self.studentNameLabel = ctk.CTkLabel(self.mainPanel, text="Student:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentNameLabel.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        self.studentNameEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentNameEntry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)

        # Creating and packing the faculty label and entry
        self.studentCollegueLabel = ctk.CTkLabel(self.mainPanel, text="Facultatea:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentCollegueLabel.grid(row=1, column=0, sticky='w', padx=10, pady=5)

        self.studentCollegueEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentCollegueEntry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)

        # Creating and packing the year label and entry
        self.studentYearLabel = ctk.CTkLabel(self.mainPanel, text="Anul:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentYearLabel.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        self.studentYearEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentYearEntry.grid(row=2, column=1, sticky='ew', padx=10, pady=5)

        # Creating and packing the specialization label and entry
        self.studentDegreeLabel = ctk.CTkLabel(self.mainPanel, text="Grad academic:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentDegreeLabel.grid(row=3, column=0, sticky='w', padx=10, pady=5)

        self.studentDegreeEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentDegreeEntry.grid(row=3, column=1, sticky='ew', padx=10, pady=5)

        # Creating and packing the degree label and entry
        self.studentSpecializationLabel = ctk.CTkLabel(self.mainPanel, text="Specializare:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentSpecializationLabel.grid(row=4, column=0, sticky='w', padx=10, pady=5)

        self.studentSpecializationEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentSpecializationEntry.grid(row=4, column=1, sticky='ew', padx=10, pady=5)

        # Creating and packing the image label and entry
        self.studentImageLabel = ctk.CTkLabel(self.mainPanel, text="Introduceti calea de imagine:", font=("Arial", 16), anchor="w", text_color='white')
        self.studentImageLabel.grid(row=5, column=0, sticky='w', padx=10, pady=5)

        self.studentImageEntry = ctk.CTkEntry(self.mainPanel, font=("Arial", 16), border_color='black', corner_radius=0)
        self.studentImageEntry.grid(row=5, column=1, sticky='ew', padx=10, pady=5)

        # Add Student Button
        self.addStudentButton = ctk.CTkButton(self.mainPanel, text="Adaugare Student", font=("Arial", 16), command=self.addStudent, fg_color='white', hover_color='white', text_color='black')
        self.addStudentButton.grid(row=6, column=0, pady=10)
        
        self.logoutButton = ctk.CTkButton(self.mainPanel, text="Logout", font=("Arial", 16), command=self.handleLogout, fg_color='white', hover_color='white', text_color='black')
        self.logoutButton.grid(row=6, column=1, pady=10)
        
    def handleLogout(self):
        self.switchToMonitor()

    def switchToMonitor(self):
        self.switch_page_callback(0)
        
    def addStudent(self):
        # Here, you can gather all the input data and process it as needed
        student_name = self.studentNameEntry.get()
        student_college = self.studentCollegueEntry.get()
        student_year = self.studentYearEntry.get()
        student_degree = self.studentDegreeEntry.get()
        student_specialization = self.studentSpecializationEntry.get()
        student_image_path = self.studentImageEntry.get()

        # You can then handle this data by saving it to the database or performing any action
        print(f"Student Info: {student_name}, {student_college}, {student_year}, {student_specialization}, {student_degree}, {student_image_path}")
        
        if self.db is not None:
            cursor = self.db.cursor()

            # SQL Insert query to add student data
            query = """
            INSERT INTO students (nume_student, facultatea, an, grad, specializare, imagine)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            # Execute the query with the values from the entry fields
            cursor.execute(query, (student_name, student_college, student_year, student_degree, student_specialization, student_image_path))
            
            # Commit the changes to the database
            self.db.commit()
            print("Student data inserted successfully.")
            
            # Close the cursor
            cursor.close()
        else:
            print("Failed to connect to the database.")

