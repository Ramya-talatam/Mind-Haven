function analyzeJournal() {
    var journalText = document.getElementById("journalInput").value;
    var reportElement = document.getElementById("report");
    reportElement.innerHTML = "";
    const journalApi = 'https://mind-haven.vercel.app/analyze';
    // const journalApi = '../../analyze';
    // Send journal text to server for analysis
    fetch(journalApi, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'journalText=' + encodeURIComponent(journalText)
    })
    .then(response => {
        // console.log('Response:', response);
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        return response.json();
    })
    .then(data => {
        // console.log('Data from server:', data);
        var positiveWords = data.positive_words;
        var negativeWords = data.negative_words;
        var focusedWords = data.focused_words;
        var overallPolarity = data.overall_polarity;

        // Display positive words
        positiveWords.forEach(function(wordObj) {
            var wordElement = document.createElement("span");
            wordElement.className = "word positive";
            wordElement.style.fontSize = (wordObj[1] * 200 + 100) + "%";
            wordElement.innerText = wordObj[0] + " ";
            reportElement.appendChild(wordElement);
        });
        reportElement.innerHTML += "<hr>";
        // Display negative words
        negativeWords.forEach(function(wordObj) {
            var wordElement = document.createElement("span");
            wordElement.className = "word negative";
            wordElement.style.fontSize = (wordObj[1] * -200 + 100) + "%";
            wordElement.innerText = wordObj[0] + " ";
            reportElement.appendChild(wordElement);
        });
        reportElement.innerHTML += "<hr>";
        // Display focused words
        focusedWords.forEach(function(word) {
            var wordElement = document.createElement("span");
            wordElement.className = "word neutral";
            wordElement.innerText = word + " ";
            reportElement.appendChild(wordElement);
        });
        reportElement.innerHTML += "<hr>";
        // Display overall polarity
        var polarityElement = document.createElement("p");
        polarityElement.innerText = "Overall Polarity: " + overallPolarity;
        reportElement.appendChild(polarityElement);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
