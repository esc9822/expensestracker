# Currency Conversion Feature

## Paano Gumagana ang LIVE Currency Conversion

### 1. Base Currency
- Lahat ng expenses ay naka-save sa database bilang **PHP (Philippine Peso)**
- PHP ang base currency, lahat ng conversions ay based dito

### 2. LIVE Exchange Rates (Auto-Update Daily!)
```
🌐 AUTOMATIC DAILY UPDATES from exchangerate-api.com
✅ Real-time exchange rates
✅ Auto-refresh every 24 hours
✅ Manual refresh button available
✅ Cached for fast loading
```

**Current rates update automatically every day!**
- 1 PHP = X USD, GBP, EUR, JPY, etc.
- Rates fetched from live API when app starts
- Updates automatically if older than 24 hours
- Falls back to stored rates if API fails

### 3. Paano Ito Gumagana

#### Pag-add ng Expense:
1. Mag-select ka ng country (e.g., United States - USD)
2. Mag-input ka ng amount (e.g., $100)
3. **Automatic conversion to PHP** bago i-save:
   - $100 ÷ 0.018 = ₱5,555.56 (saved in database)

#### Pag-view ng Expenses:
1. Mag-select ka ng country (e.g., Japan - JPY)
2. **Automatic conversion from PHP to JPY**:
   - ₱5,555.56 × 2.65 = ¥14,722.22 (displayed on screen)

### 4. Benefits
✅ **Single Source of Truth**: All amounts stored in one currency (PHP)
✅ **Real-time Conversion**: Switch countries anytime, amounts convert automatically
✅ **Accurate Budget Tracking**: Budget calculations stay consistent
✅ **Easy Reporting**: Reports automatically show in selected currency

### 5. Exchange Rate Display
- Nakikita sa taas ng page ang current exchange rate
- Example: "1 PHP = 0.0180 USD | 1 USD = 55.56 PHP"
- Madaling i-check kung magkano ang conversion

### 6. Halimbawa ng Paggamit

**Scenario**: Travel expenses sa different countries

1. **Add expense sa Philippines**:
   - Select: Philippines (₱ PHP)
   - Input: ₱1,000 for hotel
   - Saved: ₱1,000

2. **Add expense sa USA**:
   - Select: United States ($ USD)
   - Input: $50 for food
   - Saved: ₱2,777.78 (auto-converted)

3. **View in Japan currency**:
   - Select: Japan (¥ JPY)
   - Hotel shows: ¥2,650
   - Food shows: ¥7,361.11
   - Total: ¥10,011.11

### 7. Important Notes
✅ **Exchange rates AUTO-UPDATE DAILY** - live rates from internet API!
✅ **24-hour cache** - updates automatically when older than 24 hours
✅ **Manual refresh** - click "🔄 Refresh Now" link to force update
✅ **Fallback system** - uses stored rates if API fails
✅ **Base storage is always PHP** - all amounts converted to PHP when saving
✅ **Display only conversion** - walang actual currency exchange

### 8. Rate Update System
**Automatic Updates:**
- App checks rate age on every page load
- If rates are older than 24 hours, fetches new rates from API
- Rates are cached in database with timestamp
- Shows "Rates updated: [timestamp]" on screen

**Manual Refresh:**
- Click "🔄 Refresh Now" link sa country selector
- Forces immediate API call for latest rates
- Updates timestamp and displays success message

**API Source:**
- Primary: exchangerate-api.com (free API)
- No API key required for basic usage
- Updates multiple times per day

### 9. Fallback System
Kung walang internet o API down:
1. Uses cached rates from database (if available)
2. Falls back to hardcoded rates in config.py
3. Shows message: "Using cached rates" or "API failed, using fallback rates"

### 10. Updating API Settings
Para palitan ang API source, edit: `config.py`
```python
# Currency Exchange API Configuration
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/PHP'
# Alternative: 'https://api.exchangerate.host/latest?base=PHP'
```

---
**Developed by ESC © 2026**
