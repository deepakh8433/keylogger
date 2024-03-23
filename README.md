<h1>Keylogger with Automated Setup and Cross-Platform Support</h1> <br>
This Python script serves as a versatile keylogger capable of automatically setting up its environment by downloading necessary dependencies. It supports various operating systems, making it accessible and easy to use for monitoring keyboard activities.<br><br>

![2024-03-24 01_54_27-316267130-0aca001a-1673-4d70-a3db-89a85ba731a5 png (1098×165) - Brave](https://github.com/deepakh8433/keylogger/assets/164472207/869b90e6-936c-4d6e-a47a-ae3d92d238f0)


<br><br>
<h3>Features</h3>
<b>Automated Dependency Installation:</b> The script automatically installs required libraries and dependencies using pip3 if they are not already present.<br>
<b>Cross-Platform Compatibility:</b> Designed to function seamlessly across different operating systems including Windows, Linux, and macOS.<br>
<b>Effortless Execution:</b> Users can initiate the keylogger simply by executing the script without manual setup or library installation.<br>
<b>Periodic Reporting:</b> The keylogger periodically sends reports via email containing system information and logged keystrokes.<br>

<h3>Installation</h3>
&nbsp;Clone the repository: <br><br>

&nbsp;git clone https://github.com/deepah8433/keylogger.git<br><br>
&nbsp;cd keylogger/<br><br>


<h3>Configure your email.</h3>
befor run the keylogger we have make changes in our gmail account sending mail <br>
(in this we are using 2 gmail accaount <b>first</b> is disposal and its less secure password and <b>second<b> is recever mail)<br><br>
 &nbsp; step 1: if you are using gmail then click manage your google account<br>
 &nbsp; step 2: click security<br>
 &nbsp; step 3: add 2 step verification then click 2 step verification<br>
 &nbsp; step 4: scroll down you'll get app password<br>
 &nbsp; step 5: click add a name that you want then you get a password copy that password paste in keylogger disposal password<br>

<h3>Run the script:</h3> 
&nbsp;python3 keylogger.py

<h3>The keylogger will start monitoring keystrokes and system information in the background.</h3>

<h3>It will periodically send email reports to the specified email address.</h3>

<h3>Configuration</h3>
You can customize the following settings in the script:<br><br>

&nbsp;Email sender and receiver addresses.<br>
&nbsp;Email sending frequency for system information and keystroke logs.<br>
&nbsp;Ignored keys that should not be logged.<br>
<br>
<h2>Disclaimer:</h2><br>
&nbsp;This keylogger is intended for educational and security assessment purposes only. Do not use it for malicious intent or illegal activities. Use responsibly and only on systems you own or have explicit permission to monitor.

