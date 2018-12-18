$(function () {
    console.log("Notifications start");
    setTimeout(updateNotification, 100);
})

function updateNotification() {
    // code
    console.log("looking for notifs");

    var notifRequest = new XMLHttpRequest();
    notifRequest.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(notifRequest.responseText)

            notifPanel = document.getElementById("notifPanel")

            if (response.length === 0) {
                notifPanel.innerHTML = '<li class="nav-item"> \
                                        <a class="nav-link disabled" href="#">No Notifications</a> \
                                        </li>"'
            } else {
                html = '<li class="nav-item dropdown active">'
                html += '<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \
                        Notifications <span class = "badge badge-light" >' + response.length + '</span></a>'

                html += '<div class="dropdown-menu" style="width: 25rem" aria-labelledby="navbarDropdown">'
                for (notif of response) {
                    html += '<a href=/main_app/' + notif.question_url + ' class="list-group-item list-group-item-action flex-column align-items-start">'

                    html += '<div class="d-flex w-100 justify-content-between">'
                    html += '<h5 class="mb-1">' + notif.by + '</h5>'
                    html += '<small class="text-muted">' + '</small>'
                    html += '</div>'

                    html += '<p class="mb-1">' + notif.by + ' posted an answer to the question : <strong>' + notif.question + '</strong> </p>'
                    html += '</a>'
                }
                html += '</div>'
                html += '</li>'
                notifPanel.innerHTML = html
            }

        }
    }

    notifRequest.open('get', '/main_app/api/notif/', true);
    notifRequest.send()


    setTimeout(updateNotification, 5000);
}