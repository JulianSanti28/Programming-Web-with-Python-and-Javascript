document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  //Lógica cuandi se envíe el formulario
  document.querySelector('#compose-form').onsubmit = function () {

    const dest = document.querySelector('#compose-recipients').value;
    const asunt = document.querySelector('#compose-subject').value;
    const content = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST', body: JSON.stringify({
        recipients: dest,
        subject: asunt,
        body: content
      })
    })
      .then(response => response.json())
      .then(result => {

        if (result.message) {

          document.querySelector('#responseE').style.display = 'none';
          document.querySelector('#response').style.display = 'block';
          document.querySelector('#result').innerHTML = result.message;

          load_mailbox('sent');

        } else if (result.error) {

          document.querySelector('#response').style.display = 'none';
          document.querySelector('#responseE').style.display = 'block';
          document.querySelector('#resultE').innerHTML = result.error;


          load_mailbox('sent');



        }
      });

    return false;

  }

  // By default, load the inbox
  load_mailbox('inbox');

});



function compose_email() {

  var div = document.getElementById('archivedInb');
  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }

  //Ocultando elementos
  document.querySelector('#responseE').style.display = 'none';
  document.querySelector('#response').style.display = 'none';
  document.querySelector('#emls').style.display = 'none';


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  //Activando elementos (desactivados cuando se consulta un email)
  document.querySelector('#compose-subject').disabled = false;
  document.querySelector('#compose-body').disabled = false;
  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#btnTest').style.display = 'block';
  document.querySelector('#newE').style.display = 'block';
  document.querySelector('#compose-sender').style.display = 'block';
  document.querySelector('#inb').innerHTML = "";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  var div = document.getElementById('archivedInb');
  while (div.firstChild) {
    div.removeChild(div.firstChild);
  }

  document.querySelector('#emls').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  if (mailbox === 'sent') {


    document.querySelector('#emls').style.display = 'block';
    var div = document.getElementById('emls');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }

    fetch('/emails/sent')
      .then(response => response.json())
      .then(emails => {

        //Recorrer los emails

        for (i = 0; i < emails.length; i++) {

          const element = document.createElement('li');
          element.id = emails[i].id;
          element.className = 'elemento';


          //Se agrega ele lemento al cuerpo de la página con su ID
          element.innerHTML = emails[i].recipients[0] + "   " + " → " + emails[i].subject + "" + " → " + emails[i].timestamp;
          element.addEventListener('click', function () {

            const mail = '/emails/' + element.id;
            load_details('details', mail, false, false);

          });



          document.querySelector('#emls').append(element);

        }

      });



  }

  if (mailbox === 'inbox') {

    document.querySelector('#emls').style.display = 'block';
    var div = document.getElementById('emls');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }

    fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {

        for (i = 0; i < emails.length; i++) {

          const element = document.createElement('li');
          element.className = 'elemento';
          element.id = emails[i].id;
          //Se agrega ele lemento al cuerpo de la página con su ID
          element.innerHTML = emails[i].sender + "   " + "  → " + emails[i].subject + "" + " → " + emails[i].timestamp;
          element.addEventListener('click', function () {

            const mail = '/emails/' + element.id;
            load_details('details', mail, true, false);
          });

          if (emails[i].read == true) {
            element.style.background = 'rgb(164, 164, 164)';
          }

          document.querySelector('#emls').append(element);

        }

      });



  }


  if (mailbox === 'archive') {

    document.querySelector('#emls').style.display = 'block';
    var div = document.getElementById('emls');
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }

    fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {

        for (i = 0; i < emails.length; i++) {

          const element = document.createElement('li');
          element.className = 'elemento';
          element.id = emails[i].id;
          //Se agrega ele lemento al cuerpo de la página con su ID
          element.innerHTML = emails[i].sender + "   " + "  → " + emails[i].subject + "" + " → " + emails[i].timestamp;
          element.addEventListener('click', function () {

            const mail = '/emails/' + element.id;
            load_details('details', mail, false, true);
          });

          document.querySelector('#emls').append(element);

        }

      });



  }



}

//Función para mostrar los detalles de un correo
//Parámetros: Título de la vista, email (para envíar a la APi)
function load_details(mailbox, email, flag, archived) {

    


  //Ocultar vistas que no son necesarias
  document.querySelector('#emls').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'block';


  // Show the mailbox name

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(email)
    .then(response => response.json())
    .then(email => {
      //Agregando el contenido del email y deshabilitando la opción de editar, además ocultar elementos que no son necesarios
      if (flag) {
        //Ocultar vista
        document.querySelector('#compose-sender').style.display = 'none';
        //Llenar el campo from
        document.querySelector('#inb').innerHTML = email.sender;

        //Responder correo
        const reply = document.createElement('button');
        reply.className = 'archived';
        reply.innerHTML = "Reply";
        reply.addEventListener('click', function () {

          //Eliminando elementos hijos del div con id='archivedInb'
          var div = document.getElementById('archivedInb');
          while (div.firstChild) {
            div.removeChild(div.firstChild);
          }



          //Ocultando elementos
          document.querySelector('#responseE').style.display = 'none';
          document.querySelector('#response').style.display = 'none';
          document.querySelector('#emls').style.display = 'none';


          // Show compose view and hide other views
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'block';

          //Activando elementos (desactivados cuando se consulta un email)
          document.querySelector('#compose-subject').disabled = false;
          document.querySelector('#compose-body').disabled = false;
          document.querySelector('#compose-recipients').disabled = true;
          document.querySelector('#btnTest').style.display = 'block';
          document.querySelector('#newE').style.display = 'block';
          document.querySelector('#compose-sender').style.display = 'block';
          document.querySelector('#inb').innerHTML = "";

          // Clear out composition fields - replace recipients
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = 'Re:' + email.subject;
          document.querySelector('#compose-body').value = '';



        });
        document.querySelector('#archivedInb').append(reply);


        //Archivar el correo
        const element = document.createElement('button');
        element.className = 'archived';
        element.innerHTML = "Archive";
        element.addEventListener('click', function () {
          const mail = '/emails/' + email.id;

          fetch(mail, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true


            })

          })

          //Espera un tiempo para ejecutar la función
          setTimeout(function () {
            load_mailbox('inbox');
          }, 100);
        });
        document.querySelector('#archivedInb').append(element);
      }

      if (archived) {

        document.querySelector('#compose-sender').style.display = 'none';
        document.querySelector('#inb').innerHTML = email.sender;

        const element = document.createElement('button');
        element.className = 'archived';
        element.innerHTML = "Unarchived";
        element.addEventListener('click', function () {
          const mail = '/emails/' + email.id;

          fetch(mail, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false

            })


          })


          setTimeout(function () {
            load_mailbox('inbox');
          }, 100);




        });
        document.querySelector('#archivedInb').append(element);

      }

      document.querySelector('#compose-recipients').value = email.recipients[0];
      document.querySelector('#compose-subject').value = email.subject;
      document.querySelector('#compose-body').value = email.body;

      document.querySelector('#compose-subject').disabled = true;
      document.querySelector('#compose-body').disabled = true;
      document.querySelector('#compose-recipients').disabled = true;
      document.querySelector('#btnTest').style.display = 'none';
      document.querySelector('#newE').style.display = 'none';
    });

}