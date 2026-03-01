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
    
    $("#search-button").on("click", function(e) {
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
    });
});
