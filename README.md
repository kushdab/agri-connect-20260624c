# AgriConnect Kenya 2026

A lightweight Python-based marketplace application designed for the Kenyan agricultural ecosystem. It enables farmers in productive regions (like Nyandarua, Eldoret, and Meru) to list their harvests directly for wholesalers in Nairobi.

## Features
- **Role-based access**: Farmers can list produce; Wholesalers can browse the marketplace.
- **Real-time Listings**: View quantity, pricing (KES), and origin location.
- **Kenya-Specific UX**: Built with local terminology and logistics in mind.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Access via browser: `http://127.0.0.1:5000`

## Technology Stack
- **Backend**: Flask (Python 3)
- **Frontend**: Bootstrap 5 (Responsive CSS)
- **Auth**: Flask Session management