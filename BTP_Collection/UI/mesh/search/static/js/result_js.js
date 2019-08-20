function left()
{
  var page = 0;
  if("p" in getUrlVars())
    page = parseInt(getUrlVars()["p"]);
  if("q" in getUrlVars())
    var query = getUrlVars()["q"];
  if(page > 0)
  {
    page = page-1;
    window.location.href = "/results/?q="+query+"&p="+page;
  }
}

function right()
{
  var page = 0;
  if("p" in getUrlVars())
    page = parseInt(getUrlVars()["p"]);
  if("q" in getUrlVars())
    var query = getUrlVars()["q"];
  page = page+1;
  window.location.href = "/results/?q="+query+"&p="+page;
}
