document.addEventListener('DOMContentLoaded', function () {


    fetch('/follows-user', {

    })
        .then(response => response.json())
        .then(result => {

            id = document.querySelector('#Usuario').dataset.id

            for (i = 0; i < result.SeguidosU.length; i++) {

                if (id == result.SeguidosU[i]) {
                    document.getElementById('Follow').checked = true

                }

            }


        });

})



