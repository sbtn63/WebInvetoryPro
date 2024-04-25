function confirmarEliminar(url) {
    var respuesta = confirm("¿Estás seguro de que deseas este producto?");
    if (respuesta === true) {
      window.location.href = url;
    }
}