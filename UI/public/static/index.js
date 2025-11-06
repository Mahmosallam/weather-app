$(document).ready(() => {
    const spinner = $('#spinner');
    $('#go').click(() => {
        getWeather($('#city').val());
    });

    $('#city').keypress(function (event) {
        var keycode = event.keyCode ? event.keyCode : event.which;
        if (keycode === 13) {
            getWeather($('#city').val());
        }
    });

    function getWeather(city) {
        // Show the spinner when the request is made
        spinner.show();
        $.ajax({
            type: 'get',
            url: '/weather/' + city,
            success: function (result) {
                // Extract the first forecast entry
                const current = result.list[0];
                const weather = current.weather[0];
                
                $('#result').show();
                
                // Weather icon from OpenWeatherMap
                $('#weather_icon').attr('src', `https://openweathermap.org/img/wn/${weather.icon}@2x.png`);
                
                // Weather description
                $('#weather_text').html(weather.description);
                
                // City and country
                $('#city_name').html(result.city.name);
                $('#country_name').html(result.city.country);
                
                // Temperature (convert from Kelvin to Celsius and Fahrenheit)
                const tempC = (current.main.temp - 273.15).toFixed(1);
                const tempF = ((current.main.temp - 273.15) * 9/5 + 32).toFixed(1);
                $('#temp').html(
                    tempC + '&deg;C&nbsp;-&nbsp;' + tempF + '&deg;F'
                );
                
                // Feels like temperature
                const feelsC = (current.main.feels_like - 273.15).toFixed(1);
                const feelsF = ((current.main.feels_like - 273.15) * 9/5 + 32).toFixed(1);
                $('#feels_like').html(
                    feelsC + '&deg;C&nbsp;-&nbsp;' + feelsF + '&deg;F'
                );
                
                // Hide the spinner after data is displayed
                spinner.hide();
            },
            error: function (error) {
                console.error(error);
                alert('Could not fetch weather data. Please try again.');
                // Hide the spinner if there is an error
                spinner.hide();
            },
        });
    }
});