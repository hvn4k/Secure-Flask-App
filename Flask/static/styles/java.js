password="budgetdrive"
username="Admin"
function ValidateEmail()
{
    

    textbox1=document.getElementById("box1").value;
    textbox2=document.getElementById("box2").value;
    if(textbox1==username && textbox2==password)
    {

        alert("correct password")
        window.location.assign("Service.html")
    }
    if(textbox1=="" ||textbox2=="")
    {
           alert("Please enter credentials")
    }
   if(textbox1!=username || textbox2!=password || textbox1!="" && textbox2!="")
    {
          alert("Wrong Credentials")
    }
}