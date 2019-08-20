function getUrlVars()
{
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value)
    {
        vars[key] = value;
    });
    return vars;
}

function search(e, field)
{
  var code = (e.keyCode ? e.keyCode : e.which);
  if(code == 13)
  {
    var urlQuery = getUrlVars()["q"];
    var fieldQuery = field.value;
    if(urlQuery != fieldQuery)
      window.location.href = "/results/?q="+fieldQuery;
  }
}
