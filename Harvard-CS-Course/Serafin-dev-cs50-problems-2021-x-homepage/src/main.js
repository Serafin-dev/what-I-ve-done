window.h1 = document.querySelector('h1');
function createElems(elemsTags){
    var l = [];
    elemsTags.forEach(function(elem){
        l.push(document.createElement(elem));
    })
    return l;
}
function setAttrs(elem, attrs, values){
    for (var i = 0; i < attrs.length; i++){
        elem.setAttribute(attrs[i], values[i]);
    }
}
function addForm(){
    var parentDiv = document.querySelector('.answers');
    var elTags = ['FORM', 'div', 'input', 'button'];
    var elems = createElems(elTags);

    setAttrs(elems[1], ['class'], ['form-group mx-sm-3 mb-2']);
    setAttrs(elems[2], ['type', 'id', 'class', 'placeholder'], ['text', 'name','form-control', 'your name here...']);
    setAttrs(elems[3], ['type', 'class'], ['submit', 'btn btn-primary mb-2']);

    elems[3].innerHTML = 'Enter';

    elems[1].appendChild(elems[2]);
    elems[0].appendChild(elems[1]);
    elems[0].appendChild(elems[3]);
    parentDiv.appendChild(elems[0]);
    return elems[0];
}
function deleteButtons(){
    var ansButtons = document.querySelectorAll('.btn');
    for (var i = 0; i < ansButtons.length; i++){
        ansButtons[i].remove();
    }
}
function redirect(){
    window.location.replace("home.html")
}
document.querySelector('#if').addEventListener('click', function(){
    window.h1.innerHTML = ":) I'm Særafin. What's your name?";
    deleteButtons();

    var form = addForm();
    form.onsubmit = () => {
        var name = document.querySelector('#name').value;
        window.h1.innerHTML = `Hi ${name}, I'll tell you a little about myself...`;
        form.remove();
        setTimeout(redirect, 2500);
        return false;
    }
});


