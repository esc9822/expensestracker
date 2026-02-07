# ============================================================
# EXPENSE TRACKER WEB APPLICATION
# Author: Edward Colon (ESC)
# Copyright (c) 2026
# GitHub: github.com/esc9822/expensestracker
# ============================================================

from flask import Flask, render_template, request, redirect, send_file, session, flash
import csv
from datetime import datetime
import database as db
from functools import wraps
import config
import os
import uuid

app = Flask(__name__)
# Use environment variable for production, fallback for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

db.init_db()
success, message = config.fetch_live_rates()

def get_user_id():
    """Get or create a unique user_id for this browser/device"""
    if 'browser_id' not in session:
        # Generate a unique ID for this browser/device
        session['browser_id'] = str(uuid.uuid4())
    return session['browser_id']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if config.MODE == 'PERSONAL':
            if 'user' not in session:
                session['user'] = {'id': 1, 'username': 'admin', 'role': 'admin'}
            return f(*args, **kwargs)
        
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if config.MODE == 'PERSONAL':
            return f(*args, **kwargs)
        
        if 'user' not in session or session['user']['role'] != 'admin':
            flash('Admin access required!')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if config.MODE == 'PERSONAL':
        session['user'] = {'id': 1, 'username': 'admin', 'role': 'admin'}
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.verify_user(username, password)
        if user:
            session['user'] = user
            return redirect('/')
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if config.MODE == 'PERSONAL':
        return redirect('/')
    
    session.pop('user', None)
    return redirect('/login')

@app.route('/set_country', methods=['POST'])
def set_country():
    country = request.form.get('country', config.DEFAULT_COUNTRY)
    session['country'] = country
    return redirect(request.referrer or '/')

@app.route('/refresh_rates')
@login_required
def refresh_rates():
    success, message = config.fetch_live_rates()
    flash(message)
    return redirect(request.referrer or '/')

def get_current_country():
    return session.get('country', config.DEFAULT_COUNTRY)

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        due_date = request.form.get("due_date", "")
        
        # Convert amount to base currency (PHP) before saving
        current_country = get_current_country()
        country_info = config.get_country_info(current_country)
        amount_in_base = config.convert_to_base(amount, country_info['currency'])
        
        user_id = get_user_id()
        db.add_expense(date, name, amount_in_base, category, due_date, user_id)
        return redirect("/")

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_filter = request.args.get('category', '', type=str)
    
    user_id = get_user_id()
    expenses, total = db.get_all_expenses(page=page, search=search, category=category_filter, user_id=user_id)
    
    # Get current country and currency info
    current_country = get_current_country()
    country_info = config.get_country_info(current_country)
    
    # Convert all expense amounts from base currency to selected currency
    converted_expenses = []
    for expense in expenses:
        # Convert to tuple format for template compatibility (id, date, name, amount, category, due_date)
        converted_expense = (
            expense['id'],
            expense['date'],
            expense['name'],
            config.convert_from_base(expense['amount'], country_info['currency']),
            expense['category'],
            expense['due_date'] if 'due_date' in expense.keys() else ''
        )
        converted_expenses.append(converted_expense)
    
    # Calculate pagination
    per_page = 50
    total_pages = (total + per_page - 1) // per_page
    
    # Get budget status and convert
    budget_status = db.get_budget_status(user_id=user_id)
    if budget_status:
        budget_status['budget'] = config.convert_from_base(budget_status['budget'], country_info['currency'])
        budget_status['spent'] = config.convert_from_base(budget_status['spent'], country_info['currency'])
        budget_status['remaining'] = config.convert_from_base(budget_status['remaining'], country_info['currency'])
    
    # Get conversion rate (1 PHP = X selected currency)
    conversion_rate = config.CONVERSION_RATES.get(country_info['currency'], 1.0)
    
    # Get last update time for rates
    cached_rates, last_update = db.get_currency_rates()
    
    return render_template("index.html", 
                         expenses=converted_expenses, 
                         page=page, 
                         total_pages=total_pages,
                         search=search,
                         category_filter=category_filter,
                         total_count=total,
                         budget_status=budget_status,
                         user=session['user'],
                         mode=config.MODE,
                         country=current_country,
                         countries=config.COUNTRIES,
                         currency=country_info['currency'],
                         currency_symbol=country_info['symbol'],
                         conversion_rate=conversion_rate,
                         rates_last_update=last_update)

