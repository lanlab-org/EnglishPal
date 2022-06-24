var isHighlight = true;

function cancelBtnHandler() {
    cancel_highLight();
    document.getElementById("text-content").removeEventListener("click", fillinWord, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillinWord, false);
    document.getElementById("text-content").addEventListener("click", fillinWord2, false);
    document.getElementById("text-content").addEventListener("touchstart", fillinWord2, false);
}

function showBtnHandler() {
    document.getElementById("text-content").removeEventListener("click", fillinWord2, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillinWord2, false);
    document.getElementById("text-content").addEventListener("click", fillinWord, false);
    document.getElementById("text-content").addEventListener("touchstart", fillinWord, false);
    highLight();
}

function getWord() {
    var word = window.getSelection ? window.getSelection() : document.selection.createRange().text;
    return word;
}

function highLight() {
    if(!isHighlight) return;
    var txt = document.getElementById("article").innerText;
    var sel_word1 = document.getElementById("selected-words");
    var sel_word2 = document.getElementById("selected-words2");
    if (sel_word1 != null) {
        var list = sel_word1.value.split(" ");
        for (var i = 0; i < list.length; ++i) {
            list[i] = list[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list[i] != "" && "<mark>".indexOf(list[i]) == -1 && "</mark>".indexOf(list[i]) == -1) {
                txt = txt.replace(new RegExp(list[i], "g"), "<mark>" + list[i] + "</mark>");
            }
        }
    }
    if (sel_word2 != null) {
        var list2 = sel_word2.value.split(" ");
        for (var i = 0; i < list2.length; ++i) {
            list2[i] = list2[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list2[i] != "" && "<mark>".indexOf(list2[i]) == -1 && "</mark>".indexOf(list2[i]) == -1) {
                txt = txt.replace(new RegExp(list2[i], "g"), "<mark>" + list2[i] + "</mark>");
            }
        }
    }
    document.getElementById("article").innerHTML = txt;
}

function cancel_highLight() {
    var txt = document.getElementById("article").innerText;
    var sel_word1 = document.getElementById("selected-words");
    var sel_word2 = document.getElementById("selected-words2");
    if (sel_word1 != null) {
        var list = sel_word1.value.split(" ");
        for (var i = 0; i < list.length; ++i) {
            list[i] = list[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list[i] != "") {
                txt = txt.replace("<mark>" + list[i] + "</mark>", "list[i]");
            }
        }
    }
    if (sel_word2 != null) {
        var list2 = sel_word1.value.split(" ");
        for (var i = 0; i < list2.length; ++i) {
            var list2 = sel_word2.value.split(" ");
            list2[i] = list2[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list2[i] != "") {
                txt = txt.replace("<mark>" + list[i] + "</mark>", "list[i]");
            }
        }
    }
    document.getElementById("article").innerHTML = txt;
}

function fillinWord() {
    highLight();
}

function fillinWord2() {
    cancel_highLight();
}

function ChangeHighlight() {
    if (isHighlight) {
        isHighlight = false;
        cancel_highLight();
    } else {
        isHighlight = true;
        highLight();

    }
}

showBtnHandler();
