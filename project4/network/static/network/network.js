/* Código JavaScript */
document.addEventListener('DOMContentLoaded', function () {

    fetch('/likes-user', {

    })
        .then(response => response.json())
        .then(result => {

            document.querySelectorAll('label').forEach(label => {

                for (i = 0; i < result.LikesU.length; i++) {

                    if (label.id == result.LikesU[i]) {
                        document.getElementById(label.dataset.check).checked = true
                        label.style.color = 'red';
                    }

                }


            })



        });


    document.querySelectorAll('h5').forEach(h5 => {

        h5.onclick = function () {

            if (this.innerHTML == 'Edit') {


                text_area = 'text' + ' ' + this.id;

                document.getElementById(text_area).style.display = 'block';
                this.innerHTML = "Save"

            } else if (this.innerHTML == 'Save') {

                text_area = 'text' + ' ' + this.id;

                descripcion = document.getElementById(text_area).value;
                //Obteniendo el ID de la publicación
                var array = this.id.split(' ');
                publicacion_id = array[1];
                url = '/edit_post/' + publicacion_id

                //Realizo la solicitud al servidor

                fetch(url, {
                    method: 'PUT', body: JSON.stringify({
                        descripcion: descripcion
                    })
                })
                    .then(response => response.json())
                    .then(result => {
                        //Actualizando el campo en el cuerpo
                        desc_actualizar = 'desc' + ' ' + publicacion_id;
                        document.getElementById(desc_actualizar).innerHTML = result.descripcion;
                        //Reiniciando valores
                        document.getElementById(text_area).style.display = 'none';
                        this.innerHTML = 'Edit';


                    });





            }




        }

    })


    document.querySelectorAll('label').forEach(label => {

        let aux = 0;


        label.onclick = function () {

            if (this.id === "AddFollow") {


                if (aux % 2 == 0) {


                    if (document.getElementById('Follow').checked == false) {

                        id = document.querySelector('#Usuario').dataset.id

                        url = '/follow/' + id

                        fetch(url, {
                            method: 'PUT'
                        })
                            .then(response => response.json())
                            .then(result => {

                                document.querySelector('#seguidores').innerHTML = "Followers:" + " " + result.seguidores;
                                document.querySelector('#seguidos').innerHTML = "Following:" + " " + result.seguidos;



                            });





                    } else {


                        id = document.querySelector('#Usuario').dataset.id

                        url = '/remove/follow/' + id

                        fetch(url, {
                            method: 'PUT'
                        })
                            .then(response => response.json())
                            .then(result => {

                                document.querySelector('#seguidores').innerHTML = "Followers:" + result.seguidores;
                                document.querySelector('#seguidos').innerHTML = "Following:" + result.seguidos;


                            });



                    }



                }
                aux++;
            } else {

                if (document.getElementById(this.dataset.check).checked == false) {

                    url = '/likes/' + this.id
                    fetch(url, {
                        method: 'PUT'
                    })
                        .then(response => response.json())
                        .then(result => {
                            this.innerHTML = "♡" + result.likes;
                            this.style.color = 'red';
                        });
                } else {
                    url = '/likes/delete/' + this.id
                    fetch(url, {
                        method: 'PUT'
                    })
                        .then(response => response.json())
                        .then(result => {

                            this.innerHTML = "♡" + result.likes;
                            this.style.color = 'white';

                        });



                }



            }






        };
    });





})
