<script type="text/javascript">
$(document).ready(function(){

   	// campo desabilitado
   	$('#Usuario').attr("disabled", true);
   	// cor de fundo para o campo
   	$('#Usuario').css("background-color", "#cccccc");

   

	    	$("#op").click(function (){ 
           	// habilitando o campo
           	$('#usuario').attr("disabled", true);
           	// retornando a cor padrao
           	$('#usuario').css("background-color", "#cccccc");
   	});
 });
</script>