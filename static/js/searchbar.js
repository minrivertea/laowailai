


function toggle_visibility(id) {
  var e = document.getElementById("comments_full_" + id);
  if (e.style.height == "100%") {	
  }
  else {
    $("#comments_full_" + id).animate({
          height: "100%",
        }, 100, function() {
          $("#comments_full_" + id).fadeIn('100');
          $("#show_comments" + id).removeAttr("onclick")	
        } 
    );
  }
}

function clearInput(elem) {
    if (elem.value && elem.defaultValue == elem.value) {
        elem.value = new String();
    }
    elem.style.color = 'black';
};

