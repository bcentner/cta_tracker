# CTeAsy

**CTeAsy** makes the CTA easy! It is a utility designed to help users quickly determine when the next train is arriving.

---

## 🚧 TODO

- Add support for bus tracking  
- Integrate Customer Alert API to determine if events are affecting service  

---

## 📡 Data Sources

- **Train Tracker API:** [CTA Train Tracker Documentation](https://www.transitchicago.com/developers/ttdocs/#_Toc296199901)  
- **Customer Alerts API:** [CTA Customer Alerts API Documentation (PDF)](https://www.transitchicago.com/assets/1/6/cta_Customer_Alerts_API_Developer_Guide_and_Documentation_20160929.pdf)

---

## 🌐 Hosting with Ngrok

To expose your local server to the internet using Ngrok:

1. Install Ngrok:
   ```bash
    $ choco install ngrok
    $ ngrok config add-authtoken <your_token>
    $ ngrok http <port_running_flask>