@app.route("/delete/<int:index>")
@login_required
@admin_required
def delete(index):
    user_id = get_user_id()
    db.delete_expense(index, user_id)
    return redirect("/")

@app.route("/delete_all_expenses")
@login_required
@admin_required
def delete_all_expenses():
    user_id = get_user_id()
    db.delete_all_expenses(user_id)
    flash('All expenses deleted successfully!')
    return redirect("/")

@app.route("/set_budget", methods=["POST"])
@login_required
@admin_required
def set_budget():
    amount = float(request.form["budget_amount"])
    month = request.form.get("budget_month", "")
    
    if not month:
        from datetime import datetime
        month = datetime.now().strftime('%Y-%m')
    
    current_country = get_current_country()
    country_info = config.get_country_info(current_country)
    amount_in_base = config.convert_to_base(amount, country_info['currency'])
    
    user_id = get_user_id()
    db.set_budget(amount_in_base, month, user_id)
    return redirect("/")

@app.route("/clear_budget")
@login_required
@admin_required
def clear_budget():
    user_id = get_user_id()
    db.clear_budget(user_id=user_id)
    flash('Budget cleared successfully!')
    return redirect("/")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
@login_required
def edit(index):
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        due_date = request.form.get("due_date", "")
        
        # Convert amount to base currency before saving
        current_country = get_current_country()
        country_info = config.get_country_info(current_country)
        amount_in_base = config.convert_to_base(amount, country_info['currency'])
        
        user_id = get_user_id()
        db.update_expense(index, date, name, amount_in_base, category, due_date, user_id)
        return redirect("/")

    expense = db.get_expense_by_id(index, get_user_id())
    if expense:
        current_country = get_current_country()
        country_info = config.get_country_info(current_country)
        
        # Convert amount from base currency to selected currency
        expense_dict = dict(expense)
        expense_dict['amount'] = config.convert_from_base(expense['amount'], country_info['currency'])
        
        conversion_rate = config.CONVERSION_RATES.get(country_info['currency'], 1.0)
        
        return render_template("edit.html", expense=expense_dict, index=index, 
                             country=current_country,
                             countries=config.COUNTRIES,
                             currency=country_info['currency'],
                             currency_symbol=country_info['symbol'],
                             conversion_rate=conversion_rate)
    
    return redirect("/")

@app.route("/report")
@login_required
def report():
    user_id = get_user_id()
    data = db.get_report_data(user_id)
    budget_status = db.get_budget_status(user_id=user_id)
    
    current_country = get_current_country()
    country_info = config.get_country_info(current_country)
    
    # Convert all amounts from base currency to selected currency
    converted_total = config.convert_from_base(data['total'], country_info['currency'])
    
    converted_category_totals = {}
    for category, amount in data['category_totals'].items():
        converted_category_totals[category] = config.convert_from_base(amount, country_info['currency'])
    
    converted_monthly_totals = {}
    for month, amount in data['monthly_totals'].items():
        converted_monthly_totals[month] = config.convert_from_base(amount, country_info['currency'])
    
    converted_expenses = []
    for expense in data['all_expenses']:
        expense_dict = dict(expense)
        expense_dict['amount'] = config.convert_from_base(expense['amount'], country_info['currency'])
        converted_expenses.append(expense_dict)
    
    if budget_status:
        budget_status['budget'] = config.convert_from_base(budget_status['budget'], country_info['currency'])
        budget_status['spent'] = config.convert_from_base(budget_status['spent'], country_info['currency'])
        budget_status['remaining'] = config.convert_from_base(budget_status['remaining'], country_info['currency'])
    
    conversion_rate = config.CONVERSION_RATES.get(country_info['currency'], 1.0)
    
    # Get last update time for rates
    cached_rates, last_update = db.get_currency_rates()
    
    return render_template("report.html", 
                         total=converted_total, 
                         category_totals=converted_category_totals,
                         monthly_totals=converted_monthly_totals,
                         expenses=converted_expenses,
                         budget_status=budget_status,
                         user=session['user'],
                         mode=config.MODE,
                         country=current_country,
                         countries=config.COUNTRIES,
                         currency=country_info['currency'],
                         currency_symbol=country_info['symbol'],
                         conversion_rate=conversion_rate,
                         rates_last_update=last_update)

