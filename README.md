🧩 How to Use This Project
Install dependencies via:

pip install -r requirements.txt
Create an Oxylabs Pay-As-You-Go account.

Insert your Oxylabs credentials (username and password) into test2.py.

Run the controller:
python priceSearchController.py
Open your browser and navigate to your local server URL (e.g., http://127.0.0.1:5000/).

📊 User Interface
The UI allows you to input a product name and select a marketplace (currently supports eBay).

After pressing Submit, the app will retrieve and visualize price data in a bar chart.

Use the "Reset Index" feature to change how many grouped results appear at once (e.g., view 20 at a time).

⚠️ Marketplace Notes
During early testing phases, the application functioned on Amazon, Etsy, and eBay.

However, further review of Amazon and Etsy's Terms of Service revealed that automated data collection is not permitted.

To remain in compliance, functionality for these two sites has been disabled. No scraping of those platforms occurs in the current build.

🔒 Only eBay is actively supported via the user interface in accordance with their public site accessibility at this time.

🔐 Ethical Use Disclaimer
This project is intended for educational and demonstrative purposes only. Always ensure your use of this tool complies with each website’s Terms of Service and applicable laws.
  
