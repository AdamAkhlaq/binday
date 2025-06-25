# 🗑️ Binday – Bin Collection Reminder Tool

**Binday** is a lightweight Python script that fetches upcoming bin collection details (e.g., recycling, general waste) from my local council. The API behind the council’s website is **not publicly documented**, so I reverse-engineered it and built a CLI tool that tells me which bins to put out and when.

This project demonstrates my ability to work with undocumented systems, handle HTTP requests and JSON parsing, and create practical tools for everyday use—while also maintaining security and privacy through the use of environment variables.

---

## 🚀 Features

- ✅ **Reverse-engineered** a private council API via browser developer tools
- 📡 **Replicated web requests** in Python using the `requests` module
- 🧹 **Parsed JSON and XML data** to extract and display only the bin types and dates
- 🔐 **Used environment variables** to securely store location-specific data (e.g., postcode, address ID)
- 🖥️ **Created a `.bat` file** to run the script easily from the Windows terminal

---

## 💻 Example Output

```bash
C:\Users\adam>binday
Next bin collection on Thursday, 26 June 2025:
 - Green Bin
 - Blue Bin
 - Black Bin
```

---

## 🔐 Privacy Considerations

All sensitive information (such as postcode or address identifiers) is handled via environment variables, ensuring:

- No personal data is stored in the codebase
- The script remains safe to store, version, or demo
- Quick and secure reconfiguration if location changes

---

## 🧠 What I Learned

- How to inspect and decode web traffic to reverse-engineer undocumented APIs
- Building HTTP requests in Python that mimic real browser behavior
- Using `.env` files and environment variables for safe, configurable scripts
- Creating clean and portable tools for terminal-based automation on Windows

---

## 👨‍💻 Why I Built This

I created Binday to avoid manually checking my council’s bin collection schedule through a cumbersome website. This project allowed me to:

- Solve a real-world problem using code
- Practice API analysis and scripting
- Automate a repetitive task efficiently

---
