# 💰 Expense Tracker - Portfolio Project

A modern, feature-rich expense tracking web application built with Flask and Bootstrap 5.

## 🌟 Features

### Core Functionality
- ✅ **Expense Management** - Add, edit, delete expenses with categories
- 💵 **Multi-Currency Support** - 10 countries with live exchange rates
- 📊 **Budget Tracking** - Set monthly budgets with visual progress indicators
- 📈 **Analytics Dashboard** - Comprehensive expense reports with charts
- 🔐 **Authentication** - Multi-user support (Personal/Corporate modes)
- 📱 **Responsive Design** - Mobile-friendly Bootstrap 5 interface

### Advanced Features
- 🌙 **Dark Mode** - Toggle between light/dark themes (persisted in localStorage)
- 📄 **PDF Export** - Generate professional expense reports with ReportLab
- 📊 **Multiple Visualizations**:
  - Budget gauge chart (doughnut style)
  - Category pie chart
  - Category bar chart
  - Monthly trend line chart
- 🔔 **Smart Notifications**:
  - Overdue bill alerts
  - Upcoming bill warnings (7-day window)
  - Budget overspend notifications
- 💾 **CSV Export** - Download complete expense data
- 🔄 **Live Currency Rates** - Auto-refresh from ExchangeRate API
- 🎨 **Modern UI/UX**:
  - Gradient backgrounds
  - Card-based layout
  - Smooth animations
  - Icon-rich interface (Bootstrap Icons)
  - Hover effects

### Technical Features
- 🗃️ **SQLite Database** - Efficient data storage
- 🔐 **Password Hashing** - SHA256 encryption
- 📄 **Pagination** - Optimized expense listing
- 🔍 **Search & Filter** - By name and category
- 📅 **Due Date Tracking** - For bills and recurring expenses
- 🌐 **Session Management** - User authentication
- 🎯 **Role-Based Access** - Admin/User permissions

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLite3** - Database
- **ReportLab** - PDF generation
- **Chart.js** - Data visualization

### Frontend
- **Bootstrap 5** - UI framework
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side functionality
- **Google Fonts (Inter)** - Typography
- **CSS3 Custom Properties** - Theme system

## 📁 Project Structure

```
Expense Tracker/
├── app.py                 # Main Flask application
├── config.py              # Configuration & currency settings
├── database.py            # Database operations
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main dashboard
│   ├── report.html       # Analytics page
│   ├── edit.html         # Edit expense form
│   └── login.html        # Login page
└── README.md             # Documentation
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   ```
   Open browser: http://localhost:5000
   ```

## 🎯 Usage

### Personal Mode (Default)
- No login required
- Single-user access
- Full admin privileges

### Corporate Mode
- Multi-user support
- Login required
- Role-based permissions

**Demo Accounts (Corporate Mode):**
- Admin: `admin` / `admin`
- User: `user` / `user`

## 💡 Key Features Showcase

### 1. Dark Mode Toggle
```javascript
// Persisted in localStorage
localStorage.setItem('theme', 'dark');
```

### 2. Multi-Currency Support
- 10 countries with live exchange rates
- Automatic conversion
- Visual currency symbols

### 3. Budget Management
- Set monthly budgets
- Real-time progress tracking
- Visual indicators (green/yellow/red)
- Overspend alerts

### 4. Smart Notifications
- Overdue bills (red alert)
- Upcoming bills (yellow warning)
- Budget warnings
- Dynamic badge counters

### 5. Export Options
- **CSV Export** - Complete data export
- **PDF Export** - Professional reports with:
  - Summary statistics
  - Category breakdown tables
  - Monthly trends
  - Visual branding

## 📊 Analytics Dashboard

### Charts Included:
1. **Budget Gauge** - Semicircle doughnut chart
2. **Category Pie Chart** - Distribution visualization
3. **Category Bar Chart** - Comparative analysis
4. **Monthly Line Chart** - Trend analysis

## 🎨 Design System

### Colors
- Primary: `#667eea` (Purple-Blue gradient)
- Success: `#28a745`
- Warning: `#ffc107`
- Danger: `#dc3545`

### Dark Mode Palette
- Background: `#1a1a2e`
- Card Background: `#16213e`
- Text: `#eaeaea`
- Border: `#0f3460`

## 🔐 Security Features

- SHA256 password hashing
- Session management
- CSRF protection (Flask built-in)
- SQL injection prevention (parameterized queries)
- Role-based access control

## 📈 Performance Optimizations

- Pagination for large datasets
- Efficient database queries
- LocalStorage for theme persistence
- Minimal JavaScript dependencies
- CDN-hosted libraries

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔧 Configuration

Edit `config.py` to customize:
- Mode (PERSONAL/CORPORATE)
- Default currency
- Currency conversion rates
- Fallback rates
- Country mappings

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

**ESC** - Full Stack Developer
- Portfolio-ready expense tracking application
- Built with modern web technologies
- Focus on UX/UI design and functionality

## 🚀 Future Enhancements

Potential additions:
- Email notifications for due bills
- Recurring expense automation
- Category icons customization
- Data import from bank statements
- Budget forecasting with AI
- Mobile app (React Native)
- Cloud database integration
- Multi-language support

## 📸 Screenshots

### Dashboard (Light Mode)
- Clean card-based layout
- Budget progress visualization
- Quick action buttons
- Expense table with filters

### Dashboard (Dark Mode)
- Elegant dark theme
- Eye-friendly colors
- Persistent toggle

### Analytics Page
- Multiple chart visualizations
- Comprehensive statistics
- Export options

### Mobile View
- Fully responsive design
- Touch-friendly interface
- Optimized layouts

---

**Built with ❤️ for portfolio demonstration**

*Last Updated: February 2026*
