/**
    handle user input.
*/

const headerPopup = new PopupHeaderList();
const popupTable = new AuthenticationTablePopup();

headerPopup.initialize();
popupTable.initialize();

const requestButton = document.getElementById("send-request");
const requestMethod = document.getElementById("method-sel");
const requestPath = document.getElementById("route-sel");
const resultBox = document.getElementById("request-result");

requestButton.onclick = async function (e) {
    // clear last result
    resultBox.innerHTML = "";

    // send request, display result
    try {
        const response = await httpRequest(requestMethod.value, "/api/" + requestPath.value, {}, headerPopup.getHeaders());
        resultBox.innerHTML = JSON.stringify(response, null, 2);
    } catch (ex) {
        resultBox.innerHTML = ex;
        console.log(ex)
    }
}