@app.route("/download")
@login_required
def download_csv():
    import io
    from io import StringIO
    
    user_id = get_user_id()
    data = db.get_report_data(user_id)
    expenses = data['all_expenses']
    total = data['total']
    category_totals = data['category_totals']
    monthly_totals = data['monthly_totals']
    budget_status = db.get_budget_status(user_id=user_id)
    
    current_country = get_current_country()
    country_info = config.get_country_info(current_country)
    currency_symbol = country_info['symbol']
    
    # Create comprehensive CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write budget section
    writer.writerow(['MONTHLY BUDGET STATUS'])
    writer.writerow(['Country', current_country])
    writer.writerow(['Currency', country_info['currency']])
    writer.writerow(['Month', budget_status['month']])
    writer.writerow(['Budget Amount', f'{currency_symbol}{budget_status["budget"]:.2f}'])
    writer.writerow(['Total Spent', f'{currency_symbol}{budget_status["spent"]:.2f}'])
    writer.writerow(['Remaining', f'{currency_symbol}{budget_status["remaining"]:.2f}'])
    writer.writerow(['Percentage Used', f'{budget_status["percentage"]:.1f}%'])
    if budget_status['remaining'] < 0:
        writer.writerow(['Status', f'OVER BUDGET by {currency_symbol}{abs(budget_status["remaining"]):.2f}'])
    elif budget_status['percentage'] > 80:
        writer.writerow(['Status', f'WARNING: {budget_status["percentage"]:.1f}% used'])
    else:
        writer.writerow(['Status', 'On Track'])
    
    # Write expenses section
    writer.writerow([])
    writer.writerow(['EXPENSE DETAILS'])
    writer.writerow(['Date', 'Expense Name', 'Amount', 'Category', 'Due Date'])
    for expense in expenses:
        writer.writerow(expense)
    
    # Write summary section
    writer.writerow([])
    writer.writerow(['SUMMARY'])
    writer.writerow(['Total Expenses', f'{currency_symbol}{total:.2f}'])
    writer.writerow(['Total Transactions', len(expenses)])
    
    # Write category breakdown
    writer.writerow([])
    writer.writerow(['CATEGORY BREAKDOWN'])
    writer.writerow(['Category', 'Amount', 'Percentage'])
    for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total * 100) if total > 0 else 0
        writer.writerow([category, f'{currency_symbol}{amount:.2f}', f'{percentage:.1f}%'])
    
    # Write monthly breakdown
    writer.writerow([])
    writer.writerow(['MONTHLY BREAKDOWN'])
    writer.writerow(['Month', 'Amount'])
    for month in sorted(monthly_totals.keys(), reverse=True):
        writer.writerow([month, f'{currency_symbol}{monthly_totals[month]:.2f}'])
    
    # Convert to bytes for download
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'expenses_report_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/download_pdf')
@login_required
def download_pdf():
    """Generate and download PDF report with visualizations"""
    try:
        # Workaround for PIL DLL issues - mock PIL if it fails to load
        import sys
        try:
            from PIL import Image
        except (ImportError, OSError) as pil_error:
            # Create a mock PIL module to allow reportlab to import
            print(f"PIL import failed: {pil_error}, using mock")
            from unittest.mock import MagicMock
            sys.modules['PIL'] = MagicMock()
            sys.modules['PIL.Image'] = MagicMock()
        
        # Import reportlab components
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        import io
    except ImportError as e:
        print(f"Import error in PDF export: {e}")
        flash(f'PDF export requires additional libraries. Error: {str(e)}')
        return redirect('/report')
    
    try:
        # Get country and currency
        country = session.get('country', config.DEFAULT_COUNTRY)
        country_info = config.get_country_info(country)
        currency = country_info['currency']
        currency_symbol = country_info['symbol']
        conversion_rate = config.CONVERSION_RATES.get(currency, 1.0)
        
        # Get report data
        user_id = get_user_id()
        report_data = db.get_report_data(user_id)
        
        # Convert amounts for current currency
        total = report_data['total'] * conversion_rate
        
        category_totals = {}
        for category, amount in report_data['category_totals'].items():
            category_totals[category] = amount * conversion_rate
        
        monthly_totals = {}
        for month, amount in report_data['monthly_totals'].items():
            monthly_totals[month] = amount * conversion_rate
        
        # Convert expense amounts
        expenses = []
        for exp in report_data['all_expenses']:
            expenses.append({
                'date': exp[0],
                'name': exp[1],
                'amount': exp[2] * conversion_rate,
                'category': exp[3],
                'due_date': exp[4] if len(exp) > 4 else ''
            })
        
        # Get budget status
        budget_status = db.get_budget_status(user_id=user_id)
        if budget_status and currency != config.DEFAULT_CURRENCY:
            budget_status['budget'] *= conversion_rate
            budget_status['spent'] *= conversion_rate
            budget_status['remaining'] *= conversion_rate
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
        )
        
        # Title
        elements.append(Paragraph("Expense Tracker Report", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", styles['Normal']))
        elements.append(Paragraph(f"Currency: {currency_symbol} {currency}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Section
        elements.append(Paragraph("Summary", heading_style))
        summary_data = [
            ['Total Expenses:', f'{currency_symbol}{total:.2f}'],
            ['Total Transactions:', str(len(expenses))],
            ['Categories:', str(len(category_totals))],
        ]
        
        if budget_status:
            summary_data.extend([
                ['Monthly Budget:', f'{currency_symbol}{budget_status["budget"]:.2f}'],
                ['Budget Used:', f'{budget_status["percentage"]:.1f}%'],
                ['Remaining:', f'{currency_symbol}{budget_status["remaining"]:.2f}'],
            ])
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Category Breakdown
        elements.append(Paragraph("Category Breakdown", heading_style))
        category_data = [['Category', 'Amount', 'Percentage']]
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total * 100) if total > 0 else 0
            category_data.append([category, f'{currency_symbol}{amount:.2f}', f'{percentage:.1f}%'])
        
        category_table = Table(category_data, colWidths=[2*inch, 2*inch, 2*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(category_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Monthly Breakdown
        elements.append(Paragraph("Monthly Breakdown", heading_style))
        monthly_data = [['Month', 'Amount']]
        for month in sorted(monthly_totals.keys(), reverse=True):
            monthly_data.append([month, f'{currency_symbol}{monthly_totals[month]:.2f}'])
        
        monthly_table = Table(monthly_data, colWidths=[3*inch, 3*inch])
        monthly_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(monthly_table)
        elements.append(PageBreak())
        
        # Expense Details
        elements.append(Paragraph("Expense Details", heading_style))
        expense_data = [['Date', 'Name', 'Amount', 'Category']]
        for e in expenses[:50]:  # Limit to 50 most recent
            expense_data.append([
                e['date'], 
                e['name'][:30], 
                f'{currency_symbol}{e["amount"]:.2f}', 
                e['category']
            ])
        
        expense_table = Table(expense_data, colWidths=[1.2*inch, 2.3*inch, 1.2*inch, 1.3*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(expense_table)
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("© 2026 Expense Tracker | Developed by ESC", 
                                 ParagraphStyle('Footer', parent=styles['Normal'], 
                                              fontSize=9, textColor=colors.grey, alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'expense_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Error generating PDF: {str(e)}')
        return redirect('/report')

if __name__ == '__main__':
    app.run(debug=True)
