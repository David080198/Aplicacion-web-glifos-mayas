//document.getElementById("ventanas_busqueda_atributos").style.display = "none";

function llevar_a_otro(elemento)
{
    console.log("***********************************************************");
    console.log("Ejecutando funcion abrir()")
    console.log(elemento);
    var numero_thomson = "";
    var referencia_fonetica = "";
    var transcripcion = "";
    var traduccion ="";
    var comentario_de_montgomery ="";
    var datos_unidos = elemento;
    var elementos_separados = datos_unidos.split("####");
    console.log("Los elementos separados son: " + elementos_separados);
    /*console.log(elementos_separados[1]);
    console.log(elementos_separados[2]);
    console.log(elementos_separados[3]);
    console.log(elementos_separados[4]);
    console.log(elementos_separados[5]);
    console.log(elementos_separados[6]);*/

    //document.getElementById("ventanas").style.display="block";
    //document.getElementById("ventanas").style.zIndex ="40";
    //document.getElementById("ventanas").style.animationName="ventana_modal_animacion-abrir";
    //document.getElementById("ventanas").style.animationDuration="1s";
    //document.getElementById("ventanas").style.display="grid";

    /*console.log(elementos_separados[3]);*/
    numero_thomson = limpiar(elementos_separados[3]);

    /*console.log(elementos_separados[4]);*/
    referencia_fonetica = limpiar(elementos_separados[4]);

    /*console.log(elementos_separados[6]);*/
    transcripcion = limpiar(elementos_separados[6]);

    /*console.log(elementos_separados[5]);*/
    traduccion = limpiar(elementos_separados[5]);

    /*console.log(elementos_separados[2]);*/
    comentario_de_montgomery = limpiar(elementos_separados[2]);
    
    //document.getElementById("texto-thomson-number").innerHTML = numero_thomson;
    //document.getElementById("texto-referencia-fonetica").innerHTML = referencia_fonetica;
    //document.getElementById("texto-info-transcripcion").innerHTML = transcripcion;
    //document.getElementById("texto-info-traduccion").innerHTML = traduccion;
    //document.getElementById("texto-info-montgomery").innerHTML = comentario_de_montgomery;
    var enlace = window.location.pathname;
    var enlace_anterior = window.location.hash;
    console.log(enlace_anterior);
    enlace_anterior_final = "";
    for(i=1;i<enlace_anterior.length;i++)
    {
        enlace_anterior_final +=  enlace_anterior[i];
    }
    document.getElementById(enlace_anterior_final).style.background = "white";
    document.getElementById(elementos_separados[0]).style.background="rgb(39,110,144)";
    var enlace_final = enlace + "#"+ elementos_separados[0];
    location.href = enlace_final;
}

function abrir(elemento)
{
    console.log("***********************************************************");
    console.log("Ejecutando funcion abrir()")
    console.log(elemento);
    var numero_thomson = "";
    var referencia_fonetica = "";
    var transcripcion = "";
    var traduccion ="";
    var comentario_de_montgomery ="";
    var datos_unidos = elemento;
    var elementos_separados = datos_unidos.split("####");
    console.log("Los elementos separados son: " + elementos_separados);
    /*console.log(elementos_separados[1]);
    console.log(elementos_separados[2]);
    console.log(elementos_separados[3]);
    console.log(elementos_separados[4]);
    console.log(elementos_separados[5]);
    console.log(elementos_separados[6]);*/

    document.getElementById("ventanas").style.display="block";
    document.getElementById("ventanas").style.zIndex ="40";
    document.getElementById("ventanas").style.animationName="ventana_modal_animacion-abrir";
    document.getElementById("ventanas").style.animationDuration="1s";
    document.getElementById("ventanas").style.display="grid";

    /*console.log(elementos_separados[3]);*/
    numero_thomson = limpiar(elementos_separados[3]);

    /*console.log(elementos_separados[4]);*/
    referencia_fonetica = limpiar(elementos_separados[4]);

    /*console.log(elementos_separados[6]);*/
    transcripcion = limpiar(elementos_separados[6]);

    /*console.log(elementos_separados[5]);*/
    traduccion = limpiar(elementos_separados[5]);

    /*console.log(elementos_separados[2]);*/
    comentario_de_montgomery = limpiar(elementos_separados[2]);
    
    document.getElementById("texto-thomson-number").innerHTML = numero_thomson;
    document.getElementById("texto-referencia-fonetica").innerHTML = referencia_fonetica;
    document.getElementById("texto-info-transcripcion").innerHTML = transcripcion;
    document.getElementById("texto-info-traduccion").innerHTML = traduccion;
    document.getElementById("texto-info-montgomery").innerHTML = comentario_de_montgomery;
    var enlace = window.location.pathname;
    var enlace_anterior = window.location.hash;
    console.log(enlace_anterior);
    enlace_anterior_final = "";
    for(i=1;i<enlace_anterior.length;i++)
    {
        enlace_anterior_final +=  enlace_anterior[i];
    }
    document.getElementById(enlace_anterior_final).style.background = "white";
    document.getElementById(elementos_separados[0]).style.background="rgb(39,110,144)";
    var enlace_final = enlace + "#"+ elementos_separados[0];
    location.href = enlace_final;
}



function cerrar()
{
    document.getElementById("ventanas").style.animationName="ventana_modal_animacion-cerrar";
    document.getElementById("ventanas").style.animationDuration="4s";
    document.getElementById("ventanas").style.animationDirection="normal";
    document.getElementById("ventanas").style.animationFillMode="forwards";
}

