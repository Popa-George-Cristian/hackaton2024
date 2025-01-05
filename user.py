import customtkinter as ctk
import cv2
from PIL import Image
from db import connect_to_db
import camera, time

class InterfaceMonitor():
    def __init__(self, window, switch_page_callback):
        self.window = window
        self.switch_page_callback = switch_page_callback
        self.status_code = 0
        self.camera = camera.Camera()
        self.db = connect_to_db()

        self.schedule_data = None  # Initialize schedule_data here
        self.mainFrame = None
        self.initLayout()
        self.initializeCamera()
        
    def mainInfo(self):
        self.mainInfo = ctk.CTkFrame(self.window, fg_color='white', corner_radius=0, width=475, border_color="#475a69", border_width=1)
        self.mainInfo.pack(side='left', fill='both')
        self.mainInfo.pack_propagate(0)

    def handleLogout(self):
        self.switchToMonitor()

    def switchToMonitor(self):
        self.switch_page_callback(0)
        # self.camera.release_pi()
        self.camera.release_cv()
        
    def mainCamera(self):
        self.mainCamera = ctk.CTkFrame(self.window, fg_color='#475a69', corner_radius=0, width=10, height=300)
        self.mainCamera.pack(fill='both', side='top')
        self.mainCamera.pack_propagate(0)
    
        self.camera_label = ctk.CTkLabel(self.mainCamera, text=None)
        self.camera_label.pack(fill='both', expand=True)
        
    def mainDebug(self):
        self.mainDebug = ctk.CTkFrame(self.window, fg_color='white', corner_radius=0, border_width=1, border_color='#475a69')
        self.mainDebug.pack(side='bottom', fill='both', expand=True)

        self.buttonAuthorization = ctk.CTkButton(self.mainDebug, text='Authorization', command=self.allowStudent, width=200, height=25, corner_radius=0)
        self.buttonAuthorization.pack(side='top', pady=2)

        self.buttonDeny = ctk.CTkButton(self.mainDebug, text='Deny', command=self.denyStudent, width=200, height=25, corner_radius=0)
        self.buttonDeny.pack(side='top', pady=2)

        self.buttonStudentInfo = ctk.CTkButton(self.mainDebug, text='Open Student Info', command=self.invokeInfo, width=200, height=25, corner_radius=0)
        self.buttonStudentInfo.pack(side='top', pady=2)

        self.buttonSchedule = ctk.CTkButton(self.mainDebug, text='Open Schedule', command=self.invokeSchedule, width=200, height=25, corner_radius=0)
        self.buttonSchedule.pack(side='top', pady=2)

        self.buttonLogout = ctk.CTkButton(self.mainDebug, text='Logout', command=self.handleLogout, width=200, height=25, corner_radius=0)
        self.buttonLogout.pack(side='top', pady=2)
    
    def invokeSchedule(self):
        if hasattr(self, "mainSchedule") and self.mainSchedule.winfo_exists():
            self.destroySchedule()
        else:
            self.createSchedule()
    
    def createSchedule(self):
        self.mainSchedule = ctk.CTkFrame(self.mainInfo, fg_color='blue')
        self.mainSchedule.pack(fill='x', pady=10, padx=10)

        # Header Row
        self.scheduleDay = ctk.CTkLabel(self.mainSchedule, text='Luni', text_color='white', font=("Arial", 14))
        self.scheduleDay.grid(row=0, column=0, rowspan=5, padx=10, pady=5, sticky="n")  # Align to top-center

        self.scheduleHourHeader = ctk.CTkLabel(self.mainSchedule, text='Ora', text_color='white', font=("Arial", 14))
        self.scheduleHourHeader.grid(row=0, column=1, padx=10, pady=5)

        self.scheduleSpecializationHeader1 = ctk.CTkLabel(self.mainSchedule, text='AIA-2221A', text_color='white', font=("Arial", 14))
        self.scheduleSpecializationHeader1.grid(row=0, column=2, padx=10, pady=5)

        if self.schedule_data:
            if 'Joi' in self.schedule_data:
                schedule_day = self.schedule_data['Joi']
                
                for i, entry in enumerate(schedule_day, start=1):
                    hour = entry.get('ora', 'No hour')  # Default to 'No hour' if 'ora' is missing
                    specialization = entry.get('materia', 'No specialization')  # Default to 'No specialization' if missing
                    
                    hour_label = ctk.CTkLabel(self.mainSchedule, text=hour, text_color='white')
                    hour_label.grid(row=i, column=1, padx=10, pady=5, sticky="e")

                    specialization_label = ctk.CTkLabel(self.mainSchedule, text=specialization, text_color='white')
                    specialization_label.grid(row=i, column=2, padx=10, pady=5)
            else:
                # Handle case when no schedule data is available for 'Joi'
                no_schedule_label = ctk.CTkLabel(self.mainSchedule, text="No schedule available", text_color='red')
                no_schedule_label.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
        else:
            # Handle case when schedule_data is None or empty
            no_schedule_label = ctk.CTkLabel(self.mainSchedule, text="No schedule available", text_color='red')
            no_schedule_label.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")

    
    def destroySchedule(self):
        """Destroy the mainStudent section."""
        if hasattr(self, "mainSchedule") and self.mainSchedule.winfo_exists():
            self.mainSchedule.destroy()  

    def denyStudent(self):
        self.status_code = 0
        self.camera.update_status(self.status_code)
        
    def allowStudent(self):
        self.status_code = 1
        self.camera.update_status(self.status_code)
        
    def invokeInfo(self):
        """Toggle the creation and destruction of the mainStudent section."""
        if hasattr(self, "mainStudent") and self.mainStudent.winfo_exists():
            self.destroyInfo()  # If already exists, destroy it
        else:
            self.createInfo()  # Otherwise, create it

    def fetchInfo(self):
        if self.db is not None:
            cursor = self.db.cursor()

            # Wait until a valid name is returned
            username = ""
            while username == "" or username == "Unknown":
                username = self.camera.returnName()
                if username == 'Florin':
                    username = 'Cercel Cristian Florin'
                elif username == 'Cristi':
                    username = 'Popa George Cristian'
                elif username == 'gabi':
                    username = 'Plugaru Gabriel'
                
                print(f"Detected: {username}")
                time.sleep(0.5)  # Add a small delay to avoid overloading the CPU

            query = """
            SELECT nume_student, facultatea, an, grad, specializare, imagine
            FROM informatii
            WHERE nume_student = %s
            """

            # Execute the query once a valid name is detected
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                student_name, student_college, student_year, student_degree, student_specialization, student_image_path = result
                self.getGroup(student_specialization)
                self.schedule_data = self.getGroup(student_specialization)
                return (student_name, student_college, student_year, student_degree, student_specialization, student_image_path)
            else:
                print(f"No student found with the name: {username}")
                return None

    def getGroup(self, group):
        schedule_aia = {
            "Joi": [
                {'ora': '08:00-09:50', 'grupa': 'AIA-2221-A', 'materia': 'CEL (L) Y606A M. Pavel'},
                {'ora': '10:00-11:50', 'grupa': 'AIA-2221-A', 'materia': 'IA II (L) Y505M. Tiplea'},
                {'ora': '12:00-13:50', 'grupa': 'AIA-2221-A', 'materia': ''},
                {'ora': '14:00-15:50', 'grupa': 'AIA-2221-A', 'materia': 'Limbaje de Asamblare (LA) (C) Y405 s.l. B. Codres'},
            ]
        }

        schedule_ietti = {
            "Joi": [
                {'ora': '08:00-09:50', 'grupa': 'IETII-2321-B', 'materia': ''},
                {'ora': '10:00-11:50', 'grupa': 'IETII-2321-B', 'materia': 'SO (L) G409 D.Voipan'},
                {'ora': '12:00-13:50', 'grupa': 'IETII-2321-B', 'materia': 'CID (L) Y605a S.l. L. Baicu'},
                {'ora': '14:00-15:50', 'grupa': 'IETII-2321-B', 'materia': ''},
            ]
        }

        # Compare group with predefined schedules
        if group == 'AIA-2221-A':
            self.schedule_data = schedule_aia
        elif group == 'IETII-2321-B':
            self.schedule_data = schedule_ietti
        print(self.schedule_data)
        return self.schedule_data


    def createInfo(self):
        """Create the mainStudent section and populate it with widgets."""
        self.mainStudent = ctk.CTkFrame(self.mainInfo, fg_color='#2586d5')
        self.mainStudent.pack(fill='x', pady=10, padx=10)
        
        # Fetch student data
        self.getDataStudent = self.fetchInfo()
        
        # Check if the student data is valid
        if self.getDataStudent:
            # If student data is valid, unpack the information
            student_name, student_college, student_year, student_degree, student_specialization, student_image_path = self.getDataStudent

            # Add student image (fallback image if no path available)
            if student_image_path:
                self.imageStudent_pil = Image.open(student_image_path)
            else:
                self.imageStudent_pil = Image.open('./images/default_image.jpg')  # Fallback image
            self.imageStudent = ctk.CTkImage(light_image=self.imageStudent_pil, dark_image=self.imageStudent_pil, size=(128, 128))
            self.imageLabel = ctk.CTkLabel(self.mainStudent, image=self.imageStudent, text='')
            self.imageLabel.pack(side='left', padx=10, pady=10)

            # Add student information
            self.studentName = ctk.CTkLabel(self.mainStudent, text=student_name, font=("Arial", 16), anchor="w", text_color='white')
            self.studentName.pack(fill='x')
            self.studentCollegue = ctk.CTkLabel(self.mainStudent, text=student_college, font=("Arial", 16), anchor="w", text_color='white')
            self.studentCollegue.pack(fill='x')
            self.studentYear = ctk.CTkLabel(self.mainStudent, text=student_year, font=("Arial", 16), anchor="w", text_color='white')
            self.studentYear.pack(fill='x')
            self.studentDegree = ctk.CTkLabel(self.mainStudent, text=student_degree, font=("Arial", 16), anchor="w", text_color='white')
            self.studentDegree.pack(fill='x')
            self.studentSpecialization = ctk.CTkLabel(self.mainStudent, text=student_specialization, font=("Arial", 16), anchor="w", text_color='white')
            self.studentSpecialization.pack(fill='x')
            
        else:
            # If no data was fetched, show an error message
            error_message = "Student data not found or face not recognized."
            self.errorLabel = ctk.CTkLabel(self.mainStudent, text=error_message, font=("Arial", 16), anchor="w", text_color='red')
            self.errorLabel.pack(fill='x', pady=10)

    def destroyInfo(self):
        """Destroy the mainStudent section."""
        if hasattr(self, "mainStudent") and self.mainStudent.winfo_exists():
            self.mainStudent.destroy()  

    def initLayout(self):
        self.mainInfo()
        self.mainCamera()
        self.mainDebug()
        
    def initializeCamera(self):
        self.updateCameraFrame()

    def updateCameraFrame(self):
        frame = self.camera.start_recognition()
        if frame is not None:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgTk = ctk.CTkImage(light_image=img, dark_image=img, 
                                size=(self.mainCamera.winfo_width(), self.mainCamera.winfo_height()))

            self.camera_label.img = imgTk
            self.camera_label.configure(image=imgTk)

        # Schedule the next frame update
        self.window.after(30, self.updateCameraFrame)