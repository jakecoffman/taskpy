$(document).ready(function () {
    var title = $('h2').text();
    $('li#' + title + ' a').css('background-image', 'url(/static/nav_base2.jpg)');
});
function addRun(url) {
    $.ajax(url, {
        type: "POST",
        dataType: "text",
        success: function (data) {
            // Update the runs in the more column 
            $('ul#runs').hide().load(data + " ul#runs li").show('slow');
        }
    });
}
function addRunFromJobs(url, job) {
    $.ajax(url, {
        type: "POST",
        dataType: "text",
        success: function (data) {
            // Update just the row that was run
            $('tr#' + job + "Job").hide().load("/jobs/ tr#" + job + "Job td").show("slow");
        }
    });
}
// Pass task, job, trigger, etc -- prompts for and creates new item (POST)
function createNewItem(item) {
    name = prompt("Enter new " + item + " name:");
    var postdata = {
        "name": name
    };
    $.ajax('/' + item + 's/', {
        type: "POST",
        dataType: "text",
        data: postdata,
        success: function (data) {
            window.location.reload();
        }
    });
}
// Pass full URL and name of the form to send to the server
function putUrlForm(url, formName) {
    $.ajax(url, {
        type: "PUT",
        dataType: "text",
        data: $("#" + formName).serializeArray(),
        success: function (data) {
            window.location.href = data;
        }
    });
}
function deleteTask(task) {
    answer = confirm("Permanently delete this task?");
    if (answer) {
        $.ajax('/tasks/' + task, {
            type: "DELETE"
        });
        window.location.href = '/tasks/';
    }
}
function addTrigger(type, value) {
    switch (type) {
        case 'Periodic':
            input = $("<input/>");
            input.attr("name", "value");
            input.attr("type", "text");
            if (value === undefined) {
                value = ""
            }
            input.attr("value", value)
            $("#dynamic").text("Cron:");
            $("#dynamic").append($("<br/>"));
            $("#dynamic").append(input);
            break;
        default:
            $("#dynamic").text("");
            break;
    }
}
function addInput(divName, attrName, choices, sel) {
    if (sel === undefined) {
        sel = 0;
    }
    var span = $("<span/>").attr("id", attrName + curInputs);
    var select = $("<select/>").attr("name", attrName).attr("id", attrName);
    $.each(choices, function (a, b) {
        option = $("<option/>");
        option.attr("value", b).text(b);
        if (a === sel) {
            option.attr("selected", "selected");
        }
        select.append(option);
    });
    div = $("#" + divName);
    span.append(select);
    del = $("<input/>").attr("value", "Remove");
    del.attr("type", "button");
    del.attr("onclick", "removeInput('" + (attrName + curInputs) + "');");
    span.append(del);
    span.append($("<p />"));
    div.append(span);
    span.hide().show("slow");
    curInputs++;
}
function removeInput(attrName) {
    removeMe = $("#" + attrName);
    removeMe.fadeOut(500, function () {
        removeMe.remove();
    });
}