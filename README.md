## Engeneering units convertion bot
The aim of a project is a provide handy util for conversion some measures, used in technology.
You can chat with bot [here](https://t.me/eng_unit_converter_bot)

### Supported conversions:
 - Temperature(C, F, K)
 - Thermoresistors(Pt100, 100P, Ni100, Cu100)
 - Mass Flow
 - Pressure
 - Analog 4-20 mA, 1-5V, 1-10V to physical measure



### Supported languages:
 - Russian
 - English

### Local project deploy with docker
1. Instal docker
2. Clone project to your working folder
    ```
    git clone git@github.com:ead3471/eng_converter_bot.git
    ```
3. Navigate to project folder
     ```
    cd eng_converter_bot
    ```
4. Create .env file.
     ```
    BOT_TOKEN = <Your bot token>
    LOG_LEVEL = <Logging level DEBUG, INFO etc>
    ```
5. Run docker compose
    ```
    docker-compose up 
     ```


