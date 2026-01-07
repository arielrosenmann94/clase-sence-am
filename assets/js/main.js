//function accesoEspecial() {
//  const nombre = prompt("Ingresa tu nombre:");
//  const clave = prompt("Ingresa tu contraseña:");
//
//  const esAdmin = nombre === "Ariel";
//  const tieneClave = clave === "123"; // la clave que ingrese debe ser 123 
//
//  if (esAdmin && tieneClave) {
//    console.log("Acceso permitido");
//  } else {
//    alert("Acceso denegado");
//  }
//}
//
//accesoEspecial();


//document.addEventListener("mouseout", function (event) {
//    if (event.clientY < 10) {
//      alert("¡No te vayas aún! Tenemos una oferta imperdible para ti 🤩");
//    }
//  });
//
//function saludarSegunHora() {
//  const ahora = new Date();           // Obtenemos fecha y hora actual
//  const hora = ahora.getHours();      // Hora en formato 24h
//  const minutos = ahora.getMinutes(); // También podemos mostrar los minutos
//
//  const horaTexto = hora.toString().padStart(2, '0') + ":" + minutos.toString().padStart(2, '0');
//
//  if (hora >= 6 && hora < 12) {
//    alert("¡Buenos días! Son las " + horaTexto);
//  } else if (hora >= 12 && hora < 20) {
//    alert("¡Buenas tardes! Son las " + horaTexto);
//  } else {
//    alert("¡Buenas noches! Son las " + horaTexto);
//  }
//}
//
//saludarSegunHora();
//

// Lista de nombres masculinos y femeninos
  const nombres = [
    "Juan", "Pedro", "Luis", "Carlos", "Andrés", "Martín", "Lucía", "Camila", "Valentina", "Josefa",
    "Florencia", "Carla", "Sofía", "Javiera", "Fernanda"
  ];

  let stock = 100; // Stock inicial

  function compraAleatoria() {
    if (stock <= 0) {
      alert("¡Stock agotado!");
      return;
    }

    // Elegimos un nombre al azar
    const nombre = nombres[Math.floor(Math.random() * nombres.length)];

    // Mostrar la alerta con el nombre
    alert(`${nombre} hizo esta compra. ¡No te quedes sin el tuyo! Quedan ${stock - 1} unidades.`);

    // Descontamos del stock
    stock--;

    // Elegimos un tiempo aleatorio entre 1 y 15 segundos
    const tiempo = Math.floor(Math.random() * (15000 - 1000 + 1)) + 1000;

    // Repetimos la función después del tiempo aleatorio
    setTimeout(compraAleatoria, tiempo);
  }

  // Iniciar la primera compra
  compraAleatoria();

     



    //let rut = 18641544;
    //let digitoVerificador = 4;
    //console.log("¿que tipo de dato es el rut?");
    //console.log(typeof rut);
    //console.log(typeof digitoVerificador);
//
    //rut = String(rut);
//
    //digitoVerificador = String(digitoVerificador);
//
    //let rutCompleto = rut + "-" + digitoVerificador;
    //console.log("este es el rut completo:");
    //console.log(rutCompleto);


   //let pi = "3.14";
   //console.log(typeof pi)
   //pi = parseFloat(pi);
   //console.log(typeof pi)
   //console.log(tipoNumero(pi))

    //let nombre = "Ariel";
    //let apellido = "Rosenmann";
//
    //let nombreCompleto = "Hola, " + nombre + " " + apellido + "!";
    //console.log(nombreCompleto);
//
    //nombre = "juan";
    //apellido = "Perez";
//
    //nombreCompleto = `Hola, ${nombre} ${apellido}!`;
    //1  2  3  4  5 6  7  8  9   10  11  12  13  14  15
    //{} [] () ! /  *  +  -  ""  ''  ``  =   ;   .   &   |

    //let nombre = prompt("ingresa tu nombre:")
    //alert(`hola, ${nombre}`)
//
    //console.log(nombreCompleto);


    //let x = 5;
    //let y = 10;


    //console.log(5 === "5"); // falso
    //console.log(5 == "5"); // verdadero
//
    //console.log(5 == "5" && 5 === "5"); // ---> Falso
//  //             verdadero   Falso
//
    //console.log(5 == "5" || 5 === "5"); // ---> Verdadero
//              verdadero   Falso

//let user = "ariel";
//let hora = 13;
//
//  if (hora < 12) {
// alert(`Buenos días ${user}`);
//} else {
// console.log("buenas tardes");}




    //console.log(x < y); // true
//
    //console.log(x > y); //false
//
    //x = 10
//
    //console.log(x <= y) // true
//
    //x++; // 11
//
    //console.log(x >= y) //true

    //console.log(x == y); //¿Es x iagual a y?
//
    //console.log(x === y); //  es igual el caracter y el tipo de dato?
//
    //console.log(x != y); // es diferente x a y? 
//
    //console.log(x !== y); // es diferente el caracter o el tipo de datos ?


    

    




    console.log("mostrar este texto al final del archivo");