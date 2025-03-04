# **User Authentication and Target Management System using Flask and MySQL**  

## **📌 Project Description**  
This is a **Flask-based web application** that provides **user authentication** and a **target management system** with a secure login and registration process. The application enables users to register, log in, edit their profiles, set personal targets (with a limit of 5 targets per user), and remove them when needed. The backend is powered by **MySQL**, and **bcrypt** is used for password hashing to enhance security.

## **🚀 Features**  
✅ **User Authentication:** Secure user login, registration, and logout.  
✅ **Password Hashing:** Uses **bcrypt** for secure password storage.  
✅ **Session Management:** Maintains user sessions to restrict unauthorized access.  
✅ **Profile Management:** Users can edit their name, email, and password.  
✅ **Target Management:** Users can add up to **5 personal targets** and remove them if needed.  
✅ **Data Persistence:** Stores user and target data using **MySQL**.  
✅ **Cache Control:** Prevents caching for enhanced security.  

## **🛠️ Technologies Used**  
- **Flask** (Python Web Framework)  
- **MySQL** (Database)  
- **bcrypt** (Password Hashing)  
- **Flask-Session** (Session Management)  
- **HTML, CSS** (Frontend)  

## **💻 How to Run the Project**  

### **1️⃣ Install Dependencies**  
```bash
pip install flask mysql-connector-python bcrypt
```

### **2️⃣ Set Up MySQL Database**  
Create a MySQL database and table structure:  
```sql
CREATE DATABASE thunder;

USE thunder;

CREATE TABLE auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE targets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    target VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES auth(id) ON DELETE CASCADE
);
```

### **3️⃣ Configure Database in `app.py`**  
Replace MySQL credentials in `app.py` with your own:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_mysql_password'
MYSQL_DB = 'thunder'
```

### **4️⃣ Run the Application**  
```bash
python app.py
```
Access the app in your browser: **http://127.0.0.1:5000/**  

## **📷 Screenshots (Optional)**  
- Login Page  
- Registration Page  
- Dashboard  
- Target Management  

## **📜 License**  
This project is open-source and free to use.  

🔗 **Feel free to contribute, report issues, or suggest improvements!** 🚀  

#Flask #Python #Authentication #MySQL #WebApp #Project
