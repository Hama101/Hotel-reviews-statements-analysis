// grab the analyse - btn and add a click event listener to it to run the analyse function
// the analyse function call the "/analyse-text" route and send the text to the server with formdata and get the response
// the response is then displayed in textOutput textarea

Object.prototype.prettyPrint = function(){
    var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
    var replacer = function (match, pIndent, pKey, pVal, pEnd) {
        var key = '<span class="json-key" style="color: brown">',
            val = '<span class="json-value" style="color: navy">',
            str = '<span class="json-string" style="color: olive">',
            r = pIndent || '';
        if (pKey)
            r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
        if (pVal)
            r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
        return r + (pEnd || '');
    };

    return JSON.stringify(this, null, 3)
        .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
        .replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(jsonLine, replacer);
}


function analyse(event) {
    event.preventDefault();
    console.log("analyse btn clicked");
    let text = document.getElementById("text-input").value;
    let formData = new FormData();
    formData.append("text", text);
    fetch("/analyse-text", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // convert the data to a string with indentations and display it in the textOutput textarea 
        // let textOutput = JSON.stringify(data, null, 4);
        document.getElementById("text-output").innerHTML = data.prettyPrint();
    })
}
