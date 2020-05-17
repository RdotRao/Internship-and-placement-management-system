var flag = true;
function getAnyCity(chkboxName) {
    anyCityCheckbox = document.getElementById("Anycity")
    if(flag==true)
    {
        document.getElementById("id_cityofinterest").innerHTML = "Any City";
        flag = false;
    }
    else
    {
        document.getElementById("id_cityofinterest").innerHTML = "";
        flag = true;
    }
}

function getCheckedBoxes(chkboxName) {
    if(flag==true)
    {
        var checkboxes = document.getElementsByName(chkboxName);
        var checkboxesChecked = [];
        // loop over them all
        for (var i=0; i<checkboxes.length; i++) {
        // And stick the checked ones onto an array...
            if (checkboxes[i].checked) {
                checkboxesChecked.push(checkboxes[i].value.toString());
          //console.log(checkboxes[i])
            }
        }
    // Return the array if it is non-empty, or null
    return checkboxesChecked.length > 0 ? document.getElementById("id_cityofinterest").innerHTML = checkboxesChecked : document.getElementById("id_cityofinterest").innerHTML = null;
    }
  else
  {
      alert("You already have selected Any City")
  }
}