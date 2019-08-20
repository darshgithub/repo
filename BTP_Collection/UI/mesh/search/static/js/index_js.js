function send()
{
  var query = document.getElementById("query").value;
  window.location.href = '/results/?q=' + query;
}
