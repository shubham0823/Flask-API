$(document).ready(function () {
    $("#search-btn").click(function () {
        var input_string = $("#search-input").val();

        $.ajax({
            url: "http://127.0.0.1:5000/", // Replace with your Flask API's URL
            type: "POST",
            data: { input_string: input_string },
            success: function (response) {
                let results_html = '';
                console.log(response.response)
                response.response.forEach(result => {
                    results_html += `<div class="result">`;
                    // Iterate through each key-value pair
                    for (const [key, value] of Object.entries(result)) {
                        if (key === 'extracted_links' && value.length > 0) {
                            results_html += `<p><strong>${key}:</strong></p><ul>`;
                            value.forEach(link => {
                                results_html += `<li><a href="${link}" target="_blank">${link}</a></li>`;
                            });
                            results_html += '</ul>';
                        } else {
                            results_html += `<p><strong>${key}:</strong> ${value}</p>`;
                        }
                    }

                    results_html += '</div>';
                });
                $("#processed-data").html("<h3>Processed Data:</h3><br><br>" + results_html);
            },
            error: function (error) {
                $("#results").html("Error: " + error.message);
            }
        });
    });
});
