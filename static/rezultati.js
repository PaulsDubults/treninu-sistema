// Šī rinda definē globālo mainīgo grafika objektam.
let progressaGrafiks = null;

// Šī funkcija pieprasa datus no Flask JSON API.
async function ieladetGrafikaDatus(vingrinajumaId) {
    // Šī rinda izveido GET pieprasījumu uz konkrētā vingrinājuma API adresi.
    const atbilde = await fetch(`/api/rezultati/vingrinajums/${vingrinajumaId}`);

    // Šī rinda pārvērš saņemto atbildi JavaScript objektā.
    const dati = await atbilde.json();

    // Šī rinda atgriež saņemtos datus izsaucējam.
    return dati;
}

// Šī funkcija uzzīmē vai atjauno Chart.js grafiku.
async function uzzimetGrafiku() {
    // Šī rinda atrod nolaižamo sarakstu lapā.
    const izvele = document.getElementById("grafika_vingrinajums");

    // Šī rinda pārbauda, vai nolaižamais saraksts vispār eksistē.
    if (!izvele) {
        // Šī rinda pārtrauc funkciju, ja lapa nav rezultātu lapa.
        return;
    }

    // Šī rinda nolasa izvēlētā vingrinājuma ID.
    const vingrinajumaId = izvele.value;

    // Šī rinda pārbauda, vai ID ir izvēlēts.
    if (!vingrinajumaId) {
        // Šī rinda pārtrauc izpildi, ja nav ko ielādēt.
        return;
    }

    // Šī rinda pieprasa grafika datus no servera.
    const dati = await ieladetGrafikaDatus(vingrinajumaId);

    // Šī rinda atrod canvas elementu.
    const canvas = document.getElementById("progressaGrafiks");

    // Šī rinda iegūst 2D zīmēšanas kontekstu.
    const konteksts = canvas.getContext("2d");

    // Šī rinda pārbauda, vai vecais grafiks jau eksistē.
    if (progressaGrafiks) {
        // Šī rinda iznīcina veco grafiku pirms jaunā izveides.
        progressaGrafiks.destroy();
    }

    // Šī rinda izveido jaunu Chart.js line grafiku.
    progressaGrafiks = new Chart(konteksts, {
        // Šī rinda nosaka grafika tipu.
        type: "line",

        // Šī rinda definē grafika datus.
        data: {
            // Šī rinda iestata X ass etiķetes.
            labels: dati.labels,

            // Šī rinda iestata datu sērijas.
            datasets: [
                {
                    // Šī rinda nosaka sērijas nosaukumu.
                    label: "Svars kilogramos",

                    // Šī rinda iestata Y ass datus.
                    data: dati.data,

                    // Šī rinda ieslēdz aizpildīšanu zem līknes.
                    fill: false,

                    // Šī rinda iestata līknes gludumu.
                    tension: 0.2
                }
            ]
        },

        // Šī rinda definē papildu grafika iestatījumus.
        options: {
            // Šī rinda ļauj grafikam būt pielāgojamam ekrāna izmēram.
            responsive: true
        }
    });
}

// Šī rinda gaida pilnu HTML dokumenta ielādi.
document.addEventListener("DOMContentLoaded", () => {
    // Šī rinda atrod nolaižamo sarakstu.
    const izvele = document.getElementById("grafika_vingrinajums");

    // Šī rinda pārbauda, vai šī lapa satur grafika izvēli.
    if (izvele) {
        // Šī rinda uzzīmē grafiku pēc lapas ielādes.
        uzzimetGrafiku();

        // Šī rinda pievieno notikumu, lai grafiks atjaunotos pēc izvēles maiņas.
        izvele.addEventListener("change", uzzimetGrafiku);
    }
});
