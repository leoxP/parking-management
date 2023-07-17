# Parking Management System

The Parking Management System is a software application developed using Python's Tkinter library for the graphical user interface (GUI) and MySQL for the backend database. It aims to facilitate parking management in crowded places.

## Features

- **Admin Functionality:** The system provides an admin interface where the administrator can perform various tasks such as creating and dropping databases, creating tables, and setting parking spot availability.
- **Car and Bike Management:** The system supports separate databases for car parking and bike parking. Each database includes tables to store customer information, parking spot availability, entry times, and costs.
- **User Functionality:** Users can access the system to enter and exit the parking area. The system records the vehicle number, entry time, and assigns an available parking spot. Upon exit, it calculates the parking duration and cost.

## Prerequisites

Before running the Parking Management System, ensure you have the following dependencies installed:

- Python 3.10
- Tkinter library
- MySQL connector library

## Getting Started

1. Clone the repository or download the source code.
2. Install the necessary dependencies using pip and the requirements.txt file
3. Set up your MySQL server and update the database connection details in the code.
4. Run the main Python script to start the application:


## Usage

- Upon launching the application, you will be presented with a login screen.
- Enter the admin credentials to access the admin functionality, or choose the user option to enter or exit the parking area.
- The admin can create and drop databases, create tables, set parking spot availability, and configure pricing.
- Users can enter their vehicle number and choose the entry or exit option to perform the respective action.

## License

This project is licensed under the [MIT License](LICENSE).


