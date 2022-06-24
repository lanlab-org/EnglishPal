isRead = true;
isChoose = true;
var reader = window.speechSynthesis; // 全局定义朗读者，以便朗读和暂停

function getWord(){
   var word = window.getSelection?window.getSelection():document.selection.createRange().text;
   return word;
}
function fillinWord(){
   var word = getWord();
   if (isRead) read(word);
   if (!isChoose) return;
   var element = document.getElementById("selected-words");
   element.value = element.value + " " + word;
}
document.getElementById("text-content").addEventListener("click", fillinWord, false);
function read(s){
   var msg = new SpeechSynthesisUtterance(s);
   reader.speak(msg);
}
function onReadClick(){
    isRead = !isRead;
    if(!isRead){
       reader.cancel();
    }
}
function onChooseClick(){
    isChoose = !isChoose;
}