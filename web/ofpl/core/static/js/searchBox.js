// This is for the search box
$(function() {

    var searchVal = "";
    var searchCurrentForm = 0;
    var color = "#9b394e";

    // underline the newly active tab
    var active = $(".searchTab").find("a")[0];
    $(active).css("text-decoration", "underline");

    /**
    * the element
    */
    var $ui = $('#ui_element');

    function srchbxUp(){
        $ui.find('.srchbx_up')
           .addClass('srchbx_down')
           .removeClass('srchbx_up')
           .andSelf()
           .find('.srchbx_dropdown')
           .hide();
        $("#searchBoxInput").css("border-color", "#222");
    }

    function srchbxDown(){
        $ui.find('.srchbx_down')
           .addClass('srchbx_up')
           .removeClass('srchbx_down')
           .andSelf()
           .find('.srchbx_dropdown')
           .show();
        $("#searchBoxInput").css("border-color", color);
    }

    function initializeListeners(){
                /**
                * on focus and on click display the dropdown,
                * and change the arrow image
                */
                $ui.find('.srchbx_input').bind('focus click',function(){
                    srchbxDown();
                });

                /**
                * on mouse leave hide the dropdown,
                * and change the arrow image
                */
                $ui.bind('mouseleave',function(){
                    srchbxUp();
                });

                /**
                *
                *  The above code for mouseleave doesn't work on touch devices.  Here is something
                *  make the check box window go away when the user taps a close button or (for disabled users tabbing through the page) loses focus
                *  -Kevin
                */
                $('#closeLink').bind('click',function(){  // We use the wrapper class instead because otherwise, it closes the checkbox box when we click on a checkbox. -Kevin
                    srchbxUp();
                });

                /**
                * selecting all checkboxes
                */
                /* $ui.find('.srchbx_dropdown').find('label[for="all"]').prev().bind('click',function(){
                *   $(this).parent().siblings().find(':checkbox').attr('checked',this.checked).attr('disabled',this.checked);
                * });
                */
    }

initializeListeners();






function saveSearchVal(){
    searchVal = $("#searchBoxInput").val();
}

function setFormToCatalog(){
    saveSearchVal();
    $("#searchFields").html("<input value=\"" + searchVal +
        "\" id=\"searchBoxInput\" autocomplete=\"off\" name=\"keyword\"" +
        " tabindex=\"5\" class=\"srchbx_input\" placeholder=\"Search\"" +
        " type=\"text\"/><input type=\"hidden\" name=\"ctx\" value=\"263.1033.0.0.1\" />");

    $('#ui_element').attr('action', 'https://search.illinoisheartland.org/view.aspx');
    $('#ui_element').attr('method', 'get');
    $('#ui_element').attr('onsubmit', "");
    //$("#searchTypeFilter").hide(200);

    searchCurrentForm = 0;
}


function setFormToDatabases(){
    saveSearchVal();
        $("#searchFields").html("<input value=\"" + searchVal + 
            "\" id=\"searchBoxInput\" autocomplete=\"off\" name=\"uquery\" size=\"65\" tabindex=\"5\" class=\"srchbx_input\" placeholder=\"Search\" type=\"text\"/>" +

            "<input name=\"direct\" value=\"true\" type=\"hidden\">" +
            "<input name=\"scope\" value=\"site\" type=\"hidden\">" +
            "<input name=\"site\" value=\"eds-live\" type=\"hidden\">" +
            "<input name=\"profile\" value=\"eds\" type=\"hidden\">" +
            "<input name=\"authtype\" value=\"ip,guest\" type=\"hidden\">" +
            "<input name=\"custid\" value=\"s5672256\" type=\"hidden\">" +
            "<input name=\"groupid\" value=\"main\" type=\"hidden\">" +
            "<input name=\"bquery\" value=\"\" type=\"hidden\">" +
            "<!--<input name=\"cli0\" value=\"FT\" type=\"hidden\">" +
            "<input name=\"clv0\" type=\"hidden\" value='N'>" +
            "<input  type=\"checkbox\" name=\"fulltext_checkbox\" id=\"fulltext_checkbox_all\" onclick=\"limittoFullText(this.form)\" >" +

            "<input name=\"cli1\" value=\"RV\" type=\"hidden\"><input name=\"clv1\"  type=\"hidden\" value='N'><input  name=\"scholarly_checkbox\" id=\"scholarly_checkbox_articles\" onclick=\"limittoScholarly(this.form)\" type=\"checkbox\">" +

            "<input name=\"cli2\" value=\"FC\" type=\"hidden\"><input name=\"clv2\" type=\"hidden\" value='N'><input  name=\"catalog_only_checkbox\" id=\"catalog_only_checkbox\" onclick=\"limittoCatalog(this.form)\" type=\"checkbox\">" +

            "-->");

    $('#ui_element').attr('action', 'https://search.ebscohost.com/login.aspx');
    $('#ui_element').attr('method', 'get');
    $('#ui_element').attr('onsubmit', "ebscoPreProcess(this)");
    //$("#searchTypeFilter").show(200);

    searchCurrentForm = 1;
}


function setFormToSiteSearch(){
    saveSearchVal();
    $("#searchFields").html(
        "<input value=\"" + searchVal + "\" type=\"text\" name=\"query\" id=\"searchBoxInput\" autocomplete=\"off\" class=\"srchbx_input\" placeholder=\"Search\">"
    );

    $('#ui_element').attr('action', '/search');
    $('#ui_element').attr('method', 'get');
    $('#ui_element').attr('onsubmit', "");

    //$("#searchTypeFilter").hide(200);

    searchCurrentForm = 2;
}



function swapTheForm(formId){

    switch(formId) {
      case 0:
        setFormToCatalog();
        break;

      case 1:
        setFormToDatabases();
        break;


      case 2:
        setFormToSiteSearch();
        break;

      default:
        alert("Something went wrong.");
        initializeListeners();
        return;
        break;
    }

    // reset all the tabs to not be underlined
    $(".searchTab").find("a").css("text-decoration", "none");

    // underline the newly active tab
    var active = $(".searchTab").find("a")[formId];
    $(active).css("text-decoration", "underline");

    // set the border color of the text input to the background color of the active tab
    var tempElem = $(".searchTab")[formId];
    color = $(tempElem).css("background-color");
    $("#searchBoxInput").css("border-color", color);

    // Put the text input box back into focus
    $("#searchBoxInput").focus();

    // Listeners must be initialized again because the elements to which they were listening were replaced
    initializeListeners();

}




// Bind the tab elements to their respective function calls of swapTheForm

$("#tabCatalog").click(function(){
  swapTheForm(0);
});


$("#tabDatabases").click(function(){
  swapTheForm(1);
});


$("#tabSiteSearch").click(function(){
  swapTheForm(2);
});




});
