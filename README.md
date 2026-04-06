## Usage
The site is hosted at http://wegow.site.

## Purpose
This is a Django project for a weather forecasting application. It provides users a 3-day weather forecast for their location.

## Technologies Used
- Django: A Python backend framework.
- Bootstrap: A frontend framework for responsive design.
- OpenWeatherMap API: For fetching weather data. 

## Features
- Location suggestions
- 3-day weather forecast
- User-friendly interface

## Installation for development purposes
1. Clone the repository:
   ```
   git clone https://github.com/khoi-ha/DjangoWeatherForecast.git
    ```
2. Navigate to the project directory:
    ```
    cd DjangoWeatherForecast
    ```
3. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
5. Add openweathermap API key to an environment variable called `OPENWEATHER_API_KEY` (you can get one for free by signing up at https://openweathermap.org/api).

6. Download and setup PostgreSQL:
    - Follow the instructions for your operating system to install PostgreSQL.
    - Create a new database `forecast_app` and user for the project and host it at `localhost`.
    - Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

7. Set up the OpenWeatherMap API key:
    - Create a `.env` file in the DjangoWeatherForecast folder and add the following lines, replacing the placeholders with your actual API key and PostgreSQL password:
      ```
      DJANGO_SECRET_KEY=your_secret_key_here
      POSTGRES_PASSWORD=your_postgres_password_here
      ```

8. Switch to base folder:
    ```
    cd ..
    ```

9. Apply database migrations:
    ```
    python manage.py migrate
    ```

10. (Optional) Create a superuser to access the Django admin interface:
    ```
    python manage.py createsuperuser
    ```

11. Import locations, and weather types into database:
    ```
    python forecast/geography/locations.py
    python forecast/openWeather/default_imports.py
    ```

12. For testing purposes, you should turn on debug mode in `settings.py` by changing the line `DEBUG = False` to `DEBUG = True`.

13. Run the development server:
    ```
    python manage.py runserver
    ```

14. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action.
