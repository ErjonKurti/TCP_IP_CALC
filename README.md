IP Calculator with Subnetting - Kali Linux Inspired GUI
This project is a TCP/IP v4 Addressing Calculator with a modern GUI inspired by the Kali Linux aesthetic. The application allows users to calculate critical information for IPv4 addresses, including:

Network ID
Broadcast Address
First and Last Usable IPs
Number of Valid Hosts
Subnet Information for custom subnet prefixes.
Features
Dark Theme Design: A sleek, sharp edges, and professional aesthetics.
Dynamic Subnetting: Allows users to calculate subnets for a given IP and subnet mask with detailed information for each subnet.
User-Friendly Interface: Built with PyQt6, the GUI offers a responsive, interactive, and intuitive experience.
Error Handling: Validates input fields and provides clear error messages for invalid IPs or subnet masks.
Scrollable Results: Large subnet information is presented within a scrollable view for easy navigation.
Technologies Used
Python
PyQt6 for the GUI
ipaddress module for IP address calculations
How to Run
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/ip_calculator_gui.git
cd ip_calculator_gui
Install the dependencies:
bash
Copy code
pip install PyQt6
Run the application:
bash
Copy code
python main.py

Future Improvements
Add IPv6 support.
Implement additional tools like CIDR calculations.
Introduce export functionality for results in text or CSV format.
License
This project is licensed under the MIT License.

