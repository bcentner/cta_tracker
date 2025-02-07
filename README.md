# CTA Tracker
Allows users to easily find when the next train is coming

## TODO
- Webserver
- UI
- Add bus capability
- Use customer alert api -> is event affecting service?


## Data Sources
Train API: https://www.transitchicago.com/developers/ttdocs/#_Toc296199901 </br>
Customer API: https://www.transitchicago.com/assets/1/6/cta_Customer_Alerts_API_Developer_Guide_and_Documentation_20160929.pdf


<!-- TODO: project name ideas? CTEZ, CTeAsy, CTEasy, CTeasy -->

## Host with Ngrok
- *choco install ngrok*
- Sign up at https://dashboard.ngrok.com/signup
- Run config command:
    ngrok config add-authtoken ~your_token~
- Start flask app
- In a seperate terminal, run *ngrok http ~port_running_flask~*