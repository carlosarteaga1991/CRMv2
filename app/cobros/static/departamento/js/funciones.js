
// no se está usando
function fun_borrar(x,y) {
    /*ar fila= $(this).closest("tr");  
    var id = parseInt(fila.find('td:eq(0)').text()) 
    var nombre = fila.find('td:eq(1)').text()*/

    id = x;
    nombre = y;
    
    
    Swal.fire({
      title: '¿Seguro que desea borrar el registro: '+ nombre +'?',
      text: "¡Esta acción no se puede revertir!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '¡Sí, borrarlo!'
    }).then((result) => { 
      if (result.value == true) {
        try {
          //var fila= $(this).closxsest("tr"); 

          // inicio ajax
          //var parameters = $(this).serializeArray();
          
          $.ajax({
          data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()

          },
          url: '/cobros/departamento/borrar/'+id+'/',
          type: 'post',
          
          success: function (response) {
            console.log(data);
              Swal.fire(
                '¡Borrado!',
                'El registro ha sido eliminado satisfactoreamente.',
                'success'
              )
          },
          error: function (error) {
            Swal.fire(
            'Eoor!',
            'ha ocurrido un error.',
            'error'
            )
          }  
          

          });
          //fin ajax
         
          
        } catch( err ) {
          Swal.fire(
          'Eoor!',
          'ha ocurrido un error.'+ err +'',
          'error'
          )
        } 
    
      }
    })       

}