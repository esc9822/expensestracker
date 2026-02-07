# 💰 Expense Tracker

A modern expense tracking web application with multi-currency support, budget tracking, dark mode, and analytics.

**👨‍💻 Author: Edward Colon (ESC)**  
**📧 GitHub: [github.com/esc9822/expensestracker](https://github.com/esc9822/expensestracker)**  
**© 2026 All Rights Reserved**

## 🌐 Live Demo

**Try it now:** [[[https://expense-tracker-yourname.onrender.com](https://expense-tracker-yourname.onrender.com)](https://expensestracker-esc.onrender.com/)](https://expensestracker-esc.onrender.com/)

> **Note:** Free tier may take 30-60 seconds to wake up on first visit

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 💵 **Multi-Currency Support** - Track expenses in 10 different currencies with live exchange rates
- 📊 **Budget Tracking** - Set monthly budgets with visual progress indicators
- 📈 **Analytics Dashboard** - Pie charts, bar charts, and monthly trend analysis
- 🌙 **Dark Mode** - Beautiful dark theme that persists across pages
- 📄 **PDF Export** - Generate professional expense reports
- 📥 **CSV Export** - Download complete expense data
- 🔔 **Smart Notifications** - Alerts for overdue bills and budget warnings
- 📅 **Due Date Tracking** - Color-coded warnings for bills
- 🔍 **Search & Filter** - Find expenses by name or category
- 📱 **Responsive Design** - Works perfectly on mobile and desktop
- 🔐 **Two Modes** - Personal (instant access) or Corporate (multi-user with roles)

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser:**
```
http://127.0.0.1:5000
```

That's it! 🎉 Start tracking your expenses!

## 🎮 How to Use

### Adding Expenses
1. Click "Add New Expense" button
2. Fill in expense details (name, amount, category, date)
3. Optionally add a due date for bills
4. Click Submit

### Setting Budget
1. Enter your monthly budget amount in the budget section
2. View real-time budget progress with visual indicators
3. Get automatic warnings when approaching or exceeding budget

### Viewing Analytics
1. Click "View Analytics & Reports"
2. See expense breakdown by category (pie & bar charts)
3. View monthly spending trends
4. Export reports to PDF or CSV

### Changing Currency
1. Select your country from the currency dropdown
2. All amounts automatically convert to your selected currency
3. Refresh rates anytime with the refresh button

## 🌍 Supported Currencies

- 🇵🇭 Philippine Peso (PHP)
- 🇺🇸 US Dollar (USD)
- 🇪🇺 Euro (EUR)
- 🇬🇧 British Pound (GBP)
- 🇯🇵 Japanese Yen (JPY)
- 🇦🇺 Australian Dollar (AUD)
- 🇨🇦 Canadian Dollar (CAD)
- 🇸🇬 Singapore Dollar (SGD)
- 🇭🇰 Hong Kong Dollar (HKD)
- 🇰🇷 Korean Won (KRW)

## ⚙️ Configuration

### Personal vs Corporate Mode

Edit `config.py` to switch between modes:

```python
MODE = 'PERSONAL'  # No login, single user
# or
MODE = 'CORPORATE'  # Multi-user with admin/user roles
```

**PERSONAL Mode:**
- Direct access without login
- Full admin features
- Perfect for individual use

**CORPORATE Mode:**
- Login required
- Admin: Full access (budget, delete, reports)
- User: Limited access (add/edit only, no budget visibility)
- Default credentials:
  - Admin: `admin` / `admin123`
  - User: `user` / `user123`

## 📁 Project Structure

```
expense-tracker/
├── app.py              # Flask application
├── database.py         # Database operations
├── config.py           # Configuration (mode setting)
├── expenses.db         # SQLite database (auto-created)
├── templates/
│   ├── index.html      # Main page
│   ├── edit.html       # Edit expense
│   ├── report.html     # Reports & charts
│   └── login.html      # Login page (corporate mode)
├── LICENSE             # MIT License
└── README.md           # This file
```

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Security**: SHA256 password hashing

## 📊 Features in Detail

### Budget Management
- Set monthly budgets
- Real-time spending tracking
- Progress bar with percentage
- Color-coded alerts (green/yellow/red)
- Over-budget warnings

### Expense Categories
- Food, Transportation, Utilities
- Entertainment, Healthcare, Shopping
- Education, Car Insurance, Rent, Others

### Reports
- Total expenses summary
- Category breakdown (pie & bar charts)
- Monthly trends (line chart)
- Percentage distribution
- CSV export with full details

### Security (Corporate Mode)
- Session-based authentication
- Password hashing (SHA256)
- Role-based access control
- Admin/User permissions

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

**Copyright © 2026 ESC. All rights reserved.**

## 🙏 Credits

Developed by **ESC**

---

⭐ If you find this useful, please star the repository!


