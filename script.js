const button = document.getElementById("generateBtn");

button.addEventListener("click", async () => {

    const planet = document.getElementById("planetType").value;
    const habitat = document.getElementById("habitat").value;
    const iq = document.getElementById("iq").value;
    const body = document.getElementById("body").value;

    

    document.getElementById("alienName").textContent =
        "Locating...";

    document.getElementById("description").textContent =
        "Generating species...";

    document.getElementById("culture").textContent =
        "Studying alien biology...";

    document.getElementById("quote").textContent =
        "...";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/generate",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    planet,
                    habitat,
                    iq,
                    body
                })

            }
        );

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        

        document.getElementById("alienName").textContent =
            data.name;

        document.getElementById("homeWorld").textContent =
            data.home_world;

        document.getElementById("lifeSpan").textContent =
            data.life_span;

        document.getElementById("threatLevel").textContent =
            data.threat_level;

        document.getElementById("bodyTypeText").textContent =
            data.body_type;

        document.getElementById("specialTrait").textContent =
            data.special_trait;

        document.getElementById("description").textContent =
            data.description;

        document.getElementById("culture").textContent =
            data.biology;

        document.getElementById("quote").textContent =
            `"${data.quote}"`;

        

        const alienImage = document.getElementById("alienImage");
        const planetImage = document.getElementById("planetImage");

        if (alienImage) {
            alienImage.src = data.alien_image;
        }

        if (planetImage) {
            planetImage.src = data.planet_image;
        }

    }

    catch (error) {

        console.error(error);

        alert("Backend not responding.");

    }

});