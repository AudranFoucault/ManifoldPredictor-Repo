const nameInput = document.getElementById("nameInput");
const getButton = document.getElementById("getButton");
const setButton = document.getElementById("setButton");
const output = document.getElementById("output");

getButton.addEventListener("click", ()=>{
    const value = nameInput.value;
    output.innerText = `You texted : ${value}`
});

setButton.addEventListener("click", ()=>{
    nameInput.value = "Hello world";
    output.innerText = "input value changed"
})