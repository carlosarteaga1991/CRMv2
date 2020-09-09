
$(function () {
  $('#data').DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      deferRender: true,
      ajax: {
          url: window.location.pathname,
          type: 'POST',
          data: {
              'action': 'searchdata'
          },
          dataSrc: ""
      },
      columns: [
          {"data": "id_departamento"},
          {"data": "nombre"},
          {"data": "opciones"},
      ],
      columnDefs: [
          {
              targets: [-1],
              class: 'text-center',
              orderable: false,
              render: function (data, type, row) {
                  var buttons = '<a href="/cobros/departamento/actualizar/'+ row.id_departamento +'/" class="btn btn-warning" title="Editar"><i class="fas fa-edit"></i></a> ';
                  buttons += '<a href="/cobros/departamento/borrar/'+ row.id_departamento +'/"  class="btn btn-danger btn-borrar" title="Borrar" ><i class="fas fa-trash-alt"></i></a>';
                  return buttons;
              }
          },
      ],
      initComplete: function (settings, json) {

      }
  });
});

