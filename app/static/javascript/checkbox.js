$('#check').change(function() {
    if(this.checked != true){
          $("#sous_check").hide();
     }
  else{
        $("#sous_check").show();
  }
});