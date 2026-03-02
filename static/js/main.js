function formatIsoDate(isoString) {
  const date = Temporal.PlainDate.from(isoString);

  return date.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: '2-digit'
  });
}

const KELVIN_CELCIUS_DIFFERENCE = 273;
function kelvinToCelsius(k) {
    if (isNaN(k)) {
        console.log(`Invalid input Kelvin value: ${c}`);
        return;
    }
    return Math.round(k-KELVIN_CELCIUS_DIFFERENCE);
}

const MS_KMH_CONVERSION = 3.6;
function msToKmh(ms) {
    if (isNaN(ms)) {
        console.log(`Invalid input m/s value: ${ms}`);
        return;
    } 
    return Math.round(ms*MS_KMH_CONVERSION);
} 

function fillWeatherCard(response) {
    var temp = $.trim($('#weather-card-template').html());
    for (let i=0; i < response.weather_data.length; i++) {
        obj = response.weather_data[i]
        var x = temp.replace(/\[date\]/ig, formatIsoDate(obj.date));
        x = x.replace(/\[background\]/ig, obj.weather.background)
        x = x.replace(/\[weather-type\]/ig, obj.weather.type);
        x = x.replace(/\[description\]/ig, obj.weather.description);
        x = x.replace(/\[min-temp\]/ig, kelvinToCelsius(obj.weather.temp_min))
        x = x.replace(/\[max-temp\]/ig, kelvinToCelsius(obj.weather.temp_max))
        x = x.replace(/\[feels-like\]/ig, kelvinToCelsius(obj.weather.feels_like));
        x = x.replace(/\[snowfall\]/ig, obj.weather.snow);
        x = x.replace(/\[cloud-cover\]/ig, Math.round(obj.weather.cloud_cover));
        x = x.replace(/\[wind-speed\]/ig, msToKmh(obj.weather.wind_speed));
        $("#weather-container").append(x);
        if (i == 0) {
            $(".weather-card").addClass("active");
        }
    }
}


$(document).ready(function () {
    let current_location_request = null;

    // Abort any ongoing location suggestion request when the user starts typing
    if (current_location_request !== null) {
        current_location_request.abort();
        $("#location-suggestions").removeClass("show").empty();
    }

    
    $("#search-bar").on("input", function (e) {
        let keyword = `${$(this).val()}`;
        let menu=$("#location-suggestions");
        
        // Only send a request if the keyword is at least 3 characters long
        // This is because the application is hosted on a free tier and we want to minimize unnecessary database queries
        if (keyword.length >= 3) {
            current_location_request = $.ajax({
                url: "geography/api/city_suggestions",
                data: { "keyword": keyword },
                success: function(response) {
                    menu = $("#location-suggestions");
                    menu.empty();

                    // If there are suggestions, populate the dropdown menu
                    if (response.suggestions.count > 0) {
                        response.suggestions.suggestions.forEach(function(item) {
                            menu.append(
                                "<li><a class='suggestion dropdown-item' href='#'>" + item + "</a></li>"
                            );
                        });

                        // On click, populate search bar with the suggestion and hide the dropdown menu
                        $(".suggestion").on("click", function(e) {
                            e.preventDefault();
                            $("#search-bar").val($(this).text());
                            menu.removeClass("show").empty();
                        });
                        menu.addClass('show');
                    } else {
                        menu.removeClass('show');
                    }
                },
                error: function(xhr, status, error) {
                    menu = $("#location-suggestions");
                    menu.empty();
                    menu.append(
                        "<li><a class='dropdown-item disabled' href='#'> Error fetching location suggestions </a></li>"
                    );
                    menu.addClass("show");
                }
                });
        } else {
                $("#location-suggestions").removeClass("show").empty();
        }
    });
    
    $("#search-button").click(function(e) {
        e.preventDefault();
        let location = $("#search-bar").val();
        var parts = location.split(", ");
        
        var city = "";
        var state = "";
        var country = "";
        
        if (parts.length === 2) {
            city = parts[0];
            state = "";
            country = parts[1];
        } else if (parts.length === 3) {
            city = parts[0];
            state = parts[1];
            country = parts[2];            
        }
        else {
            return;
        }

        $.ajax({
            url: "forecast/api",
            data: {city:city, state:state, country:country, days:"3"},
            success: function (response) {
                console.log(response)
                $("#weather-container").empty()
                $("#location-name").text(`${response.city}, ${response.country}`);
                fillWeatherCard(response);
            }
        })
    });
});
