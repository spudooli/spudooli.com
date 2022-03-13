$("#contactForm").validator().on("submit", function (event) {
    if (event.isDefaultPrevented()) {
        // handle the invalid form...
        formError();
        submitMSG(false, "Did you fill in the form properly?");
    } else {
        // everything looks good!
        event.preventDefault();
        submitForm();
    }
});


function submitForm(){
    // Initiate Variables With Form Content
    var name = $("#name").val();
    var email = $("#email").val();
    var subject = $("#subject").val();
    var message = $("#message").val();
 

    $.ajax({
        type: "POST",
        url: "../contact_me.php.htm",
        data: "name=" + name + "&email=" + email + "&subject=" + subject + "&message=" + message,
        success : function(text){
            if (text == "success"){
                formSuccess();
            } else {
                formError();
                submitMSG(false,text);
            }
        }
    });
}

function formSuccess(){
    $("#contactForm")[0].reset();
    submitMSG(true, "Message Submitted!")
}

function formError(){
    $("#contactForm").removeClass().addClass('').one('', function(){
        $(this).removeClass();
    });
}

function submitMSG(valid, msg){
    if(valid){
        var msgClasses = "align-center alert alert-success";
    } else {
        var msgClasses = "align-center alert alert-danger";
    }
    $("#msgresult").removeClass().addClass(msgClasses).slideDown().text(msg);
}

 //reset previously set border colors and hide all message on .keyup()
    $("#contact-form input, #contact-form textarea").keyup(function(){
        $("#contact-form input, #contact-form textarea").css('border-color', '');
        $("#msgresult").slideUp();
    });