
$(document).ready(function() {
    $("#weatherForm").on("submit", function(e) {
        e.preventDefault(); // Empêche le comportement par défaut du formulaire
        let city = $("#city").val().toLowerCase().replace(/[-']/g, ' ').replace(/saint/g, 'st');
        let date = $("#date").val();

        const date_str = new Date(date);
        const today = new Date();
        const oneWeekLater = new Date();
        oneWeekLater.setDate(today.getDate() + 8);

        if (isNaN(date_str.getTime()) || date_str < today || date_str > oneWeekLater) {
            console.log('Date invalide ou en dehors de la plage autorisée.');
            return;
        }

        const formattedDate = ('0' + date_str.getDate()).slice(-2) + '-' + ('0' + (date_str.getMonth() + 1)).slice(-2) + '-' + date_str.getFullYear();

        // Utilisation de la fonction jQuery AJAX pour récupérer les données météo
        $.ajax({
            url: "http://localhost:8888/mateo/" + city + '/?date_str=' + formattedDate,
            type: "GET",
            success: function(data) {
                // Affiche les informations météo
                $("#weatherInfo").html(data.response);
                // Génération du texte et lecture de l'audio
                const audio = new Audio("data:audio/mp3;base64," + data.audio);
                audio.play();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