function cerrar_atributos()
{
    document.getElementById("ventanas_busqueda_atributos").style.animationName="ventana_modal_cerrar_atributos";
    document.getElementById("ventanas_busqueda_atributos").style.animationDuration="1s";
    document.getElementById("ventanas_busqueda_atributos").style.animationFillMode="forwards";
}

function cerrar_nuevo_usuario()
{
    document.getElementById("ventana_ingresar_nuevo_usuario").style.animationName="ventana_modal_cerrar_atributos";
    document.getElementById("ventana_ingresar_nuevo_usuario").style.animationDuration="1s";
    document.getElementById("ventana_ingresar_nuevo_usuario").style.animationFillMode="forwards";
}

function limpiar(elemento_limpiar)
{
    var elemento_limpio="";
    for(i=0;i<elemento_limpiar.length;i++)
    {
        if(elemento_limpiar[i] != "(" && elemento_limpiar[i] != ")", elemento_limpiar[i] != "'")
        {
            elemento_limpio += elemento_limpiar[i];
        }
    }
    return elemento_limpio;
}

function menor(total_datos)
{
    var link_actual = "";
    var link_actual_hash="";
    var valor_id ="";
    var link_actual = window.location.pathname;
    var link_actual_hash = window.location.hash;
    for(i=1;i<link_actual_hash.length;i++)
    {
      valor_id += link_actual_hash[i];
    }
    document.getElementById(valor_id).style.background = "white";
    document.getElementById("1").style.backgroundColor = "rgb(39,110,144)";
    location.href = link_actual + "#" + "1";
}

function mayor(total_datos)
{
   link_actual = "";
   link_actual_hash = "";
   valor_id = "";
   total_datos_limpio = "";
   var link_actual = window.location.pathname;
   var link_actual_hash = window.location.hash;
   for(i=1;i<link_actual_hash.length;i++)
   {
      valor_id += link_actual_hash[i];
   }
   for(i=1;i<(total_datos.length-1);i++)
   {
      total_datos_limpio += total_datos[i];
   }
   document.getElementById(valor_id).style.background = "white";
   location.href = link_actual + "#" + total_datos_limpio;
   document.getElementById(total_datos_limpio).style.backgroundColor = "rgb(39,110,144)";
}


function sumar(total_datos)
{
   var valor_id = "";
   var total_datos_limpio = "";
   var link_actual = window.location.pathname;
   var link_actual_hash = window.location.hash;
   var link_actual_total = link_actual + link_actual_hash;
   for(i=1;i<link_actual_hash.length;i++)
   {
      valor_id += link_actual_hash[i];
   }
   valor_id = parseInt(valor_id);
   for(i=1;i<(total_datos.length-1);i++)
   {
      total_datos_limpio += total_datos[i];
   }
   if(valor_id < total_datos_limpio && valor_id>=1)
   {
    document.getElementById(valor_id).style.backgroundColor = "white";
    valor_id = valor_id+1;
    location.href = window.location.pathname + "#" + valor_id;
    document.getElementById(valor_id).style.backgroundColor = "rgb(39,110,144)";
   }
}

function restar(total_datos)
{
   var valor_id = "";
   var total_datos_limpio ="";
   var link_actual = window.location.pathname;
   var link_actual_hash = window.location.hash;
   var link_actual_total = link_actual + link_actual_hash;
   for(i=1;i<link_actual_hash.length;i++)
   {
      valor_id += link_actual_hash[i];
   }
   valor_id = parseInt(valor_id);
   for(i=1;i<(total_datos.length-1);i++)
   {
      total_datos_limpio += total_datos[i];
   }
   if((valor_id-1)!=0)
   {
    if(valor_id <= total_datos_limpio && valor_id>=1)
    {
        document.getElementById(valor_id).style.backgroundColor = "white";
        valor_id = valor_id-1;
        location.href = window.location.pathname + "#" + valor_id;
        document.getElementById(valor_id).style.backgroundColor = "rgb(39,110,144)";
    }
   }
   else{
     valor_id=1;
     document.getElementById(valor_id).style.backgroundColor = "rgb(39,110,144)";
   }
}

function orden_datos(orden,dato)
{

    enlace = window.location.href


    enlace_actual = window.location.href
    enlace_actual_1 = window.location.hostname
    enlace_actual_2 = window.location.pathname
    enlace_actual_3 = window.location.protocol
    var url = new URL(enlace_actual);
    var result = url.port;


    enlace_pc_1 = enlace_actual_3 + "//" + enlace_actual_1 + ":" + result + "/index/" + orden + "/" + dato + "/default/default/default/#1"
    console.log(enlace_pc_1)
    

    window.location.replace(enlace_pc_1);
    //window.location.replace("http://127.0.0.1/index/"+ orden + "/" + dato + "/default/default/default/#1");
}

function orden_datos_invitado(orden,dato)
{

    enlace = window.location.href


    enlace_actual = window.location.href
    enlace_actual_1 = window.location.hostname
    enlace_actual_2 = window.location.pathname
    enlace_actual_3 = window.location.protocol
    var url = new URL(enlace_actual);
    var result = url.port;


    enlace_pc_1 = enlace_actual_3 + "//" + enlace_actual_1 + ":" + result + "/index_invitado/" + orden + "/" + dato + "/default/default/default/#1"
    console.log(enlace_pc_1)
    

    window.location.replace(enlace_pc_1);
    //window.location.replace("http://127.0.0.1/index/"+ orden + "/" + dato + "/default/default/default/#1");
}
